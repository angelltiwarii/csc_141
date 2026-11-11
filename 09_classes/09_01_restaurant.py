# This is quite difficult with a level of 6/10

class Restaurant:
    """ Model a restaurant with OOP """
    def __init__ (self,restaurant_name,cusine_type,location,price_range):
        self.restaurant_name = restaurant_name
        self.cusine_type = cusine_type
        self.location = location
        self.price_range = price_range

    def describe_restaurant (self):
        print (f'The restaurant name is {self.restaurant_name}.')
        print(f'The price is {self.price_range}.')

    def can_you_take_a_date(self):
        if self.price_range < 50:
            print(f"Don't embarrass yourself. It's too expensive!")
        else:
            print(f"You can afford {self.restaurant_name}.")

an.restaurant=Restaurant('Cici Shack', 'Soul Food', 'Philidelphia', 20)
an.restaurant.can_you_take_a_date()