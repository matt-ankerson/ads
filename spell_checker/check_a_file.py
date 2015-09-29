# This script exercises a plugin spelling checker.
# A filename is given at the command line, the file is then
# searched for errors and the results printed in stdout.
from spell_checker import SpellChecker

speller = SpellChecker()
filename = raw_input('File to check: ')
if filename is None or filename == '':
    filename = 'test_doc.txt'
    print 'Using default test file...\n'

for mistake in speller.iter_spelling_on_file(filename):
    print mistake

print 'Done!'
