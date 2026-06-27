import hashlib
import json
from pathlib import Path
from palette import (
    monochromatic,
    complementary,
    triadic
)

DATA_PATH = Path(
    "data/palettes.jsonl"
)


def load_palettes():

    palettes=[]

    with open(
        DATA_PATH,
        encoding="utf-8"
    ) as f:

        for line in f:

            palettes.append(
                json.loads(line)
            )

    return palettes


PALETTES=load_palettes()


TRANSLATIONS={

    "ночь":"night",
    "ночной":"night",

    "лес":"forest",
    "лесной":"forest",

    "деревья":"forest",

    "осень":"autumn",
    "осенний":"autumn",

    "киберпанк":"cyberpunk",

    "свобода":"freedom",

    "лето":"summer",
    "летний":"summer",

    "рассвет":"sunrise",

    "меланхоличный":"melancholy",

    "вечер":"evening"
}


def normalize(text):

    words=[]

    for word in text.lower().split():

        words.append(

            TRANSLATIONS.get(
                word,
                word
            )

        )

    return words


def similarity(
    query_words,
    tags
):

    return len(

        set(query_words)
        &
        set(tags)

    )


def deterministic_index(
    text,
    count
):

    seed=int(

        hashlib.sha256(

            text.encode()

        ).hexdigest(),

        16

    )

    return seed % count


def generate_palette(
    text:str,
    scheme:str,
    creativity:float
):

    words=normalize(text)

    scored=[]

    for palette in PALETTES:

        score=similarity(

            words,
            palette[
                "tags"
            ]
        )

        scored.append({

            "score":score,
            "palette":palette
        })


    max_score=max(

        x["score"]
        for x in scored

    )


    candidates=[

        x["palette"]

        for x in scored

        if x["score"]
        ==
        max_score

    ]


    index= deterministic_index(
        text,
        len(candidates)
    )


    chosen=candidates[index]

    base_colors=chosen[
        "colors"
    ]


    if scheme=="monochromatic":

        colors=monochromatic(
            base_colors[2]
        )

    elif scheme=="complementary":

        colors=complementary(
            base_colors[2]
        )

    elif scheme=="triadic":

        colors=triadic(
            base_colors[2]
        )

    else:

        colors=base_colors


    return [

        {

            "hex":color,
            "name":
            chosen["name"]

        }

        for color in colors

    ]