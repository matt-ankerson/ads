from priority_queue import PriorityQueue

# Author: Matt Ankerson
# Date: 14 September 2015

# This class models a stock exchange where orders can be input in 0(log n) time,
# regardless of whether or not it can be immediately processed.
# The aim is to optimally match buy orders to sell orders.

class StockExchange(object):
    
    def __init__(self):
        self.buyers = PriorityQueue()
        self.sellers = PriorityQueue()
        
    def buy(self, buy_order):
        '''Input a buy order, regardless of any suitable sell order.'''
        self.buyers.push(buy_order, buy_order)  # use order value for key and value.
        
    def sell(self, sell_order):
        '''Input a sell order, regardless of any suitable buy order.'''
        self.sellers.push(sell_order, sell_order)   # use order value for key and value.
        
    def get_buyers(self):
        '''Return a list of all pending buyers.'''
        summary = 'Pending Buyers: \n'
        for buyer in self.buyers.elements():
            summary += ('$' + str(buyer._key) + '\n')
        return summary
        
    def get_sellers(self):
        '''Return a list of all pending sellers.'''
        summary = 'Pending Sellers: \n'
        for seller in self.sellers.elements():
            summary += ('$' + str(seller._key) + '\n')
        return summary
        
    def process(self):
        '''Process buy orders in an optimal match-up fashion. O(n2) time.'''
        # A buy order for $x can only be processed if there is an existing sell order with price $y
        # such that $x >= $y.
        summary = ''
        temp_buyers = PriorityQueue()                       # Create a temp pq for buyers
        while self.buyers.peek() is not None:               # Iterate all buyers
            buyer = self.buyers.pop()                       # Get the next buyer
            temp_sellers = PriorityQueue()
            buyer_matched = False                           # Assume there's no match for this buyer
            while self.sellers.peek() is not None:
                seller = self.sellers.pop()                 # Get the next seller
                if buyer._key >= seller._key:               # This is a valid matchup
                    buyer_matched = True
                    summary += ('Buyer $' + str(buyer._key) + ' matched with seller $' + str(seller._key) + '\n')
                else:
                    # if this seller was no good, push it on the temp seller pq
                    temp_sellers.push(seller._key, seller._value)
            self.sellers = temp_sellers                     # Copy the temp seller pq back to the original
            if not buyer_matched:
                temp_buyers.push(buyer._key, buyer._value)
        self.buyers = temp_buyers                       # Copy the temp buyer pq back to the original
        return summary
        
if __name__ == '__main__':
    # Try out the Stock Exchange.
    se = StockExchange()
    se.buy(120)
    se.buy(125)
    se.buy(130)
    se.buy(135)
    se.sell(130)
    se.sell(132)
    se.sell(140)
    se.sell(138)
    result = se.process()
    print(result)
    buyers_remaining = se.get_buyers()
    sellers_remaining = se.get_sellers()
    print(buyers_remaining)
    print(sellers_remaining)