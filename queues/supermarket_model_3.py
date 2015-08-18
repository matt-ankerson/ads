from queue import Queue
from customer import Customer
import random as r

# Author: Matt Ankerson
# Date: 15 August 2015

# This script models queue behaviour at a supermarket.
# The scenario is: 10 checkouts, customers are all held in a staging queue.
# When a checkout becomes available, the next customer is placed at that checkout.

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
        self.staging_queue = Queue()
    
    def add_customer(self):
        # assign a new customer to the staging queue
        c = Customer(r.randint(1, 5))
        self.staging_queue.enqueue(c)
        self.n_customers += 1       # increment n_customers
        
    def clock_a_minute(self):
        self.time_taken += 1
        # add a customer every two minutes.
        if self.n_customers <= 1000 and self.time_taken % 2 == 0:
            self.add_customer()
        # decrement time required for the people at a checkout.
        # place the next customer at any empty checkout
        for checkout in self.checkouts:
            if checkout.is_empty():
                if not self.staging_queue.is_empty(): 
                    checkout.enqueue(self.staging_queue.dequeue())
            else:
                # decrement time left for the customer
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
    print("Staging Queue Assignment: ")
    soup = SuperMarket()
    while not soup.done:
        soup.clock_a_minute()
    print("Time taken: " + str(soup.time_taken))