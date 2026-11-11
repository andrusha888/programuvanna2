import random
import threading
import time


class BankAccount:
    def __init__(self, balance: float = 0.0):
        self.balance = balance
        self.transaction_count = 0

    def deposit(self, amount: float) -> None:
        current = self.balance
        time.sleep(random.uniform(0.0001, 0.001))
        self.balance = current + amount
        self.transaction_count += 1

    def withdraw(self, amount: float) -> bool:
        current = self.balance
        time.sleep(random.uniform(0.0001, 0.001))
        if current >= amount:
            self.balance = current - amount
            self.transaction_count += 1
            return True
        return False


class SafeBankAccount:
    def __init__(self, balance: float = 0.0):
        self.balance = balance
        self.transaction_count = 0
        self._lock = threading.Lock()

    def deposit(self, amount: float) -> None:
        with self._lock:
            current = self.balance
            time.sleep(random.uniform(0.0001, 0.001))
            self.balance = current + amount
            self.transaction_count += 1

    def withdraw(self, amount: float) -> bool:
        with self._lock:
            current = self.balance
            time.sleep(random.uniform(0.0001, 0.001))
            if current >= amount:
                self.balance = current - amount
                self.transaction_count += 1
                return True
            return False


def run_transactions(account, num_deposits: int, num_withdrawals: int, amount: float):
    threads = []

    def make_deposits():
        for _ in range(num_deposits // 5):
            account.deposit(amount)

    def make_withdrawals():
        for _ in range(num_withdrawals // 5):
            account.withdraw(amount)

    for _ in range(5):
        threads.append(threading.Thread(target=make_deposits))
        threads.append(threading.Thread(target=make_withdrawals))

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def main():
    initial_balance = 1000.0
    num_deposits = 100
    num_withdrawals = 100
    amount = 5.0
    expected_balance = initial_balance + num_deposits * amount - num_withdrawals * amount

    print("=== Без синхронізації ===")
    unsafe = BankAccount(initial_balance)
    run_transactions(unsafe, num_deposits, num_withdrawals, amount)
    print(f"Баланс: {unsafe.balance:.2f}")
    print(f"Транзакцій: {unsafe.transaction_count}")
    print(f"Правильний результат: {unsafe.balance == expected_balance}")

    print("\n=== Із синхронізацією Lock ===")
    safe = SafeBankAccount(initial_balance)
    run_transactions(safe, num_deposits, num_withdrawals, amount)
    print(f"Баланс: {safe.balance:.2f}")
    print(f"Транзакцій: {safe.transaction_count}")
    print(f"Правильний результат: {safe.balance == expected_balance}")
    print(f"\nОчікуваний баланс: {expected_balance:.2f}")


if __name__ == "__main__":
    main()
