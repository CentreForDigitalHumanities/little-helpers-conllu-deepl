#%%
import os
import pathlib
import requests
from tqdm import tqdm

#%%
PROJROOT = pathlib.Path(__file__).parents[1].resolve()

#%%
""" The selected corpora to download:
https://universaldependencies.org/treebanks/et_edt/index.html
https://universaldependencies.org/treebanks/hu_szeged/index.html
https://universaldependencies.org/treebanks/tr_boun/index.html
https://universaldependencies.org/treebanks/tr_imst/index.html
"""

URLS = [
'https://github.com/UniversalDependencies/UD_Estonian-EDT/raw/r2.12/et_edt-ud-{SET}.conllu',
'https://github.com/UniversalDependencies/UD_Hungarian-Szeged/raw/r2.12/hu_szeged-ud-{SET}.conllu',
'https://github.com/UniversalDependencies/UD_Turkish-BOUN/raw/r2.12/tr_boun-ud-{SET}.conllu',
'https://github.com/UniversalDependencies/UD_Turkish-IMST/raw/r2.12/tr_imst-ud-{SET}.conllu'
]

SETS = ['dev', 'test', 'train']

urls = [url.format(SET=set) for set in SETS for url in URLS]

#%%
def download_file(url, filename):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

for url in tqdm(urls):
    filename = os.path.basename(url)
    print(f'Downloading {url}')
    download_file(url, os.path.join(PROJROOT, 'data', filename))
