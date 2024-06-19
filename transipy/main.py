import argparse
import json
import os
from loguru import logger
import pandas as pd
from transipy.trans_helper import translate_df, translate_docx, translate_excel
from transipy.utils import *
from googletrans import LANGUAGES

def get_parser():
    parser = argparse.ArgumentParser(
        description='Translate text in a file (.csv/.txt/.tsv/.docx/.xlsx) from source language to target language.',
    )
    parser.add_argument('-f', '--file-path', type=str, required=True, help='The source file path')
    parser.add_argument('-l', '--sep', type=str, default=None, help='The separator of the file [comma, tab, space,...]')
    parser.add_argument('-s', '--source', type=str, required=True, help='Source language (e.g. en, vi)')
    parser.add_argument('-t', '--target', type=str, required=True, help='target language (e.g. en, vi)')
    parser.add_argument('-c', '--chunk-size', type=int, default=1, help='The chunk size for splitting the translation process')
    parser.add_argument('-o', '--output-file', type=str, default=None, help='The output file path')
    parser.add_argument('-d', '--dictionary', type=str, default=None, help='The dictionary file path, using for custom translation')
    parser.add_argument('--column', type=str, default=None, help='The column name to translate, separated by comma')
    parser.add_argument('--skip', type=str, default=None, help='The column name to skip, separated by comma')
    parser.add_argument('--sheet', type=str, default=None, help='The sheet name to translate, separated by comma (only for .xlsx files)')
    return parser.parse_args()

def main():    
    args = get_parser()
    input_file = args.file_path
    source_language = args.source
    target_language = args.target
    chunk_size = args.chunk_size
    output_file = args.output_file
    
    if not os.path.exists(args.file_path):
        logger.error(f"File not found: {args.file_path}")
        return
    
    if source_language not in LANGUAGES:
        logger.error(f"Unsupported source language: {source_language}")
        return
    
    if target_language not in LANGUAGES:
        logger.error(f"Unsupported target language: {target_language}")
        return
    
    if chunk_size < 1:
        logger.error("Chunk size must be greater than 0")
        return
    
    dictionary = {}
    
    if args.dictionary:
        try:
            with open(args.dictionary) as f:
                dictionary = json.load(f)
        except Exception as e:
            logger.error(f"Error loading default dictionary: {e}")
            return
    
    file_extension = get_file_extension(input_file)
    
    if not is_supported_file(input_file):
        logger.error("Unsupported file format. Please use .csv/.tsv/.txt/.docx or .xlsx files.")
        return
    
    if not args.output_file:
        output_extention = f"_{source_language}_{target_language}{file_extension}"
        output_file = input_file.replace(file_extension, output_extention)
    
    if is_csv(input_file):
        sep = get_separetor(args.sep) if args.sep else ','
        df = pd.read_csv(input_file, sep=sep)
        columns = args.column.split(',') if args.column else df.columns
        skips = args.skip.split(',') if args.skip else []
        columns = [col for col in columns if col not in skips]
        
        translated_df = translate_df(
            df=df, 
            columns=columns,
            src=source_language, 
            dest=target_language, 
            chunk_size=chunk_size, 
            dictionary=dictionary, 
            output_file=output_file
        )
        translated_df.to_csv(output_file, index=False)
    
    elif is_tsv(input_file):
        sep = get_separetor(args.sep) if args.sep else '\t'
        df = pd.read_csv(input_file, sep=sep)
        columns = args.column.split(',') if args.column else df.columns
        skips = args.skip.split(',') if args.skip else []
        columns = [col for col in columns if col not in skips]
        
        translated_df = translate_df(
            df=df, 
            columns=columns,
            src=source_language, 
            dest=target_language, 
            chunk_size=chunk_size, 
            dictionary=dictionary, 
            output_file=output_file
        )
        translated_df.to_csv(output_file, index=False)
        
    elif is_excel(file_extension):
        dfs = pd.read_excel(input_file, sheet_name=get_all_excel_sheet_names(input_file))
        sheets = args.sheet.split(',') if args.sheet else dfs.keys()
        sheets = [sheet for sheet in sheets if sheet in dfs.keys()]
        
        translate_excel(
            dfs=dfs, 
            sheets=sheets,
            src=source_language, 
            dest=target_language, 
            chunk_size=chunk_size, 
            dictionary=dictionary, 
            output_file=output_file
        )
        
    elif is_text(file_extension):
        with open(input_file, 'r') as f:
            texts = f.readlines()
        df = pd.DataFrame(texts, columns=['text'])
        df = translate_df(
            df=df, 
            columns=['text'],
            src=source_language, 
            dest=target_language, 
            chunk_size=chunk_size, 
            dictionary=dictionary, 
            output_file=output_file
        )
        with open(output_file, 'w') as f:
            f.write('\n'.join(df['text'].tolist()))
    elif is_docx(file_extension):
        translate_docx(
            file_path=input_file, 
            src=source_language, 
            dest=target_language, 
            chunk_size=chunk_size, 
            dictionary=dictionary, 
            output_file=output_file
        )
    else:
        logger.error("Unsupported file format. Please use .csv/.tsv/.txt/docx or .xlsx files.")
        return