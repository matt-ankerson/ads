from itertools import permutations

# Author: Matt Ankerson
# Date:   29 September 2015
# The purpose of this module is to provide a spell checker for any text file.


class SpellChecker(object):

    def __init__(self, correct_words_filename=''):
        self.correct_words = set()
        self.alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyv'
        self.word_map = {}
        if correct_words_filename == '':
            correct_words_filename = 'correct_words.txt'
        self.load_correct_words(correct_words_filename)

    def build_word_map(self):
        '''Create the dict that maps incorrectly spelled words to sets
            of potential matches (correctly spelled words).'''
        if len(self.correct_words) == 0:
            raise ValueError('Correct words not yet loaded.')
        for word in self.correct_words:
            # Get a set of incorrectly spelled versions of word.
            bad_words = self.derive_bad_spelling(word)
            for bad_word in bad_words:
                # Create a new entry in the word map dict if required.
                try:
                    self.word_map[bad_word].add(word)
                except:
                    self.word_map[bad_word] = set()

    def load_correct_words(self, filename):
        '''Load lines of given text file at filename into the set.'''
        with open(filename, 'r') as word_file:
            for line in word_file:
                self.correct_words.add(str.strip(line))

    def check_word(self, word):
        '''Assess whether or not the given word is correct.'''
        return word in self.correct_words

    def derive_bad_spelling(self, correct_word):
        '''Return a set of possible miss-spellings.'''
        if not self.check_word(correct_word):
            raise ValueError('Not a correct word')
        bad_words = set()
        # Permutation (arrangement)
        bad_words = bad_words.union(set([''.join(p)
                                         for p in permutations(correct_word)]))
        # Position based
        for i in range(len(correct_word) + 1):
            for c in self.alph:
                # Incorrect substitution.
                bad_words.add(correct_word[:i] + c + correct_word[i+1:])
                # Inserting unwanted chars.
                bad_words.add(correct_word[:i] + c + correct_word[i:])
        # Missing letters.
        for c in correct_word:
            bad_words.add(correct_word.translate(None, ''.join(c)))
            # str.translate is not the best choice here.
        return bad_words

if __name__ == '__main__':
    speller = SpellChecker()
    speller.build_word_map()
    for item in speller.word_map:
        print item
