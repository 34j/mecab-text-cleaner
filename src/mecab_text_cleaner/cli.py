from typing import Literal

import click

from . import to_ascii_clean, to_reading


@click.command()
@click.argument("text", type=str)
@click.option("-a/-rd", "--ascii/--reading", default=False)
@click.option(
    "-r", "--reading-type", type=click.Choice(["orth", "pron", "kana"]), default="pron"
)
@click.option("-at/-nat", "--add-atype/--no-add-atype", default=True)
@click.option(
    "-b/-nb", "--add-blank-between-words/--no-add-blank-between-words", default=True
)
@click.option(
    "-u",
    "--when-unknown",
    type=click.Choice(["passthrough", "*", "unidecode"]),
    default="passthrough",
)
@click.option(
    "-rs/-nrs", "--remove-multiple-spaces/--no-remove-multiple-spaces", default=True
)
def main(
    text: str,
    ascii: bool = False,
    reading_type: Literal["orth", "pron", "kana"] = "pron",
    add_atype: bool = True,
    add_blank_between_words: bool = True,
    when_unknown: Literal["passthrough", "*", "unidecode"] = "passthrough",
    remove_multiple_spaces: bool = True,
) -> None:
    if ascii:
        text = to_ascii_clean(text, remove_multiple_spaces=remove_multiple_spaces)
    else:
        text = to_reading(
            text,
            reading_type=reading_type,
            add_atype=add_atype,
            add_blank_between_words=add_blank_between_words,
            when_unknown=when_unknown,
        )
    click.echo(text)
