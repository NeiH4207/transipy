from time import sleep
import requests
import ast
import requests
import ast
import pandas as pd
from multiprocessing import Pool, cpu_count
from googletrans import Translator
from loguru import logger

from transipy.utils import split_df_by_group

def translate(text, src, dest):
    if not isinstance(text, str):
        return text
    
    params = {
        "client": "gtx",
        "sl": src,
        "tl": dest,
        "dt": "t",
        "q": text
    }
    url = "https://translate.googleapis.com/translate_a/single"
    with requests.get(url, params=params) as response:
        if response.status_code == 200:
            t = response.text.replace('null', '"null"')
            t = t.replace('true', 'True')
            t = ast.literal_eval(t)
            t = ''.join([x[0] for x in t[0]])
            return t
        else:
            try:
                return Translator().translate(text, src=src, dest=dest).text
            except Exception as e:
                logger.error(f"Error when translating {text} from {src} to {dest}: {e}")
                return text
            
    
def translate_series(series, src='en', dest='vi'):
    return series.apply(translate, src=src, dest=dest)


def translate_column(df, column, src='en', dest='vi', chunk_size=16, default_dict={}):
    unique_values = df[column].unique()
    unique_series = pd.Series(unique_values, name=column)
    unique_series.index = unique_series.index.map(lambda x: f'group_{x // chunk_size}')
    
    n_chunks = (unique_series.shape[0] // chunk_size) + 1
    num_process = min(n_chunks, max(1, cpu_count() // 2)) # Use half of the available CPU cores
    chunks = split_df_by_group(unique_series, num_process)
    
    params = [(chunks[i], src, dest) for i in range(num_process)]
    
    dictionary = {}
    with Pool(num_process) as pool:
        results = pool.starmap(translate_series, params)
        for i, chunk in enumerate(chunks):
            for j, value in enumerate(results[i]):
                dictionary[chunk.values[j].lower()] = value

    dictionary.update(default_dict)
    df[column] = df[column].apply(lambda x: dictionary.get(x.lower(), x))
    df[column] = df[column].replace({'null': ''}).fillna('')
    sleep(0.5)
    return df

def translate_csv(df, src='en', dest='vi', output_file=None, chunk_size=16, default_dict={}):
    translated_df = df.copy()
    for column in translated_df.columns:
        logger.info(f"Translating column: {column}")
        translate_column(translated_df, column, src, dest, chunk_size, default_dict)
    
    if output_file:
        translated_df.to_csv(output_file, index=False)
    
    return translated_df

def translate_excel(dfs, src='en', dest='vi', output_file=None, chunk_size=16, default_dict={}):
    for sheet in dfs.keys():
        logger.info(f"Translating sheet: {sheet}")
        dfs[sheet] = translate_csv(dfs[sheet], src, dest, chunk_size=chunk_size, default_dict=default_dict)
        
        with pd.ExcelWriter(output_file) as writer:
            for sheet_name in dfs.keys():
                dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    return dfs