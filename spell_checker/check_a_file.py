# This script exercises a plugin spelling checker.
# A filename is given at the command line, the file is then
# searched for errors and the results printed in stdout.
from spell_checker import SpellChecker

print 'This file uses a dictionary of known words to check a text file ' + \
    'for spelling. Supply paths to these files or press enter for defaults.\n'

known_words = raw_input('Filename or path to dictionary of known words: ')
print 'Loading trie from dictionary file...'

if known_words is None or known_words == '':
    known_words = 'words.txt'
speller = SpellChecker(known_words)
filename = raw_input('File to check: ')
if filename is None or filename == '':
    filename = 'test_doc.txt'
    print 'Using default test file...\n'

for mistake in speller.iter_spelling_on_file(filename):
    print mistake

print '\nDone!'
