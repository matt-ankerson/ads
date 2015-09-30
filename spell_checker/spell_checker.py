# Author: Matt Ankerson
# Date:   29 September 2015
# The purpose of this module is to provide a spell checker for any text file.

# This iteration of my solution attempts to solve the problem using the
# Levenshtein distance algorithm. Levenshtein distance is defined
# as the min number of edits required to transform one string into the other.


class SpellChecker(object):

    def __init__(self, correct_words_filename=''):
        self.word_map = {}          # Dictionary for word map.
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
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                cost = int((ord(start[i - 1]) - ord(finish[j - 1])) != 0)
                v1 = matrix[i - 1][j] + 1
                v2 = matrix[i][j - 1] + 1
                v3 = matrix[i - 1][j - 1] + cost
                matrix[i][j] = min(v1, v2, v3)  # take the minimum value
        return matrix[n][m]

    def load_correct_words(self, filename):
        '''Load lines of text file at filename into the dict. Word lengths
            serve as keys, to the corresponding words of those lengths'''
        with open(filename, 'r') as word_file:
            for line in word_file:
                word = str.strip(line)
                length = len(word)
                if length not in self.word_map:
                    self.word_map[length] = set()
                self.word_map[length].add(word)

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
    print speller.check_spelling_on_file('test_doc.txt')
