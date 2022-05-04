import random
import time

class Customer:

    def __init__(self, items:int) -> object:
        self.items:int = items # Number of items the customer has to checkout

    def find_best_checkout(self, checkouts:list):
        """ Find the best checkout to go to using a list of checkouts """

        can_use_express_checkout:bool = self.items <= 10 # Determines if the customer can use an express checkout
        best_checkout:Checkout = None # Keep track of best so far
        lowest_customer_items:int = 0
        
        # Iterate through each checkout
        for checkout in checkouts:
            
            # Check if the checkout is express and if the customer can use it
            # Skip this checkout if the customer is not ellegible to use it
            if checkout.express and not can_use_express_checkout:
                continue

            customer = checkout.get_last_customer() # Get the last customer in the queue

            # Check if the customer at the back of the queue has a smaller amount of items
            # Than the recorded lowest
            if best_checkout == None or customer.items < lowest_customer_items:
                best_checkout = checkout # Update best checkout
                lowest_customer_items = customer.items # Update lowest number of items
        
        # When the search has finished add the customer to the best queue
        best_checkout.add_customer(self)


class Checkout:

    def __init__(self, express:bool) -> object:
        self.customers:list[Customer] = [] # Holds a queue of customers
        self.express:bool = express # Is the checkout an express checkout?

    def update(self) -> None:
        """ Processes the queue of customers """

        # if queue is empty do nothing
        if self.customers == []: return
        
        # First, check if the customer at the front of the queue has any items
        if self.customers[0].items == 0:
            del(self.customers[0]) # Remove customer from the queue
            return

        self.customers[0].items -= 1 # Process one item

    def get_last_customer(self) -> Customer:
        """ Get the last customer in the queue """
        return self.customers[-1]

    def add_customer(self, customer:Customer) -> None:
        """ Add a customer to the queue """
        self.customers.append(customer)



def autopopulate_checkouts(checkouts:list) -> None:
    """ Autopopulate checkouts with customers """

    for checkout in checkouts:
        
        # Gen 3 - 6  customers for every chekout
        for x in range(random.randint(3, 6)):
            # Generate customer with 10 items or less if checkout is express
            if checkout.express:
                customer = Customer(random.randint(1, 10))
            else:
                customer = Customer(random.randint(1, 20))

            checkout.add_customer(customer)

def display_checkouts(checkouts:list) -> None:
    """ Print out the queue for each checkout """
    
    for i,checkout in enumerate(checkouts):
        print(f"{str(i+1)}{'(E)' if checkout.express else ''}", end="\t")
        item_total = 0
        for customer in checkout.customers:
            print(f"{customer.items:<4}", end=" ")
            item_total += customer.items
        print("\n",end="")
    print("\n\n")

def main() -> None:
    """ Main code """

    checkouts = [
        Checkout(False),
        Checkout(False),
        Checkout(False),
        Checkout(True)
    ]

    autopopulate_checkouts(checkouts)

    while True:

        # 1 in 2 chance of new customer joining a queue
        if random.randint(1,2) == 1:
            customer = Customer(random.randint(1, 20)) # Customer can spawn with 1 - 20 items
            print(f"NEW CUSTOMER - Items: {customer.items}")
            customer.find_best_checkout(checkouts)

        # Update the checkouts
        for checkout in checkouts:
            checkout.update()

        display_checkouts(checkouts)
        time.sleep(1)

main()
