class BankAccount:
    def __init__(self, owner, balance, annual_rate):
        self._owner = owner
        self._annual_rate = annual_rate
        self.__balance = 0
        self.balance = balance

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Баланс має бути числом")
        if value < 0:
            raise ValueError("Баланс не може бути від'ємним")
        self.__balance = value

    @property
    def yearly_interest(self):
        return round(self.__balance * self._annual_rate / 100, 2)


account = BankAccount("Іван", 10000, 5)

print("Власник рахунку:", account._owner)
print("Баланс:", account.balance, "грн")
print("Річні відсотки:", account.yearly_interest, "грн")

account.balance = 12000
print("\nНовий баланс:", account.balance, "грн")
print("Нові річні відсотки:", account.yearly_interest, "грн")

for invalid_value in [-100, "п'ять тисяч"]:
    try:
        account.balance = invalid_value
    except (ValueError, TypeError) as error:
        print("Помилка при значенні", repr(invalid_value), ":", error)

try:
    print(account.__balance)
except AttributeError as error:
    print("Помилка прямого доступу:", error)

print("Доступ через name mangling:", account._BankAccount__balance)
