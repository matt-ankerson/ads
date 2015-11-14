from queue import Queue


class WordLadderSolver(object):

    def __init__(self):
        self.unprocessed_q = Queue()
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self.ladder_dict = {}
        self.legal_words = set()
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
                    if new_word in self.legal_words and\
                            new_word not in self.ladder_dict:
                        yield new_word

    def solve(self, start, end):
        # put start word in queue.
        self.unprocessed_q.enqueue(start)
        check_end = start
        self.ladder_dict[start] = None
        # loop until queue is empty.
        while not self.unprocessed_q.is_empty() and check_end != end:
            # pop the next word from the queue.
            next_word = self.unprocessed_q.dequeue()
            # add derivs of next_word to queue.
            for deriv in self.direct_derivs(next_word):
                self.unprocessed_q.enqueue(deriv)
                self.ladder_dict[deriv] = next_word
            check_end = next_word
        # did we find a path to the end word?
        if check_end == end:
            # return the path.
            path = [end]
            next_key = self.ladder_dict[end]
            while next_key is not None:
                path.append(next_key)
                next_key = self.ladder_dict[next_key]
            return path
        else:
            return 'No path found.'

if __name__ == '__main__':
    solver = WordLadderSolver()
    output = solver.solve('baldy', 'wonky')
    print output
