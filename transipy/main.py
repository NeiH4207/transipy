import argparse
import json
import os
from loguru import logger
import pandas as pd
from transipy.trans_helper import translate_csv, translate_excel
from transipy.utils import *
from googletrans import LANGUAGES

def get_parser():
    parser = argparse.ArgumentParser(
        description='Translate text in a file (.csv/.txt) from source language to target language.',
    )
    parser.add_argument('-f', '--file-path', type=str, required=True, help='The source file path')
    parser.add_argument('-l', '--sep', type=str, default=None, help='The separator of the file')
    parser.add_argument('-s', '--source', type=str, required=True, help='Source language (e.g. en, vi)')
    parser.add_argument('-t', '--target', type=str, required=True, help='target language (e.g. en, vi)')
    parser.add_argument('-c', '--chunk-size', type=int, default=8, help='The chunk size for splitting the translation process')
    parser.add_argument('-o', '--output-file', type=str, default=None, help='The output file path')
    parser.add_argument('--default-dict', type=str, default=None, help='The default dictionary path for translations')
    return parser

def main():    
    args = get_parser().parse_args()
    if not os.path.exists(args.file_path):
        logger.error(f"File not found: {args.file_path}")
        return
        
    input_file = args.file_path
    source_language = args.source
    target_language = args.target
    chunk_size = args.chunk_size
    output_file = args.output_file
    
    if source_language not in LANGUAGES:
        logger.error(f"Unsupported source language: {source_language}")
        return
    
    if target_language not in LANGUAGES:
        logger.error(f"Unsupported target language: {target_language}")
        return
    
    if chunk_size < 1:
        logger.error("Chunk size must be greater than 0")
        return
    
    default_dict = {}
    
    if args.default_dict:
        try:
            with open(args.default_dict) as f:
                default_dict = json.load(f)
        except Exception as e:
            logger.error(f"Error loading default dictionary: {e}")
            return
    
    file_extension = get_file_extension(input_file)
    
    if not is_supported_file(input_file):
        logger.error("Unsupported file format. Please use .csv/.txt or .xlsx files.")
        return
    
    if not args.output_file:
        output_extention = f"_{source_language}_{target_language}{file_extension}"
        output_file = input_file.replace(file_extension, output_extention)
    
    if is_csv(input_file):
        df = pd.read_csv(input_file, sep=get_separetor(args.sep))
        df = translate_csv(df, source_language, target_language, output_file, chunk_size, default_dict)
        df.to_csv(output_file, index=False)
        
    elif is_excel(file_extension):
        dfs = pd.read_excel(input_file, sheet_name=get_all_excel_sheet_names(input_file))
        translate_excel(dfs, source_language, target_language, output_file, chunk_size, default_dict)
        
    elif is_text(file_extension):
        with open(input_file, 'r') as f:
            texts = f.readlines()
        df = pd.DataFrame(texts, columns=['text'])
        df = translate_csv(df, source_language, target_language, None, chunk_size, default_dict)
        with open(output_file, 'w') as f:
            f.write('\n'.join(df['text'].tolist()))
    else:
        logger.error("Unsupported file format. Please use .csv/.txt or .xlsx files.")
        return

    
    
if __name__ == '__main__':
    main()