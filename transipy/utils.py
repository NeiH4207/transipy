import re
import zipfile
import requests
import ast
from googletrans import Translator
from loguru import logger

def get_file_extension(file_path):
    return '.' + file_path.split('.')[-1]

def is_csv(file_path):
    return get_file_extension(file_path) == '.csv'

def is_excel(file_path):
    return get_file_extension(file_path) == '.xlsx'

def is_text(file_path):
    return get_file_extension(file_path) == '.txt'

def get_separetor(sep):
    if sep == 'comma':
        return ','
    elif sep == 'tab':
        return '\t'
    elif sep == 'semicolon':
        return ';'
    else:
        return ','

def get_all_excel_sheet_names(file_path, skip_list: list = []):
    sheets = []
    with zipfile.ZipFile(file_path, 'r') as zip_ref: xml = zip_ref.read("xl/workbook.xml").decode("utf-8")
    for s_tag in  re.findall("<sheet [^>]*", xml) : sheets.append(  re.search('name="[^"]*', s_tag).group(0)[6:])
    return [sheet for sheet in sheets if sheet not in skip_list]

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
            
            