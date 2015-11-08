import redblack_treemap


class InvertedFile(object):

    def __init__(self):
        self.wordmap = redblack_treemap.RedBlackTreeMap()

    def construct_wordmap(self, document):
        # document is assumed to be a list of unordered, numbered words.
        for i in xrange(0, len(document)):
            try:
                # try append this index to this word's list of indices.
                self.wordmap[document[i]].append(i)
            except KeyError:
                # initiate the list of indices for this word.
                self.wordmap[document[i]] = [i]

    def __repr__(self):
        display = '{ '
        for item in self.wordmap:
            display += str(item.key()) + ': '
            display += str(item.value()) + ', '
        return display[:-2] + ' }'

if __name__ == '__main__':
    invertedfile = InvertedFile()
    document = ['the', 'quick', 'brown', 'fox', 'jumped', 'over',
                'the', 'lazy', 'dog']
    invertedfile.construct_wordmap(document)
    print invertedfile
