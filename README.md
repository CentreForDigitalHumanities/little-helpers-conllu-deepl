# Little helpers for conllu and DeepL

This repository contains a few Python functions for some one-off tasks with `.conllu` files and fetching [DeepL](https://www.deepl.com/) translations.

- For parsing and writing .conllu files, [conllu](https://github.com/EmilStenstrom/conllu) is used.
- DeepL translations are fetched using the [DeepL Python package](https://github.com/DeepLcom/deepl-python).
- Extracted and translated sentences and words are stored in a SQLite database.


## Notes

    virtualenv ~/.virtualenvs/conllu-deepl --prompt="(conllu-deepl) "
    source ~/.virtualenvs/conllu-deepl/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt

Scripts containing blocks marked with `#%%` can be run interactively in VSCode.
