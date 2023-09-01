from __future__ import annotations

import re
import warnings
from logging import getLogger
from typing import Callable, Literal, NamedTuple

import fugashi

LOG = getLogger(__name__)


class UnidicFeatures17(NamedTuple):
    """https://clrd.ninjal.ac.jp/unidic/faq.html
    https://clrd.ninjal.ac.jp/unidic/UNIDIC_manual.pdf"""

    # ChaSen品詞体系
    pos1: str
    """品詞大分類(ChaSen品詞体系)"""
    pos2: str
    """品詞中分類(ChaSen品詞体系)"""
    pos3: str
    """品詞小分類(ChaSen品詞体系)"""
    pos4: str
    """品詞細分類(ChaSen品詞体系)"""

    # 語彙素
    lForm: str
    """語彙素読み

    語彙素見出し（カタカナ表記）"""
    lemma: str
    """語彙素(+語彙素細分類)

    語彙素見出し（漢字仮名混じり表記）"""
    goshu: str
    """語種

    語種の名称"""

    # 語形
    cType: str
    """活用型

    活用の種類（型）"""
    cForm: str
    """活用形

    活用の形"""
    iType: str
    """語頭変化型

    語頭音変化の種類（型）"""
    iForm: str
    """語頭変化形

    語頭音変化の形"""
    fType: str
    """語末変化型

    語末音変化の種類（型）"""
    fForm: str
    """語末変化形

    語末音変化の形"""

    # 書字形
    orth: str
    """書字形出現形

    書字形基本形が活用変化を受けたもの"""
    orthBase: str
    """書字形基本形

    書字形見出し"""

    # 発音形
    pron: str
    """発音形出現形

    発音形基本形が活用変化を受けたもの"""
    pronBase: str
    """発音形基本形

    発音形見出し"""


class UnidicFeatures26(UnidicFeatures17):
    kana: str
    """仮名形出現形

    書字形基本形をカタカナ表記にしたもの"""
    kanaBase: str
    """仮名形基本形

    書字形出現形をカタカナ表記にしたもの"""
    form: str
    """語形出現形

    語形が活用変化を受けたもの"""
    formBase: str
    """語形基本形

    語形見出し"""
    iConType: str
    """語頭変化結合型

    後続要素の語頭変化形への制約の種類（型）"""
    fConType: str
    """語末変化結合型"""
    aType: str
    """アクセント型

    アクセント核の位置"""
    aConType: str
    """アクセント結合型

    前接（後続）要素との結合時のアクセント変化の種類（型）"""
    aModType: str
    """アクセント修飾型

    活用によるアクセント変化の種類（型）"""


class UnidicFeatures29(UnidicFeatures26):
    type: str
    """品詞"""
    lid: str
    """語彙表ID"""
    lemma_id: str
    """語彙素ID"""


