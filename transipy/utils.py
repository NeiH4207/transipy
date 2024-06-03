import hashlib
import re
import zipfile

def get_file_extension(file_path):
    return '.' + file_path.split('.')[-1]

def is_csv(file_path):
    return get_file_extension(file_path) == '.csv'

def is_tsv(file_path):
    return get_file_extension(file_path) == '.tsv'

def is_excel(file_path):
    return get_file_extension(file_path) == '.xlsx'

def is_text(file_path):
    return get_file_extension(file_path) == '.txt'

def is_docx(file_path):
    return get_file_extension(file_path) == '.docx'

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

def is_supported_file(file_path):
    return is_csv(file_path) or is_tsv(file_path) or is_excel(file_path) or is_text(file_path) or is_docx(file_path)


def split_df_by_group(df, chunks):
    entities = df.index.unique()
    return [df[df.index.isin(entities[i::chunks])] for i in range(chunks)]

def md5hash(s: str): 
    return hashlib.md5(s.encode('utf-8')).hexdigest()