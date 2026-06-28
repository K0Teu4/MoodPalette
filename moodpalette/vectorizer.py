import math


def tokenize(text: str):

    return text.lower().split()


def build_vocab(palettes):

    vocab = set()

    for p in palettes:

        for tag in p["tags"]:
            vocab.add(tag)

        for color in p["colors"]:
            vocab.add(color)

    return list(vocab)


def vectorize(tokens, vocab):

    vec = [0.0] * len(vocab)

    for t in tokens:

        for i, v in enumerate(vocab):

            if t == v:
                vec[i] += 2.0

            elif t in v or v in t:
                vec[i] += 0.5

    # normalize
    norm = math.sqrt(sum(x * x for x in vec))

    if norm == 0:
        return vec

    return [x / norm for x in vec]


def cosine(a, b):

    return sum(x * y for x, y in zip(a, b))