def to_reading(
    text: str,
    reading_type: Literal["orth", "pron", "kana"] = "pron",
    add_atype: bool = True,
    add_blank_between_words: bool = True,
    when_unknown: Literal["passthrough", "*", "unidecode"]
    | Callable[[str], str] = "passthrough",
    tagger: fugashi.Tagger = fugashi.Tagger(),
) -> str:
    """Convert text to reading.
    Note that MeCab interprets spaces as word boundaries, and will be removed.
    Lines (\\n only) are restored later.

    Parameters
    ----------
    text : str
        The text to convert.
    reading_type : Literal[&quot;orth&quot;, &quot;pron&quot;,
    &quot;kana&quot;], optional
        Reading type, by default "pron"
        "pron" is the pronunciation (発音形), "orth" is the orthography (書字形),
        "kana" is the kana(仮名) form of orthography
    add_atype : bool, optional
        Whether to consider aType (アクセント型) and add "]" to the reading, by default True
    add_blank_between_words : bool, optional
        Whether to add a blank between words, by default True
    when_unknown : Literal[&quot;passthrough&quot;, , optional
        What to do when the reading is unknown ("補助記号" and "一般"),
        by default "passthrough"
        "passthrough" will pass the original text,
        "*" will pass "*", "unidecode" will use unidecode,
        and a callable will be called with the original text
    tagger : fugashi.Tagger, optional
        The tagger to use, by default fugashi.Tagger()

    Returns
    -------
    str
        The reading

    Raises
    ------
    ImportError
        When when_unknown="unidecode" and unidecode is not installed

    Examples
    --------
    >>> from mecab_text_cleaner import to_reading
    >>> to_reading("     空、雲。\\n雨！（")
    'ソ]ラ、 ク]モ。\\nア]メ！（'
    """
    if when_unknown == "unidecode":
        # check unidecode first
        import unidecode

    res = ""

    for line in text.splitlines():
        for word in tagger(line):
            LOG.debug(f"word={word}, feature={word.feature}")
            reading = getattr(word.feature, reading_type)

            if reading in ("*", None):
                # unknown reading
                if not (word.feature.pos1 == "補助記号" and word.feature.pos2 == "一般"):
                    # known symbol
                    if add_blank_between_words:
                        res = res[:-1]
                    res += word.surface
                # unknown symbol
                elif when_unknown == "passthrough":
                    res += word.surface
                elif when_unknown == "*":
                    res += "*"
                elif when_unknown == "unidecode":
                    res += unidecode.unidecode(word.surface)
                elif callable(when_unknown):
                    res += when_unknown(word.surface)
                else:
                    raise ValueError(
                        f"when_unknown={when_unknown} is not supported"
                    )  # pragma: no cover

                # add blank between words
                if add_blank_between_words:
                    res += " "
                continue

            # known reading
            if (
                add_atype
                and word.feature.aType is not None
                and word.feature.aType.isdigit()
            ):
                # aType is number
                aType = int(word.feature.aType)

                if aType == 0:
                    reading += "="
                elif aType <= len(reading):
                    reading = reading[:aType] + "]" + reading[aType:]
                else:
                    warnings.warn(
                        f"aType={aType} is too large for reading={reading} "
                        f"of len={len(reading)}, ignoring",
                        RuntimeWarning,
                    )  # pragma: no cover
            else:
                # no aType
                pass
            res += reading

            # add blank between words
            if add_blank_between_words:
                res += " "

        # remove last blank
        if add_blank_between_words:
            res = res[:-1]

        # add newline
        res += "\n"

    # remove last newline
    return res[:-1]


def to_ascii_clean(
    text: str,
    reading_type: Literal["orth", "pron", "kana"] = "pron",
    add_atype: bool = True,
    add_blank_between_words: bool = True,
    tagger: fugashi.Tagger = fugashi.Tagger(),
    remove_multiple_spaces: bool = True,
) -> str:
    """Convert text to reading, then to ascii.

    Parameters
    ----------
    text : str
        The text to convert.
    reading_type : Literal[&quot;orth&quot;, &quot;pron&quot;,
    &quot;kana&quot;], optional
        Reading type, by default "pron"
        "pron" is the pronunciation (発音形), "orth" is the orthography (書字形),
        "kana" is the kana(仮名) form of orthography
    add_atype : bool, optional
        Whether to consider aType (アクセント型) and add "]" to the reading, by default True
    add_blank_between_words : bool, optional
        Whether to add a blank between words, by default True
    when_unknown : Literal[&quot;passthrough&quot;, , optional
        What to do when the reading is unknown ("補助記号" and "一般"),
        by default "passthrough"
        "passthrough" will pass the original text,
        "*" will pass "*", "unidecode" will use unidecode,
        and a callable will be called with the original text
    tagger : fugashi.Tagger, optional
        The tagger to use, by default fugashi.Tagger()
    remove_multiple_spaces : bool, optional
        Whether to remove multiple spaces created by unidecode, by default True

    Returns
    -------
    str
        The ascii-cleaned text

    Raises
    ------
    ImportError
        When unidecode is not installed

    Examples
    --------
    >>> from mecab_text_cleaner import to_reading
    >>> to_reading("     空、雲。\\n雨！（")
    'so]ra, ku]mo. \\na]me!('
    """
    import unidecode

    text = unidecode.unidecode(
        to_reading(
            text,
            reading_type=reading_type,
            add_atype=add_atype,
            add_blank_between_words=add_blank_between_words,
            when_unknown="passthrough",
            tagger=tagger,
        )
    )
    if remove_multiple_spaces:
        text = re.sub(r" +", " ", text)
    return text
