class House:
    def __init__(self, doors, windows, pools):
        self.doors = doors
        self.windows = windows
        self.pools = pools

    def market_value(self):
        market_value = (self.doors * 12) + (self.windows * 71) + (self.pools * 300)
        return market_value

    # def market_value(self):
    #     return ((12 * self.doors) + (71 * self.windows) + (300 * self.pools)) * global_meh_factor

    def description(self):
        return 'This house has {} doors, {} windows and {} pools with a market value of {}'.format(self.doors,
                                                                                                   self.windows,
                                                                                                   self.pools,
                                                                                                   self.market_value())


my_house = House(doors=1, windows=2, pools=0)
mansion = House(doors=5, windows=10, pools=100)
prison = House(doors=1, windows=0, pools=0)

print(my_house.description())
print(mansion.description())
print(prison.description())
