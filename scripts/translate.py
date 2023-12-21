#%%
import deepl
import os
import pathlib
import sqlite3
from tqdm import tqdm

#%% Database connection
PROJROOT = pathlib.Path(__file__).parents[1].resolve()
DBPATH = os.path.join(PROJROOT, 'data', 'sentences.db')
conn = sqlite3.connect(DBPATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

#%% Enter your DeepL authentication key
auth_key = input('DeepL Authentication Key: ')

#%% DeepL translator instance
translator = deepl.Translator(auth_key)

#%%
# for language in translator.get_source_languages():
#     print(f"{language.code}: {language.name}")

#%%
def translate_sentence(sentence_id, sentence, language):
    """ Translate a sentence from the given language to English,
    and store it in the database.
    """
    translation = translator.translate_text(sentence, source_lang=language, target_lang="EN-GB")
    print(language, ': ', sentence_id, ': ', translation.text)
    cur.execute(
        '''UPDATE sentences
        SET sentence_text_translation = ?
        WHERE sentence_id = ?
        ''', (translation.text, sentence_id)
        )

    conn.commit()

#%% Create a list of sentence row objects to translate
sentences_to_translate = cur.execute(
    '''SELECT s.sentence_id, s.sentence_text, cf."language"
    FROM sentences s
    JOIN corpus_files cf
     ON cf.corpus_file = s.corpus_file
    WHERE s.sentence_text_translation IS NULL;
    ''').fetchall()

#%% Translate the sentences
for row in tqdm(sentences_to_translate):
    translate_sentence(row['sentence_id'], row['sentence_text'], row['language'])

#%% Close the database connection
conn.close()
