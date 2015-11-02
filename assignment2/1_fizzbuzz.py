def fizz_buzz():
    for x in xrange(1, 101):
        if x % 3 == 0 and x % 5 == 0:
            yield 'FizzBuzz'
        elif x % 3 == 0:
            yield 'Fizz'
        elif x % 5 == 0:
            yield 'Buzz'
        else:
            yield x

if __name__ == '__main__':
    for x in fizz_buzz():
        print x
