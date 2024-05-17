import argparse
from multiprocessing import Pool, cpu_count
import time
from loguru import logger
import pandas as pd
from transipy.utils import *

def translate_sample(x, src='en', dest='vi'):
    if isinstance(x, str):
        return translate(x, src=src, dest=dest)
    else:
        return x
    
def translate_series(series, src='en', dest='vi'):
    return series.apply(translate_sample, src=src, dest=dest)

def split_df_by_group(_df, chunks):  
    df_split=[]
    entities = _df.index.unique()
    for i in range(chunks): df_split.append(_df[_df.index.isin(entities[i::chunks])].copy())       
    return df_split    

def translate_column(df, column, src='en', dest='vi', chunk_size = 16, default_dict = {}):
    unique_values = df[column].unique()
    unique_series = pd.Series(unique_values, name=column)
    
    unique_series.index = unique_series.index.map(lambda x: 'group_' + str(x // chunk_size))
    n_chunks = unique_series.shape[0] // chunk_size + 1
    num_process = min(n_chunks, max(1, cpu_count() // 2))
    chunks = split_df_by_group(unique_series, num_process)

    params = []
    for i in range(num_process):
        params.append((chunks[i], src, dest))
        
    dictionary = {}
    
    with Pool(num_process) as p:
        results = p.starmap(translate_series, params)
        
        for i in range(num_process):
            for j in range(len(results[i])):
                dictionary[chunks[i].values[j].lower()] = results[i].values[j]
    
    for key in default_dict:
        dictionary[key] = default_dict[key]
    
    df[column] = df[column].apply(lambda x: dictionary[x.lower()] if x.lower() in dictionary.keys() else x)
    df[column] = df[column].apply(lambda x: '' if pd.isnull(x) or x == 'null' else x)
    
    # Sleep to avoid being blocked by Google Translate
    time.sleep(0.25)
    return df

def translate_csv(df, src='en', dest='vi', output_file=None, save_every_column=False):
    """
    Translate selected columns of a DataFrame from source language to target language.
    
    Parameters:
    - df: DataFrame to be translated
    - columns: list of columns to be translated
    - src: source language (default: 'en')
    - dest: target language (default: 'vi')
    - output_file: path to save the translated DataFrame (default: None)
    - save_every_column: whether to save the translated DataFrame after each column is translated (default: False)
    
    Returns:
    - df: translated DataFrame
    """
    
    translated_df = df.copy()
    
    for column in translated_df.columns:
        translate_column(translated_df, column, src, dest)
        logger.info(f"Translated column: {column}")
        # Save the translated DataFrame after each column is translated
        if save_every_column:
            translated_df.to_csv(output_file, index=False)
    
    return translated_df

def get_parser():
    parser = argparse.ArgumentParser(
        description='Translate text in a file (.csv/.txt) from source language to target language.',
    )
    parser.add_argument('-f', '--file-path', type=str, default='examples/sample.csv', help='The source file path')
    parser.add_argument('--sep', type=str, help='The separator of the file')
    parser.add_argument('-s', '--source', type=str, default='en', help='Source language (e.g. en, vi)')
    parser.add_argument('-t', '--target', type=str, default='vi', help='target language (e.g. en, vi)')
    parser.add_argument('-o', '--output-file', type=str, default=None, help='The output file path')
    parser.add_argument('--save-every-column', action='store_true', help='Save the translated DataFrame after each column is translated')
    return parser

def main():
    args = get_parser().parse_args()
    input_file = args.file_path
    source_langugage = args.source
    target_language = args.target
    file_extension = get_file_extension(input_file)
    output_file = args.output_file
    
    if is_csv(input_file):
        if output_file is None:
            output_file = input_file.replace(file_extension, f"_{source_langugage}_{target_language}.csv")
            
        df = pd.read_csv(input_file)
        df = translate_csv(df, source_langugage, target_language, output_file, 
                           save_every_column=args.save_every_column)
        df.to_csv(output_file, index=False)
    
    
if __name__ == '__main__':
    main()