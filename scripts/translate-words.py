#%%
import deepl
import os
import pathlib
import sqlite3
from tqdm import tqdm

#%%
PROJROOT = pathlib.Path(__file__).parents[1].resolve()
DBPATH = os.path.join(PROJROOT, 'data', 'sentences.db')
conn = sqlite3.connect(DBPATH)
cur = conn.cursor()

#%%
auth_key = input('DeepL Authentication Key: ')

#%%
translator = deepl.Translator(auth_key)

#%%
def translate_word(word, language):
    translation = translator.translate_text(word, source_lang=language, target_lang="EN-GB")
    if isinstance(translation, list):
        translated = '; '.join([t.text for t in translation])
    elif isinstance(translation, deepl.translator.TextResult):
        translated = translation.text
    else:
        raise TypeError("Translation is not a (list of) deepl.translator.TextResult object(s)")
    table = f'wordforms_{language.lower()}'
    print(language, ': ', table, '; ', word, ': ', translated)
    cur.execute(
        f'''UPDATE {table}
        SET translation = ?
        WHERE wordform = ?
        ''', (translated, word)
        )
    conn.commit()

#%%
def get_words_to_translate(table):
    words_to_translate = cur.execute(
    f'''SELECT wordform
    FROM {table}
    WHERE translation IS NULL;
    ''').fetchall()
    return words_to_translate

#%%
# et words characters: 438171 (newspaper)
# hu words characters: 123676
# tr words characters: 420612
chars_sum = 0
for lang in ['et', 'hu', 'tr']:
    table = f'wordforms_{lang}'
    words_to_translate = get_words_to_translate(table)
    for word in tqdm(words_to_translate):
        wordform = word[0]
        translate_word(wordform, lang)
        chars_sum += len(wordform)
        if chars_sum >= 500000: # 500000
            break
    if chars_sum >= 500000: # 500000
        break

#%%
conn.close()
print("Finished!")
