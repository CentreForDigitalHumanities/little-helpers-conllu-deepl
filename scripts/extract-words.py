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

#%% Create a table per language to store word translations
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
    """ Extract wordforms from a .conllu file and store them in the database.
    Store identical forms only once using ON CONFLICT DO NOTHING.
    """
    filepath = os.path.join(PROJROOT, 'data', 'UD', conllu_file)
    with open(filepath, 'r') as f:
        language = conllu_file[:2]
        table = f'wordforms_{language}'
        for sentence in conllu.parse_incr(f):
            sentence_id = sentence.metadata.get('sent_id', 'NA')
            # For ET, process only newspaper sentences (aja_ is unique to ET)
            if (sentence_id.startswith('aja') and not sentence_id.startswith(('aja_horisont', 'aja_luup'))) \
            or language != 'et':
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

#%% Create a list of .conllu files
conllu_files = []

for filename in os.listdir(os.path.join(PROJROOT, 'data', 'UD')):
    if filename.endswith('.conllu'):
        conllu_files.append(filename)

conllu_files = sorted(conllu_files)


#%% Process the conllu files and extract wordforms to database.
for conllu_file in tqdm(conllu_files):
    extract_wordforms(conllu_file)

#%% Close the database connection
conn.close()
