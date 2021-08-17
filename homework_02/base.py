from abc import ABC

class Vehicle(ABC):
    weight = 1500
    started = False
    fuel = 0
    fuel_consumption = 5
    
    def __init__(self, weight = 1500, started = False, fuel = 0, fuel_consumption = 5 ) -> None:
    
    def start(self started, fuel ):
        if started:
            if fuel > 0:
                started = True
                print(started)
