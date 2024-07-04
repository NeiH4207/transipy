import ast
import docx
from time import sleep
from typing import Dict, List, Optional, Union

import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor
from googletrans import Translator
from loguru import logger

from transipy.utils import md5hash, split_df_by_group

TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"
MAX_TEXT_LENGTH = 50000
CHUNK_SIZE = 5000

def translate(text: str, src: str, dest: str) -> str:
    """Translate text from source language to destination language."""
    if not isinstance(text, str):
        return text
    
    if len(text) > MAX_TEXT_LENGTH:
        logger.warning(f"Text length is too long: {len(text)} (max: {MAX_TEXT_LENGTH} characters), skipping...")
        return text
    
    chunks = split_text_into_chunks(text)
    translated_chunks = translate_chunks(chunks, src, dest)
    return ' '.join(translated_chunks)

def split_text_into_chunks(text: str) -> List[str]:
    """Split text into chunks of maximum length."""
    if len(text) <= CHUNK_SIZE:
        return [text]
    
    chunks = []
    start_point = 0
    while start_point < len(text):
        end_point = text.find('.', start_point + CHUNK_SIZE)
        if end_point == -1:
            end_point = len(text)
        chunks.append(text[start_point:end_point])
        start_point = end_point + 1
    return chunks

def translate_chunks(chunks: List[str], src: str, dest: str) -> List[str]:
    """Translate a list of text chunks."""
    translated_chunks = []
    for chunk_text in chunks:
        try:
            translated_chunk = translate_single_chunk(chunk_text, src, dest)
            translated_chunks.append(translated_chunk)
        except Exception as e:
            logger.exception(f"Error translating chunk: {e}")
            translated_chunks.append(chunk_text)
    return translated_chunks

def translate_single_chunk(chunk_text: str, src: str, dest: str) -> str:
    """Translate a single chunk of text."""
    params = {
        "client": "gtx",
        "sl": src,
        "tl": dest,
        "dt": "t",
        "q": chunk_text
    }
    try:
        with requests.get(TRANSLATE_URL, params=params) as response:
            response.raise_for_status()
            t = response.text.replace('null', '"null"').replace('true', 'True')
            t = ast.literal_eval(t)
            return ''.join([x[0] for x in t[0]])
    except requests.RequestException:
        logger.warning("Google Translate API failed, falling back to googletrans library")
        return Translator().translate(chunk_text, src=src, dest=dest).text

def translate_series(series: pd.Series, src: str = 'en', dest: str = 'vi') -> pd.Series:
    """Translate a pandas Series."""
    return series.apply(translate, src=src, dest=dest)

def translate_column(df: pd.DataFrame, column: str, src: str = 'en', dest: str = 'vi', chunk_size: int = 4, dictionary: Dict[str, str] = {}) -> pd.DataFrame:
    """Translate a specific column in a DataFrame."""
    df[column] = df[column].fillna('').astype(str).replace("nan", '')
    unique_values = df[column].unique()
    unique_series = pd.Series(unique_values, name=column)
    unique_series.index = unique_series.index.map(lambda x: f'group_{x // chunk_size}')
    
    hashing_dictionary = {md5hash(key.lower()): value for key, value in dictionary.items()}
    
    n_chunks = (unique_series.shape[0] // chunk_size) + 1
    with ThreadPoolExecutor() as executor:
        chunks = split_df_by_group(unique_series, n_chunks)
        results = list(executor.map(lambda chunk: translate_series(chunk, src, dest), chunks))
    
    for chunk, result in zip(chunks, results):
        for value, translated in zip(chunk, result):
            md5_str = md5hash(value.lower())
            if md5_str not in hashing_dictionary:
                hashing_dictionary[md5_str] = translated

    df[column] = df[column].apply(lambda x: hashing_dictionary.get(md5hash(x.lower()), x))
    df[column] = df[column].replace({'null': ''}).fillna('')
    sleep(0.1)
    return df

def translate_df(df: pd.DataFrame, columns: Optional[List[str]] = None, src: str = 'en', dest: str = 'vi', chunk_size: int = 4, dictionary: Dict[str, str] = {}, output_file: Optional[str] = None) -> pd.DataFrame:
    """Translate specified columns in a DataFrame."""
    translated_df = df.copy()
    
    for column in columns:
        if column not in translated_df.columns:
            logger.warning(f"Column {column} not found in the dataframe, skipping...")
            continue
        
        logger.info(f"Translating column: {column}")
        if translated_df[column].dtype == 'object':
            translate_column(translated_df, column, src, dest, chunk_size, dictionary)
    
    if output_file:
        translated_df.to_csv(output_file, index=False)
    
    return translated_df

def translate_excel(dfs: Dict[str, pd.DataFrame], sheets: Optional[List[str]] = None, src: str = 'en', dest: str = 'vi', chunk_size: int = 4, dictionary: Dict[str, str] = {}, output_file: Optional[str] = None) -> Dict[str, pd.DataFrame]:
    """Translate specified sheets in an Excel file."""
    sheets = sheets or list(dfs.keys())
        
    for sheet in sheets:
        if sheet not in dfs:
            logger.warning(f"Sheet {sheet} not found in the dataframe, skipping...")
            continue
        
        logger.info(f"Translating sheet: {sheet}")
        columns = dfs[sheet].columns
        dfs[sheet] = translate_df(
            df=dfs[sheet], 
            columns=columns,
            src=src, 
            dest=dest, 
            chunk_size=chunk_size, 
            dictionary=dictionary
        )
        
    if output_file:
        with pd.ExcelWriter(output_file) as writer:
            for sheet_name in sheets:
                dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    
    return dfs

def translate_docx(file_path: str, src: str = 'en', dest: str = 'vi', chunk_size: int = 4, dictionary: Dict[str, str] = {}, output_file: Optional[str] = None) -> docx.Document:
    """Translate a Word document."""
    doc = docx.Document(file_path)
    translated_doc = docx.Document()
    
    raw_docs = [paragraph.text for paragraph in doc.paragraphs]
    
    df = pd.DataFrame(raw_docs, columns=['text'])
    
    df = translate_df(
        df=df, 
        columns=['text'],
        src=src, 
        dest=dest, 
        chunk_size=chunk_size, 
        dictionary=dictionary
    )
    
    for text in df['text']:
        translated_doc.add_paragraph(text)
        
    if output_file:
        translated_doc.save(output_file)
        
    return translated_doc