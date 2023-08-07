import glob
import os.path

ids = []
with open('../tokenizer/ids.txt', 'r', encoding='utf8') as f:
    for linea in f.readlines():
        ids.append(linea.strip('\n'))

for f in glob.glob('./html/*.html'):
    if os.path.basename(f)[:-4] not in ids:
        os.remove(f)

