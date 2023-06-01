class Vehicule:
    color = "White"
    
    def __init__(self, name, max_speed, mileage) -> None:
        self.name = name
        self.max_speed = max_speed
        self.mileage = mileage
    
    def seating_capacity(self, capacity):
        return f"The seating capacity of a {self.name} is {capacity} passengers"

class Bus(Vehicule):
    def seating_capacity(self, capacity=50):
        return super().seating_capacity(capacity=50)
    

bus = Bus("tobis", 200, 100000)
print(bus.seating_capacity())