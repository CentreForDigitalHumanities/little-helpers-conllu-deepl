#%%
import conllu
import os
import pathlib
import sqlite3
from tqdm import tqdm

#%% SQLite database connection
PROJROOT = pathlib.Path(__file__).parents[1].resolve()
DBPATH = os.path.join(PROJROOT, 'data', 'sentences.db')
conn = sqlite3.connect(DBPATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

#%% Create table structures
def prepare_db():
    cur.execute(
    '''CREATE TABLE IF NOT EXISTS corpus_files (
        corpus_file TEXT PRIMARY KEY
        , language TEXT
        );
    ''')
    cur.execute(
    '''CREATE TABLE IF NOT EXISTS sentences (
        corpus_file TEXT REFERENCES corpus_files(corpus_file)
        , sentence_id TEXT PRIMARY KEY
        , sentence_text TEXT
        , sentence_text_translation TEXT
        );
    ''')
    conn.commit()

prepare_db()

#%% Create a list of .conllu files
conllu_files = []

for filename in os.listdir(os.path.join(PROJROOT, 'data')):
    if filename.endswith('.conllu'):
        conllu_files.append(filename)

conllu_files = sorted(conllu_files)

#%% Store corpus filename with language code
for filename in conllu_files:
    filename = filename.removesuffix('.conllu')
    # DeepL uses ISO 639-1 codes
    language = filename[:2].upper()
    cur.execute(
    '''INSERT INTO corpus_files (corpus_file, language)
    VALUES (:filename, :language)
    ON CONFLICT (corpus_file) DO UPDATE SET language = :language;
    ''', {'filename': filename, 'language': language}
    )

conn.commit()

#%%
def extract_sentences(conllu_file):
    """ Extract sentences from a .conllu file and store them in the database"""
    filename = os.path.basename(conllu_file)
    basename = os.path.splitext(filename)[0]

    with open(conllu_file, 'r') as f:
        for sentence in conllu.parse_incr(f):
            cur.execute(
            '''INSERT INTO sentences (
                corpus_file
                , sentence_id
                , sentence_text
                )
            VALUES (?, ?, ?)
            ON CONFLICT (sentence_id) DO NOTHING;
            ''', (basename, sentence.metadata['sent_id'], sentence.metadata['text']))

    conn.commit()

#%% Process the list of conllu files and extract sentences to database.
for filename in tqdm(conllu_files):
    conllu_file = os.path.join(PROJROOT, 'data', filename)
    print(filename)
    extract_sentences(conllu_file)

#%% Close the database connection
conn.close()
