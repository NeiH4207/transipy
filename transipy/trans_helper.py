from time import sleep
import time
import requests
import ast
import requests
import ast
import pandas as pd
from multiprocessing import Pool, cpu_count
from googletrans import Translator
from loguru import logger

from transipy.utils import md5hash, split_df_by_group

def translate(text, src, dest):
    if not isinstance(text, str):
        return text
    
    if len(text) > 50000:
        logger.warning(f"Text length is too long: {len(text)} (max: 10000 characters), skipping...")
        return text
    elif len(text) > 5000:
        max_length = 5000
        chunks = []
        start_point = 0
        while start_point < len(text):
            end_point = text.find('.', start_point + max_length)
            if end_point == -1:
                end_point = len(text)
            chunks.append(text[start_point:end_point])
            start_point = end_point + 1
    else:
        chunks = [text]
        
    translated_chunks = []
    
    for chunk_text in chunks:
        params = {
            "client": "gtx",
            "sl": src,
            "tl": dest,
            "dt": "t",
            "q": chunk_text
        }
        try:
            url = "https://translate.googleapis.com/translate_a/single"
            with requests.get(url, params=params) as response:
                if response.status_code == 200:
                    t = response.text.replace('null', '"null"')
                    t = t.replace('true', 'True')
                    t = ast.literal_eval(t)
                    t = ''.join([x[0] for x in t[0]])
                    translated_chunks.append(t)
                else:
                    try:
                        response_text = Translator().translate(text, src=src, dest=dest).text
                        translated_chunks.append(response_text)
                    except Exception as e:
                        logger.error(f"Error from GG-translate-API when translating text with length {len(text)}: {e}")
                        return text
        except Exception as e:
            logger.error(f"Error from requests when translating text with length {len(text)}: {e}")
            return text
                
    return ' '.join(translated_chunks)
                
    
def translate_series(series, src='en', dest='vi'):
    return series.apply(translate, src=src, dest=dest)


def translate_column(df, column, src='en', dest='vi', chunk_size=4, dictionary={}):
    df[column] = df[column].fillna('').astype(str).replace("nan", '')
    unique_values = df[column].unique()
    unique_series = pd.Series(unique_values, name=column)
    unique_series.index = unique_series.index.map(lambda x: f'group_{x // chunk_size}')
    
    hashing_dictionary = {}
    for key, value in dictionary.items():
        hashing_dictionary[md5hash(key.lower())] = value
        
    dictionary = hashing_dictionary
    
    n_chunks = (unique_series.shape[0] // chunk_size) + 1
    num_process = min(n_chunks, max(1, cpu_count() // 4 * 3)) # Use half of the available CPU cores
    chunks = split_df_by_group(unique_series, num_process)
    
    params = [(chunks[i], src, dest) for i in range(num_process)]
        
    with Pool(num_process) as pool:
        try:
            results = pool.starmap(translate_series, params)
        except Exception as e:
            logger.error(f"Error translating column {column}: {e}")
            return df
        for i, chunk in enumerate(chunks):
            for j, value in enumerate(results[i]):
                md5_str = md5hash(chunk.values[j].lower())
                if md5_str not in dictionary:
                    dictionary[md5_str] = value

    df[column] = df[column].apply(lambda x: dictionary.get(md5hash(x.lower()), x))
    df[column] = df[column].replace({'null': ''}).fillna('')
    sleep(0.1)
    return df

def translate_df(df, columns=None, src='en', dest='vi', chunk_size=4, dictionary={}, output_file=None):
    translated_df = df.copy()
    if columns is None:
        columns = translated_df.columns
        
    for column in columns:
        if column not in translated_df.columns:
            logger.warning(f"Column {column} not found in the dataframe, skipping...")
            continue
        
        logger.info(f"Translating column: {column}")
        if translated_df[column].dtype != 'object':
            continue
        translate_column(translated_df, column, src, dest, chunk_size, dictionary)
    
    if output_file:
        translated_df.to_csv(output_file, index=False)
    
    return translated_df

def translate_excel(dfs, sheets=None, src='en', dest='vi', chunk_size=4, dictionary={}, output_file=None):
    if sheets is None:
        sheets = dfs.keys()
        
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
            dictionary=dictionary, 
            output_file=output_file
        )
        
        with pd.ExcelWriter(output_file) as writer:
            for sheet_name in sheets:
                dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    return dfs