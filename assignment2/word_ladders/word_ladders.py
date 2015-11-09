

class WordLadderSolver(object):

    def __init__(self):
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self.legal_words = set()
        self.graph = {}
        with open('dictionary.txt', 'r') as f:
            for word in [line.rstrip('\n') for line in f]:
                self.legal_words.add(word)

    def direct_derivs(self, word):
        '''yield valid words with 1 char difference to word.'''
        for i, c in enumerate(word):
            for x in self.alphabet:
                if x == c:
                    pass
                else:
                    new_word = word[:i] + x + word[i + 1:]
                    if new_word in self.legal_words:
                        yield new_word

    def solve(self, start, end):
        self.graph = {}

if __name__ == '__main__':
    solver = WordLadderSolver()
