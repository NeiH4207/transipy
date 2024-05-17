import argparse
import json
from multiprocessing import Pool, cpu_count
import time
from loguru import logger
import pandas as pd
from transipy.utils import *
    
def translate_series(series, src='en', dest='vi'):
    return series.apply(translate, src=src, dest=dest)

def split_df_by_group(_df, chunks):  
    df_split=[]
    entities = _df.index.unique()
    for i in range(chunks): df_split.append(_df[_df.index.isin(entities[i::chunks])].copy())       
    return df_split    

def translate_column(df, column, src='en', dest='vi', chunk_size = 16, default_dict = {}):
    """
    This code defines a function translate_column that translates a specific column in a DataFrame from a source language to a target language. It uses a default dictionary for translations, splits the data into chunks, and processes the translation in parallel using multiprocessing. Finally, it applies the translation to the column in the DataFrame and returns the updated DataFrame.

    Parameters:
    - df: DataFrame to be translated
    - column: Name of the column to translate
    - src: Source language (default: 'en')
    - dest: Target language (default: 'vi')
    - chunk_size: Size of the chunk for grouping unique values (default: 16)
    - default_dict: Default dictionary for translations (default: empty dictionary)

    Returns:
    - df: DataFrame with the translated column
    """
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

def translate_csv(df, src='en', dest='vi', output_file=None, chunk_size=16, default_dict={}):
    """
    Translate selected columns of a DataFrame from source language to target language.
    
    Parameters:
    - df: DataFrame to be translated
    - columns: list of columns to be translated
    - src: source language (default: 'en')
    - dest: target language (default: 'vi')
    - output_file: path to save the translated DataFrame (default: None)
    
    Returns:
    - df: translated DataFrame
    """
    
    translated_df = df.copy()
    
    for column in translated_df.columns:
        logger.info(f"Translating column: {column}")
        translate_column(translated_df, column, src, dest, chunk_size, default_dict)
        
        if output_file is not None:
            translated_df.to_csv(output_file, index=False)
    
    return translated_df

def translate_excel(dfs, src='en', dest='vi', output_file=None, chunk_size=16, default_dict={}):
    """
    Translate Excel sheets from source language to target language.

    Parameters:
    - dfs: Dictionary of DataFrames representing Excel sheets
    - src: Source language (default: 'en')
    - dest: Target language (default: 'vi')
    - output_file: Path to save the translated Excel file (default: None)
    - chunk_size: Number of rows to translate at a time (default: 16)

    Returns:
    - dfs: Dictionary of translated DataFrames
    """
    for sheet in dfs.keys():
        logger.info(f"Translating sheet: {sheet}")
        dfs[sheet] = translate_csv(dfs[sheet], src, dest, chunk_size=chunk_size, default_dict=default_dict)
        
        with pd.ExcelWriter(output_file) as writer:
            for sheet_name in dfs.keys():
                dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    return dfs

def get_parser():
    parser = argparse.ArgumentParser(
        description='Translate text in a file (.csv/.txt) from source language to target language.',
    )
    parser.add_argument('-f', '--file-path', type=str, required=True, help='The source file path')
    parser.add_argument('--sep', type=str, default=None, help='The separator of the file')
    parser.add_argument('-s', '--source', type=str, required=True, help='Source language (e.g. en, vi)')
    parser.add_argument('-t', '--target', type=str, required=True, help='target language (e.g. en, vi)')
    parser.add_argument('-c', '--chunk-size', type=int, default=8, help='The chunk size for splitting the translation process')
    parser.add_argument('-o', '--output-file', type=str, default=None, help='The output file path')
    parser.add_argument('--default-dict', type=str, default=None, help='The default dictionary path for translations')
    return parser

def main():
    args = get_parser().parse_args()
    input_file = args.file_path
    source_langugage = args.source
    target_language = args.target
    chunk_size = args.chunk_size
    file_extension = get_file_extension(input_file)
    default_dict = {}
    
    if args.default_dict is not None:
        try:
            with open(args.default_dict) as f:
                default_dict = json.load(f)
        except Exception as e:
            logger.error(f"Error loading default dictionary: {e}")
            return
    
    if args.output_file is None:
        output_file = input_file.replace(file_extension, f"_{source_langugage}_{target_language}{file_extension}")
    else:
        output_file = args.output_file
    
    if is_csv(input_file):
        df = pd.read_csv(input_file, sep=get_separetor(args.sep))
        df = translate_csv(df, source_langugage, target_language, output_file, chunk_size, default_dict)
        df.to_csv(output_file, index=False)
    
    elif is_excel(file_extension):
        dfs = pd.read_excel(input_file, sheet_name=get_all_excel_sheet_names(input_file))
        dfs = translate_excel(dfs, source_langugage, target_language, output_file, chunk_size, default_dict)
    elif is_text(file_extension):
        with open(input_file, 'r') as f:
            texts = f.readlines()
            
        df = pd.DataFrame(texts, columns=['text'])
        df = translate_csv(df, source_langugage, target_language, None, chunk_size, default_dict)
        translated_texts = df['text'].tolist()
        with open(output_file, 'w') as f:
            f.write('\n'.join(translated_texts))
    else:
        logger.error("Unsupported file format. Please use .csv or .xlsx files.")
        return
    
    
if __name__ == '__main__':
    main()