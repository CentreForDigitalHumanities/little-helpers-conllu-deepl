#%%
import conllu
import os
import pathlib
from tqdm import tqdm

#%% Create a list of .conllu files
PROJROOT = pathlib.Path(__file__).parents[1].resolve()
conllu_files = []
for filename in os.listdir(os.path.join(PROJROOT, 'data', 'UD')):
    if filename.endswith('.conllu'):
        conllu_files.append(filename)

conllu_files = sorted(conllu_files)
conllu_files

#%%
def process(filename):
    """ Read a conllu file and iterate over the sentences.
    If the sentence belongs to a newspaper collection, write it
    to a combined file per corpus"""
    filepath = os.path.join(PROJROOT, 'data', 'UD', filename)
    language = filename[:2]
    basename = os.path.splitext(filename)[0]
    ud_proj = basename
    for suffix in ['-dev', '-test', '-train']:
        ud_proj = ud_proj.removesuffix(suffix)
    ud_proj_combined = f'{ud_proj}-combined.conllu'
    ud_proj_combined_fp = os.path.join(PROJROOT, 'data', 'processed', ud_proj_combined)
    with open(filepath, 'r') as f, open(ud_proj_combined_fp, 'a') as outfile:
        for sentence in conllu.parse_incr(f):
            sentence_id = sentence.metadata.get('sent_id', 'NA')
            if language == 'et':
                # ET Newspaper sentences start with 'aja_', excluding 'aja_horisont' and 'aja_luup'
                if (sentence_id.startswith('aja_') and not sentence_id.startswith(('aja_horisont', 'aja_luup'))):
                    outfile.write(sentence.serialize())
            if language == 'tr':
                # TR Newspaper sentences start with 'news_'
                if sentence_id.startswith('news_'):
                    outfile.write(sentence.serialize())
            if language == 'hu':
                # HU consists of only news corpora?
                outfile.write(sentence.serialize())

#%% Create a combined file per corpus of only newspaper sentences
for conllu_file in tqdm(conllu_files):
    process(conllu_file)
