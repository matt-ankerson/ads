# Author: Matt Ankerson
# Date:   5 October 2015
# The purpose of this module is to provide a spell checker for any text file.
# This solution attempts to solve the problem using the Damerau -
# Levenshtein distance algorithm. Levenshtein distance is defined as the
# minimum number of edits required to transform one string into the other.
# I came to my solution with the help of Steve Hanov's blog post:
# stevehanov.ca/blog/index.php?id=114
# And the wikipedia articles here:
# https://en.wikipedia.org/wiki/Levenshtein_distance
# https://en.wikipedia.org/wiki/Damerau-Levenshtein_distance

# Levenshtein distance bretween strings: 'lousy', 'google'
#    | j- g  o  o  g  l  e
# ------------------------
# i- | 0  1  2  3  4  5  6
# l  | 1  0  1  2  3  4  5
# o  | 2  1  1  2  3  4  4
# u  | 3  2  2  1  2  3  4
# s  | 4  3  3  2  2  3  4
# y  | 5  4  4  3  3  3  4 <-- this is our final cost/distance.


class SpellChecker(object):

    class _TrieNode:

        def __init__(self):
            self.word = None
            self.children = {}
            # For computing distance tables incrementally.
            self.second_row = None

        def insert(self, word):
            node = self
            # Address each letter in the new word
            for letter in word:
                # If there's not already a path for this letter
                if letter not in node.children:
                    # Create a (node) path for this letter
                    node.children[letter] = self.__class__()
                node = node.children[letter]  # Reassign node to the new child
            node.word = word    # Assign the whole word to this leaf node.

    def __init__(self, correct_words_filename=''):
        # Python set holds all correct words for very fast validation.
        # We're using more memory by doing this, but reducing the number of
        # computations performed and purifying results by weeding out words
        # that the trie based algoritm doesn't need to deal with.
        self.word_set = set()
        self.word_trie = self._TrieNode()           # Use trie for word map.
        self.max_cost = 2   # For our maximum Levenshtein distance / cost.
        if correct_words_filename == '':
            correct_words_filename = 'correct_words.txt'
        self.load_correct_words(correct_words_filename)

    def load_correct_words(self, filename):
        '''Load lines of text file at filename into the set and trie.'''
        with open(filename, 'r') as word_file:
            for line in word_file:
                word = str.strip(line)
                self.word_trie.insert(word)
                self.word_set.add(word)

    def _search_recursive(self, node, this_letter, prev_letter, word,
                          one_ago, two_ago, results):
        '''Recursive function for building our Levenshtein table
        one row at a time.'''
        # Get a matrix of one row for the letter, with a column for each
        # letter in 'word'. Plus a column for the empty string at col 0.
        n_columns = len(word) + 1     # number of columns
        this_row = [one_ago[0] + 1]
        for j in xrange(1, n_columns):
            if word[j - 1] == this_letter:   # Cost addition for substitution.
                cost = 0
            else:
                cost = 1
            insert = this_row[j - 1] + 1
            delete = one_ago[j] + 1
            substitute = one_ago[j - 1] + cost
            # Get lowest cost
            new_entry = min(insert, delete, substitute)
            # This is where Levenshtein ends and we add an additional
            # computation to make it a Damerau-Levenshtein distance.
            # Transposition:
            if prev_letter != '' and j > 1 and this_letter == word[j - 2] \
                    and prev_letter == word[j - 1]:
                transpose = two_ago[j - 2] + cost
                new_entry = min(new_entry, transpose)
            this_row.append(new_entry)
        # If the last entry in the current row is less than our max cost,
        # and there is a word in this node, then add it.
        if this_row[-1] <= self.max_cost and node.word is not None:
            results.append((node.word))
        # If an entry in the current row are less than our cost, then
        # recur on each branch.
        if min(this_row) <= self.max_cost:
            for letter in node.children:
                self._search_recursive(node.children[letter], letter,
                                       this_letter, word, this_row,
                                       one_ago, results)

    def _second_row(self, letter, word, one_ago):
        '''Get single Levenshtein distance row. Especially useful for
        getting the first two rows for the recursive Damerau-Levenshtein
        table building function.'''
        n_columns = len(word) + 1
        this_row = [one_ago[0] + 1]
        for j in xrange(1, n_columns):
            if word[j - 1] == letter:
                cost = 0
            else:
                cost = 1
            insert = this_row[j - 1] + 1
            delete = one_ago[j] + 1
            substitute = one_ago[j - 1] + cost
            # Get lowest cost
            this_row.append(min(insert, delete, substitute))
        return this_row

    def search_word_trie(self, word):
        '''Return a list of all words within our maximum Levenshtein
        distance to the given word, and a list of suggestions.'''
        length = len(word)
        results = []
        if length == 1:
            return []
        if word in self.word_set:
            return []
        # First row of distance table. 1 col for each letter, plus 1 for the
        # empty string in the first node.
        first_row = range(len(word) + 1)
        prev_letter = ''
        for letter in self.word_trie.children:
            # Save second rows into the child nodes.
            row = self._second_row(letter, word, first_row)
            self.word_trie.children[letter].second_row = row
        # Recur down each branch of the trie.
        for letter in self.word_trie.children:
            node = self.word_trie.children[letter]
            self._search_recursive(node, letter, prev_letter, word,
                                   node.second_row, first_row, results)
            prev_letter = letter
        return results

    def iter_spelling_on_file(self, filename):
        '''Check spelling on each word in the file at the given filename.
            Instead of returning a report, yield each scalar result.'''
        with open(filename, 'r') as word_file:
            line_no = 1
            for line in word_file:
                line = str.strip(line)
                words = line.split(' ')
                for word in words:
                    word = word.translate(None, "'!.,$#@%^&*()+=")
                    word = word.lower()
                    results = self.search_word_trie(word)
                    if len(results) > 0 or word not in self.word_set:
                        yield 'Line: ' + str(line_no) + ' ' + word + ' (' + \
                            str(results).translate(None, "[]'()") + ')'
                line_no += 1

if __name__ == '__main__':
    speller = SpellChecker('correct_words.txt')
    print speller.search_word_trie('goober')
