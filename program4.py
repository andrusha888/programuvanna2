from abc import ABC, abstractmethod


class Delivery(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def calculate_cost(self, weight):
        pass

    @abstractmethod
    def deliver(self, address):
        pass

    def info(self, weight):
        return f"{self.name}: доставка коштує {self.calculate_cost(weight):.2f} грн"


class CourierDelivery(Delivery):
    @property
    def name(self):
        return "Кур'єр"

    def calculate_cost(self, weight):
        return 50 + weight * 15

    def deliver(self, address):
        return f"Кур'єр доставить замовлення за адресою: {address}"


class PostDelivery(Delivery):
    @property
    def name(self):
        return "Пошта"

    def calculate_cost(self, weight):
        return 30 + weight * 10

    def deliver(self, address):
        return f"Посилку відправлено на відділення: {address}"


class MessageLog:
    def write(self, message):
        print("Повідомлення:", message)


class Order:
    def __init__(self, product_cost, weight, address, delivery, log):
        self.product_cost = product_cost
        self.weight = weight
        self.address = address
        self.delivery = delivery
        self.log = log

    def complete(self):
        shipping = self.delivery.calculate_cost(self.weight)
        self.log.write(self.delivery.deliver(self.address))
        print("Спосіб доставки:", self.delivery.name)
        print(f"Вартість товарів: {self.product_cost:.2f} грн")
        print(f"Вартість доставки: {shipping:.2f} грн")
        print(f"Усього: {self.product_cost + shipping:.2f} грн")


try:
    delivery = Delivery()
except TypeError as error:
    print("Не можна створити Delivery:", error)

methods = [CourierDelivery(), PostDelivery()]
print("\nПоліморфна перевірка способів доставки:")
for method in methods:
    print(method.info(2))
    print(method.deliver("Київ"))

print("\nОформлення замовлень:")
log = MessageLog()

order1 = Order(500, 2, "Київ, вул. Центральна, 10", methods[0], log)
order1.complete()

print()
order2 = Order(700, 3, "Відділення №5", methods[1], log)
order2.complete()
