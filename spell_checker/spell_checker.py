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
        self.word_trie = self._TrieNode()          # Use trie for word map.
        self.word_map = {}
        self.max_cost = 2   # For our maximum Levenshtein distance / cost.
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
                v1 = matrix[i - 1][j] + 1
                v2 = matrix[i][j - 1] + 1
                v3 = matrix[i - 1][j - 1] + cost
                matrix[i][j] = min(v1, v2, v3)  # take the minimum value
        return matrix[n][m]

    def load_correct_words(self, filename):
        '''Load lines of text file at filename into the trie.'''
        with open(filename, 'r') as word_file:
            for line in word_file:
                word = str.strip(line)
                self.word_trie.insert(word)

    def _search_recursive(self, node, letter, word, prev_row, results):
        '''Recursive function for building our Levenshtein table
        one row at a time.'''
        # Get a matrix of one row for the letter, with a column for each
        # letter in 'word'. Plus a column for the empty string at col 0.
        n_columns = len(word) + 1     # number of columns
        cur_row = [prev_row[0] + 1]
        for column_no in xrange(1, n_columns):
            insert_cost = cur_row[column_no - 1] + 1    # v1
            delete_cost = prev_row[column_no] + 1       # v2
            # If previous letter in word is not 'letter'
            if word[column_no - 1] != letter:
                replace_cost = prev_row[column_no - 1] + 1  # v3
            else:   # previous letter in word is 'letter'
                replace_cost = prev_row[column_no - 1]      # v3
            # Get lowest cost
            new_col = min(insert_cost, delete_cost, replace_cost)
            cur_row.append(new_col)
        # If the last entry in the current row is less than 2,
        # and there is a word in this node, then add it.
        if cur_row[-1] <= self.max_cost and node.word is not None:
            results.append((node.word, cur_row[-1]))
        # If ANY entries in the current row are less than our cost, then
        # recur on each branch.
        if min(cur_row) <= self.max_cost:
            for letter in node.children:
                self._search_recursive(node.children[letter], letter, word,
                                       cur_row, results)

    def search_word_trie(self, word):
        '''Returns a list of all words within our maximum Levenshtein
        distance to the given word.'''
        # First row of distance table. 1 col for each letter, plus 1 for the
        # empty string in the first node.
        cur_row = range(len(word) + 1)
        results = []
        # Recur down each branch of the trie.
        for letter in self.word_trie.children:
            self._search_recursive(self.word_trie.children[letter], letter,
                                   word, cur_row, results)
        return results

    def check_spelling(self, word):
        '''Perform spell check and offer suggestions.'''
        errors = []     # Build list of errors
        length = len(word)
        if length == 1:
            return None
        if word in self.word_map[length]:
            return None
        selected_set = self.word_map[length].union(self.word_map[length + 1])
        for w in selected_set:
            distance = self.calculate_distance(word, w)
            if distance < 2:    # 2 is our maximum cost.
                errors.append(w)
        return errors

    def check_spelling_on_file(self, filename):
        '''Check spelling on each word in the file at the filename.'''
        output = ''
        with open(filename, 'r') as word_file:
            line_no = 1
            for line in word_file:
                line = str.strip(line)
                words = line.split(' ')
                for word in words:
                    word = word.translate(None, "'!.,$#@%^&*()+=")
                    word = word.lower()
                    result = self.check_spelling(word)
                    if result is not None:
                        output += '\n' + str(line_no) + ' ' + \
                            word + ' (' + str(result) + ')'
                line_no += 1
        return output

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
                    result = self.check_spelling(word)
                    if result is not None:
                        yield 'Line: ' + str(line_no) + ' ' + word + ' (' + \
                            str(result).translate(None, "[]'") + ')'
                line_no += 1

if __name__ == '__main__':
    speller = SpellChecker('correct_words.txt')
    print speller.search_word_trie('goober')
    # print speller.check_spelling_on_file('test_doc.txt')
