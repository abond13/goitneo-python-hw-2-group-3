"""
    Домашнє завдання №2
    Завдання №2
"""

import re
from collections import UserDict
from contextlib import contextmanager

### Exceptions
class NameFormatError(Exception):
    pass

class PhoneFormatError(Exception):
    pass

### Classes
class Field:
    """
    Базовий клас для полів запису.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    """
    Клас для зберігання імені контакту.

    Мої додаткові умови:
        Імʼя має задоволняти наступним вимогам:
            1. Довжина повинна бути 2+ символів.
            2. Перша літера велика.
                Наприклад: Al
            3. Може мати другу частину через пробіл,
            яка теж починається з великої літери і має як мінімум два символи.
                Наприклад: Al Gore
    """
    def __init__(self, name):
        if not re.fullmatch("[A-Z][a-z]+(\s[A-Z][a-z]+)?", name):
            raise NameFormatError
        super().__init__(name)

class Phone(Field):
    """
    Клас для зберігання номера телефону.
    Телефон має задоволняти наступним вимогам:
        1. Складається з цифр.
        2. Довжина повинна бути 10 символів.
    """
    def __init__(self, phone):
        if not re.fullmatch("[0-9]{10}", phone):
            raise PhoneFormatError
        super().__init__(phone)

class Record:
    """
    Клас для зберігання інформації про контакт,
    включаючи ім'я та список телефонів.
    """
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        # Додаємо лише унікальний телефон
        if self.find_phone_record(phone) is None:
            self.phones.append(Phone(phone))
            return True
        return False

    def remove_phone(self, phone):
        record = self.find_phone_record(phone)
        if record:
            self.phones.remove(record)
            return True
        return False

    def edit_phone(self, old_phone, new_phone):
        # Якщо старий телефон існує, і якщо ми успішно додали новий
        # телефон, то тоді видаляємо старий
        if self.find_phone(old_phone) and self.add_phone(new_phone):
            self.remove_phone(old_phone)
            return True
        return False

    def find_phone(self, phone):
        record = self.find_phone_record(phone)
        if record:
            return self.find_phone_record(phone).value
        return None

    def find_phone_record(self, phone):
        # Так як номер унікальний (див. add_phone()),
        # то виходимо відразу, якщо його знайшли.
        for record in self.phones:
            if record.value == phone:
                return record
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def find(self, name):
        return self.data.get(name, None)

    def add_record(self, record:Record):
        self.data[record.name.value] = record

    def delete(self, name):
        if self.data.pop(name, None):
            return True
        return False

    def __str__(self):
        return 'Address book:\n\t' + '\n\t'.join(record.__str__() for record in self.data.values())


# Ловимо наші виняткoві ситуації
@contextmanager
def catch_my_exceptions(*exceptions):
    try:
        yield
    except NameFormatError:
        print("Wrong name")
    except PhoneFormatError:
        print("Wrong phone")


def main():
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john) # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")


    ##################
    # Додаткові тести:
    print("\n\n\n* Additional tests: *")
    with catch_my_exceptions(Exception):
        print("\nTest #1")
        bad_name = Name("john") # Виведення: Wrong name

    with catch_my_exceptions(Exception):
        print("\nTest #2")
        bad_phone = Phone("333") # Виведення: Wrong phone

    print("\nTest #3")
    jbond = Record("James Bond")
    jbond.add_phone("8765432100")
    jbond.add_phone("1111111111")
    jbond.add_phone("8765432100") # номер–дублікат -- не додаємо
    print(jbond) # Виведення: Contact name: James Bond, phones: 8765432100; 1111111111

    print("\nTest #4")
    with catch_my_exceptions(Exception):
        jbond.edit_phone("1111111111","1234") # Виведення: Wrong phone

    print("\nTest #5")
    with catch_my_exceptions(Exception):
        jbond.edit_phone("1111111111","8765432100") # Заміна на номер, який вже існує -- ігноруєм
    print(jbond) # Виведення: Contact name: James Bond, phones: 8765432100; 1111111111

    print("\nTest #6")
    with catch_my_exceptions(Exception):
        jbond.remove_phone("111") # Видалення неіснуючого номера -- ігноруєм
    print(jbond) # Виведення: Contact name: James Bond, phones: 8765432100; 1111111111

    print("\nTest #7")
    print(jbond.find_phone("5555555555")) # Виведення: None

    print("\nTest #8")
    book.add_record(jbond)
    book.add_record(jbond) # додаємо дублікат
    print(book) # друкуемо всю книгу
    # Виведення:
    # Address book:
    #         Contact name: John, phones: 5555555555; 1112223333
    #         Contact name: James Bond, phones: 8765432100; 1111111111

    print("\nTest #9")
    print(book.find("James")) # Виведення: None
    print(book.delete("James")) # видаляємо неіснуючий контакт -- Виведення: False
    print(book) # друкуемо всю книгу
    # Виведення:
    # Address book:
    #         Contact name: John, phones: 5555555555; 1112223333
    #         Contact name: James Bond, phones: 8765432100; 1111111111

if __name__ == "__main__":
    main()
