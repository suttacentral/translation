import regex
from common import PO_DIR

files = (PO_DIR / 'pli-tv').glob('**/*.po')

for file in files:
    with file.open() as f:
        original_string = string = f.read()
    
    string = regex.sub(r'(?m)" +$(?<!$^)', '"', string)
    string = regex.sub(r'(?m)^(msgid|msgstr) "$', r'\1 ""', string)
    string = regex.sub(r'(?m)^(msgid|msgstr) (?!")', r'\1 "', string)
    string = regex.sub(r'(?m)^(msgctxt .*)$(?<!")', r'\1"', string)
    
    if string != original_string:
        with file.open('w') as f:
            f.write(string)
