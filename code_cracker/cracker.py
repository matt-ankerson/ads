import string
import argparse


def possible_words(base, dictionary):
    # _ indicates missing letter.
    # + indicates letters that must be the same.
    # words in dictionary are considered to be the right length.
    # example: __z+__+
    possibles = set()
    constraints = {}
    # parse the given word,
    # build dict of constraints for fast lookup.
    for i, c in enumerate(base):
        constraints[i] = c
    # loop over the dictionary, add words which conform to our
    # constraints to the set of possible words.
    for word in dictionary:
        word_ok = True
        # loop over the word, compare against constraints.
        for i, c in enumerate(word):
            if constraints[i] == '_':
                pass
            elif constraints[i] == '+':
                # ensure other occurences of '+' match.
                for k, v in constraints.items():
                    if v == '+':
                        if word[k] != c:
                            word_ok = False
            else:
                if c != constraints[i]:
                    word_ok = False
        if word_ok:
            possibles.add(word)
    return possibles


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple program to compute" +
                                     " a list of possible words, given" +
                                     " a certain criteria")
    parser.add_argument('-b', dest='base', required=True,
                        metavar='<word>',
                        help='word with given letters, underscores as missing' +
                        ' letters and pluses as synonymous letters.')
    parser.add_argument('-d', dest='dictionary', required=True,
                        type=file, metavar='<dictionary file>',
                        help='lexicon file')
    args = parser.parse_args()

    dictionary = {
        line.strip().lower().translate(None, string.punctuation)
        for line in args.dictionary if len(line) == len(args.base) + 1}
    print possible_words(args.base, dictionary)
