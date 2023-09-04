# MeCab Text Cleaner

<p align="center">
  <a href="https://github.com/34j/mecab-text-cleaner/actions/workflows/ci.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/34j/mecab-text-cleaner/ci.yml?branch=main&label=CI&logo=github&style=flat-square" alt="CI Status" >
  </a>
  <a href="https://mecab-text-cleaner.readthedocs.io">
    <img src="https://img.shields.io/readthedocs/mecab-text-cleaner.svg?logo=read-the-docs&logoColor=fff&style=flat-square" alt="Documentation Status">
  </a>
  <a href="https://codecov.io/gh/34j/mecab-text-cleaner">
    <img src="https://img.shields.io/codecov/c/github/34j/mecab-text-cleaner.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">
  </a>
</p>
<p align="center">
  <a href="https://python-poetry.org/">
    <img src="https://img.shields.io/badge/packaging-poetry-299bd7?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAASCAYAAABrXO8xAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAJJSURBVHgBfZLPa1NBEMe/s7tNXoxW1KJQKaUHkXhQvHgW6UHQQ09CBS/6V3hKc/AP8CqCrUcpmop3Cx48eDB4yEECjVQrlZb80CRN8t6OM/teagVxYZi38+Yz853dJbzoMV3MM8cJUcLMSUKIE8AzQ2PieZzFxEJOHMOgMQQ+dUgSAckNXhapU/NMhDSWLs1B24A8sO1xrN4NECkcAC9ASkiIJc6k5TRiUDPhnyMMdhKc+Zx19l6SgyeW76BEONY9exVQMzKExGKwwPsCzza7KGSSWRWEQhyEaDXp6ZHEr416ygbiKYOd7TEWvvcQIeusHYMJGhTwF9y7sGnSwaWyFAiyoxzqW0PM/RjghPxF2pWReAowTEXnDh0xgcLs8l2YQmOrj3N7ByiqEoH0cARs4u78WgAVkoEDIDoOi3AkcLOHU60RIg5wC4ZuTC7FaHKQm8Hq1fQuSOBvX/sodmNJSB5geaF5CPIkUeecdMxieoRO5jz9bheL6/tXjrwCyX/UYBUcjCaWHljx1xiX6z9xEjkYAzbGVnB8pvLmyXm9ep+W8CmsSHQQY77Zx1zboxAV0w7ybMhQmfqdmmw3nEp1I0Z+FGO6M8LZdoyZnuzzBdjISicKRnpxzI9fPb+0oYXsNdyi+d3h9bm9MWYHFtPeIZfLwzmFDKy1ai3p+PDls1Llz4yyFpferxjnyjJDSEy9CaCx5m2cJPerq6Xm34eTrZt3PqxYO1XOwDYZrFlH1fWnpU38Y9HRze3lj0vOujZcXKuuXm3jP+s3KbZVra7y2EAAAAAASUVORK5CYII=" alt="Poetry">
  </a>
  <a href="https://github.com/ambv/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" alt="black">
  </a>
  <a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">
  </a>
</p>
<p align="center">
  <a href="https://pypi.org/project/mecab-text-cleaner/">
    <img src="https://img.shields.io/pypi/v/mecab-text-cleaner.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">
  </a>
  <img src="https://img.shields.io/pypi/pyversions/mecab-text-cleaner.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">
  <img src="https://img.shields.io/pypi/l/mecab-text-cleaner.svg?style=flat-square" alt="License">
</p>

This is a simple Python package for getting japanese readings (yomigana) and accents using MeCab.
Please also consider using [pyopenjtalk](https://github.com/r9y9/pyopenjtalk) (no accents) or [pyopenjtalk_g2p_prosody (ESPnet)](https://github.com/espnet/espnet/blob/5d0758e2a7063b82d1f10a8ac2de98eb6cf8a352/espnet2/text/phoneme_tokenizer.py#L103) (with accents), as this package does not account for accent changes in compound words.

## Installation

Install this via pip or pipx (or your favourite package manager):

```shell
pipx install mecab-text-cleaner[unidecode,unidic]
```

```shell
pip install mecab-text-cleaner[unidecode,unidic]
```

## Usage

```shell
> mtc いい天気ですね。
イ]ー テ]ンキ デス ネ。
> mtc いい天気ですね。 --ascii
i] te]nki desu ne.
> mtc いい天気ですね --no-add-atype --no-add-blank-between-words
イーテンキデスネ
> mtc いい天気ですね --no-add-atype --no-add-blank-between-words -r kana
イイテンキデスネ
```

```python
from mecab_text_cleaner import to_reading, to_ascii_clean

assert to_reading("     空、雲。\n雨！（") == "ソ]ラ、 ク]モ。\nア]メ！（"
assert to_ascii_clean("      한空、雲。\n雨！（") == "han so]ra, ku]mo. \na]me!("
```

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- prettier-ignore-start -->
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- markdownlint-disable -->
<!-- markdownlint-enable -->
<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- prettier-ignore-end -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
