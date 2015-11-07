def fizz_buzz():
    for x in xrange(1, 101):
        if x % 15 == 0:
            print 'FizzBuzz'
        elif x % 3 == 0:
            print 'Fizz'
        elif x % 5 == 0:
            print 'Buzz'
        else:
            print x

if __name__ == '__main__':
    fizz_buzz()
