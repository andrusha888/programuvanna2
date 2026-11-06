class Transport:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def move(self):
        return "Транспорт рухається"

    def __str__(self):
        return f"{self.brand} {self.model}"


class Car(Transport):
    def __init__(self, brand, model, fuel):
        super().__init__(brand, model)
        self.fuel = fuel

    def move(self):
        return f"Автомобіль {self} їде, паливо: {self.fuel}"


class Bus(Transport):
    def __init__(self, brand, model, seats):
        super().__init__(brand, model)
        self.seats = seats

    def move(self):
        return f"Автобус {self} перевозить пасажирів, місць: {self.seats}"


class Bicycle(Transport):
    def __init__(self, brand, model, gears):
        super().__init__(brand, model)
        self.gears = gears

    def move(self):
        return f"Велосипед {self} рухається завдяки педалям, передач: {self.gears}"


vehicles = [
    Car("Toyota", "Corolla", "бензин"),
    Bus("Mercedes", "Sprinter", 18),
    Bicycle("Trek", "Marlin", 21)
]

print("Робота різних видів транспорту:")
for vehicle in vehicles:
    print(vehicle.move())

print("\nПеревірка типів:")
print("Перший об'єкт є Transport:", isinstance(vehicles[0], Transport))
print("Другий об'єкт є Bus:", isinstance(vehicles[1], Bus))
print("Car є підкласом Transport:", issubclass(Car, Transport))
print("Bicycle є підкласом Car:", issubclass(Bicycle, Car))
