from mecab_text_cleaner import to_ascii_clean, to_reading


def test_simple():
    assert to_reading("雲") == "ク]モ"


def test_complex():
    assert to_reading(" 1한.    局長、武蔵 小杉に向かう。") == "1 한. キョクチョー=、 ム]サシ コスギ ニ ムカウ=。"


def test_multiline():
    assert to_reading("     한空、雲。\n雨！（") == "한 ソ]ラ、 ク]モ。\nア]メ！（"


def test_multiline_noatype():
    assert to_reading("     한空、雲。\n雨！（", add_atype=False) == "한 ソラ、 クモ。\nアメ！（"


def test_multiline_noblank():
    assert (
        to_reading("     한空、雲。\n雨！（", add_blank_between_words=False)
        == "한ソ]ラ、ク]モ。\nア]メ！（"
    )


def test_multiline_unidecode():
    assert (
        to_reading("     한空、雲。\n雨！（", when_unknown="unidecode")
        == "han ソ]ラ、 ク]モ。\nア]メ！（"
    )


def test_multiline_star():
    assert to_reading("     한空、雲。\n雨！（", when_unknown="*") == "* ソ]ラ、 ク]モ。\nア]メ！（"


def test_multiline_custom():
    assert (
        to_reading("     한空、雲。\n雨！（", when_unknown=lambda x: x + x)
        == "한한 ソ]ラ、 ク]モ。\nア]メ！（"
    )


def test_to_ascii():
    assert to_ascii_clean("      한空、雲。\n雨！（") == "han so]ra, ku]mo. \na]me!("


def test_to_ascii_2():
    assert (
        to_ascii_clean("     한空、雲。\n雨！（", remove_multiple_spaces=False)
        == "han so]ra,  ku]mo. \na]me!("
    )
