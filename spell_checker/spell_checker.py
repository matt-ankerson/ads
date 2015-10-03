# Author: Matt Ankerson
# Date:   29 September 2015
# The purpose of this module is to provide a spell checker for any text file.

# This iteration of my solution attempts to solve the problem using the
# Levenshtein distance algorithm. Levenshtein distance is defined
# as the min number of edits required to transform one string into the other.


class SpellChecker(object):

    class _TrieNode:

        def __init__(self):
            self.word = None
            self.children = {}

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
        # computations performed by weeding out words that the trie would
        # incorrectly consider miss-spelled.
        self.word_set = set()
        self.word_trie = self._TrieNode()           # Use trie for word map.
        self.max_cost = 1   # For our maximum Levenshtein distance / cost.
        if correct_words_filename == '':
            correct_words_filename = 'correct_words.txt'
        self.load_correct_words(correct_words_filename)

    def build_matrix(self, n, m):
        '''Build a row*col matrix.'''
        matrix = [[i for i in range(m)]]
        row = [0 for i in range(m)]
        for i in range(1, n):
            matrix.append(row[:])
            matrix[i][0] = i
        return matrix

    def calculate_distance(self, start, finish):
        '''Calculate Levenshtein distance between two words.'''
        n = len(start)
        m = len(finish)
        matrix = self.build_matrix(n + 1, m + 1)
        for i in range(1, n + 1):   # For each row
            for j in range(1, m + 1):   # For each col
                cost = int((ord(start[i - 1]) - ord(finish[j - 1])) != 0)
                v1 = matrix[i - 1][j] + 1           # deletion of a char
                v2 = matrix[i][j - 1] + 1           # insersion of a char
                v3 = matrix[i - 1][j - 1] + cost    # match or mismatch
                matrix[i][j] = min(v1, v2, v3)  # take the minimum value
        return matrix[n][m]

    def load_correct_words(self, filename):
        '''Load lines of text file at filename into the set and trie.'''
        with open(filename, 'r') as word_file:
            for line in word_file:
                word = str.strip(line)
                self.word_trie.insert(word)
                self.word_set.add(word)

    # Levenshtein distance bretween strings: 'lousy', 'google'
    #    | j- g  o  o  g  l  e
    # ------------------------
    # i- | 0  1  2  3  4  5  6
    # l  | 1  0  1  2  3  4  5
    # o  | 2  1  1  2  3  4  4
    # u  | 3  2  2  1  2  3  4
    # s  | 4  3  3  2  2  3  4
    # y  | 5  4  4  3  3  3  4 <-- this is our final cost/distance.

    def _search_recursive(self, node, letter, word, one_ago, results):
        '''Recursive function for building our Levenshtein table
        one row at a time.'''
        # Get a matrix of one row for the letter, with a column for each
        # letter in 'word'. Plus a column for the empty string at col 0.
        n_columns = len(word) + 1     # number of columns
        this_row = [one_ago[0] + 1]
        for y in xrange(1, n_columns):
            if word[y - 1] == letter:   # Cost addition for substitution.
                cost = 0
            else:
                cost = 1
            insert = this_row[y - 1] + 1
            delete = one_ago[y] + 1
            substitute = one_ago[y - 1] + cost
            # Get lowest cost
            new_entry = min(insert, delete, substitute)
            # This is where Levenshtein ends and we add an additional
            # computation to make it a Damerau-Levenshtein distance.
            this_row.append(new_entry)
        # If the last entry in the current row is less than our max cost,
        # and there is a word in this node, then add it.
        if this_row[-1] <= self.max_cost and node.word is not None:
            results.append((node.word))
        # If ANY entries in the current row are less than our cost, then
        # recur on each branch.
        if min(this_row) <= self.max_cost:
            for letter in node.children:
                self._search_recursive(node.children[letter], letter, word,
                                       this_row, results)

    def _damlev_distance(self, str1, str2):
        '''Calculate the damerau-levenshtein distance between two
        strings or any two sequences.'''
        # Get a matrix with len(str1) rows and len(str2) columns
        matrix = [[0 for c in range(len(str2))] for r in range(len(str1))]
        for a in range(0, len(str1)):
            matrix[a][0] = a
        for b in range(1, len(str2)):
            matrix[0][b] = b
        for i in xrange(1, len(str1)):
            for j in xrange(1, len(str2)):
                if str1[i] == str2[j]:
                    cost = 0
                else:
                    cost = 1
                deletion = matrix[i - 1][j] + 1
                insertion = matrix[i][j - 1] + 1
                substitute = matrix[i - 1][j - 1] + cost
                matrix[i][j] = min(deletion, insertion, substitute)
                # Transposition
                if i > 1 and j > 1 and str1[i] == str2[j - 1] and \
                        str1[i - 1] == str2[j]:
                    transpose = matrix[i - 2][j - 2] + cost
                    matrix[i][j] = min(matrix[i][j], transpose)
        return matrix[len(str1) - 1][len(str2) - 1]

    def _recur_trie_for_suggestions(self, node, target_word, results):
        # Is there a word in this node?
        # if node.word is not None:
        distance = self.max_cost + 1
        if node.word is not None:
            distance = self._damlev_distance(target_word, node.word)
        # Is this distance <= to our max distance?
        if distance <= self.max_cost:
            results.append((node.word))
        # recur down each branch of this node
        for letter in node.children:
            self._recur_trie_for_suggestions(node.children[letter],
                                             target_word, results)
        return results

    def search_word_trie(self, word):
        '''Returns a list of all words within our maximum Levenshtein
        distance to the given word.'''
        length = len(word)
        if length == 1:
            return []
        if word in self.word_set:
            return []
        # First row of distance table. 1 col for each letter, plus 1 for the
        # empty string in the first node.
        # first_row = range(len(word) + 1)
        results = []
        # Recur down each branch of the trie.
        for letter in self.word_trie.children:
            # self._search_recursive(self.word_trie.children[letter], letter,
            #                       word, first_row, results)
            self._recur_trie_for_suggestions(self.word_trie.children[letter],
                                             word, results)
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
                    if len(results) > 0:
                        yield 'Line: ' + str(line_no) + ' ' + word + ' (' + \
                            str(results).translate(None, "[]'()") + ')'
                line_no += 1

if __name__ == '__main__':
    speller = SpellChecker('correct_words.txt')
    print speller.search_word_trie('goober')
