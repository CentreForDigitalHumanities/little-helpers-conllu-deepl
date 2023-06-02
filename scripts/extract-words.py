#%%
import conllu
import os
import pathlib
import sqlite3
from tqdm import tqdm

#%%
PROJROOT = pathlib.Path(__file__).parents[1].resolve()
DBPATH = os.path.join(PROJROOT, 'data', 'sentences.db')
conn = sqlite3.connect(DBPATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

#%%
def prepare_db():
    cur.execute(
    '''CREATE TABLE IF NOT EXISTS wordforms_et (
        wordform TEXT PRIMARY KEY
        , translation TEXT
        );
    ''')
    cur.execute(
    '''CREATE TABLE IF NOT EXISTS wordforms_hu (
        wordform TEXT PRIMARY KEY
        , translation TEXT
        );
    ''')
    cur.execute(
    '''CREATE TABLE IF NOT EXISTS wordforms_tr (
        wordform TEXT PRIMARY KEY
        , translation TEXT
        );
    ''')
    conn.commit()

prepare_db()

#%%
def extract_wordforms(conllu_file):
    filepath = os.path.join(PROJROOT, 'data', 'UD', conllu_file)
    with open(filepath, 'r') as f:
        language = conllu_file[:2]
        table = f'wordforms_{language}'
        for sentence in conllu.parse_incr(f):
            sentence_id = sentence.metadata.get('sent_id', 'NA')
            for word in sentence:
                if word['upos'] != 'PUNCT':
                    wordform = word['form']
                cur.execute(
                f''' INSERT INTO {table} (wordform)
                    VALUES (:wordform)
                ON CONFLICT (wordform) DO NOTHING
                ;''', {'wordform': wordform}
                )
                conn.commit()
                print(f"Processed {sentence_id}: {wordform}")
        print("Finished")

#%%
conllu_files = []

for filename in os.listdir(os.path.join(PROJROOT, 'data', 'UD')):
    if filename.endswith('.conllu'):
        conllu_files.append(filename)

conllu_files = sorted(conllu_files)


#%%
for conllu_file in tqdm(conllu_files):
    extract_wordforms(conllu_file)

#%%
conn.close()