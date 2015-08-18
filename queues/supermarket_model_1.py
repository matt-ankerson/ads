from queue import Queue
from customer import Customer
import random as r

# Author: Matt Ankerson
# Date: 15 August 2015

# This script models queue behaviour at a supermarket.
# The scenario is: 10 checkouts, a customer selects a checkout at random.

class SuperMarket(object):
    
    def __init__(self):
        r.seed()
        self.n_customers = 0
        self.done = False
        self.time_taken = 0
        self.checkouts = []
        for k in range(10):     # build list of checkout queues
            q = Queue()
            self.checkouts.append(q)
    
    def add_customer(self):
        # randomly assign a new customer to a queue
        c = Customer(r.randint(1, 5))
        self.checkouts[r.randint(0, 9)].enqueue(c)
        self.n_customers += 1       # increment n_customers
        
    def clock_a_minute(self):
        self.time_taken += 1
        # add a customer every two minutes.
        if self.n_customers <= 1000 and self.time_taken % 2 == 0:
            self.add_customer()
        # decrement time required for the people at the head of each queue
        for checkout in self.checkouts:
            if not checkout.is_empty(): 
                # decrement time left for the first customer
                checkout.first().checkout_time -= 1
                if checkout.first().checkout_time <= 0:
                    # if the customer has finished, pull them off the queue
                    checkout.dequeue()
        # assess whether or not we have customers left to deal with
        self.done = self.queues_empty()

    def queues_empty(self):
        # check to ensure that we've still got customers to deal with
        empty = True
        if self.n_customers < 1000:
            empty = False
        else:
            for checkout in self.checkouts:
                if not checkout.is_empty():
                    empty = False
        return empty
        
if __name__ == "__main__":
    
    print("Random Queue Assignment: ")
    soup = SuperMarket()
    while not soup.done:
        soup.clock_a_minute()
    print("Time taken: " + str(soup.time_taken))
    
    