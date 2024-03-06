from collections import UserDict
from datetime import datetime, timedelta
import re, inspect


# Базовий клас для полів запису
class Field:
    def __init__(self, value: str):
        if not value:
            raise Exception("You did not specify a required argument!")
        else:
            self.value = value

    def __str__(self) -> str:
        return str(self.value)


# Клас для зберігання імені контакту. Обов'язкове поле
class Name(Field):
    # реалізація класу
    def __init__(self, value: str):
        if not value.strip():
            raise Exception("You entered an empty string!")
        else:
            super().__init__(value)


# Клас для зберігання номера телефону. Має валідацію формату (10 цифр)
class Phone(Field):
    def __init__(self, value: str):
        if not ((value.isdigit()) and (len(value) == 10)):
            raise Exception("Incorrect phone format! Phone not added!")
        else:
            super().__init__(value)


class Birthday(Field):
    def __init__(self, value: str):
        try:
            # Додайте перевірку коректності даних
            if re.match(r"\d{2}\.\d{2}\.\d{4}", value):
                super().__init__(value)
                # та перетворіть рядок на об'єкт datetime
                datetime.strptime(value, "%d.%m.%Y")
            else:
                raise Exception("Invalid date format. Use DD.MM.YYYY")
        except Exception as e:
            raise Exception("Invalid date format. Use DD.MM.YYYY") from e


# Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів
class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # Додавання телефонів
    def add_phone(self, phone: str):
        phone = Phone(phone)
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)

    # Редагування телефонів
    def edit_phone(self, phone: str, new_phone: str):
        for number in self.phones:
            if number.value == phone:
                self.phones[self.phones.index(number)] = Phone(new_phone)
                break
        else:
            raise Exception(f"Phone {phone} is not found in contact {self.name}")

    # Пошук телефону
    def find_phone(self, phone: str):
        for number in self.phones:
            if number.value == phone:
                return number
        return None

    # Видалення телефонів
    def remove_phone(self, phone: str):
        for number in self.phones:
            if number.value == phone:
                self.phones.remove(number)

    # Додавання дати народження
    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    # Формат виводу даних про контакт
    def __str__(self) -> str:
        return f"Contact name: {self.name},\t\t phones: {'; '.join(str(phone.value) for phone in self.phones)},\t\t birthday: {self.birthday}."


# Клас для зберігання та управління записами
class AddressBook(UserDict):
    # Додавання записів
    def add_record(self, record):
        self.data[record.name.value] = record

    # Пошук записів за іменем
    def find(self, name):
        return self.data.get(name)

    # Видалення записів за іменем
    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self) -> list:
        today = datetime.today().date()
        congratulation_list = []
        for name, record in self.data.items():
            if isinstance(record.birthday, Birthday):
                birthday = record.birthday.value
                birthday = birthday[:6] + str(today.year)
                birthday = (datetime.strptime(birthday, "%d.%m.%Y")).date()
                if 0 <= (birthday - today).days <= 7:  # перевіряємо, чи наступає дата впродовж тижня, включаючи поточний день
                    day_week = (birthday.weekday())  # отримуємо день тижня, на який припадає день народження
                    user_dict = {"Name": name, "Birthday": birthday.strftime("%Y.%m.%d"), }  # створюємо словник з іменем користувача та датою народження
                    if day_week == 5:  # перевіряємо чи не випадає на субботу
                        congratulations_day = birthday + timedelta(days=2)  # день для привітання на 2 дні пізніше, якщо так
                    elif day_week == 6:  # перевіряємо чи не випадає на неділю
                        congratulations_day = birthday + timedelta(days=1)  # день для привітання на день пізніше, якщо так
                    else:  # всі інші припадають на будній день
                        congratulations_day = birthday  # вітати треба в той же день
                    user_dict["Day_for_greetings"] = congratulations_day.strftime("%Y.%m.%d")  # додаємо до словника день привітання
                    congratulation_list.append(user_dict)  # додаємо в список результатів
            else:
                continue
        return congratulation_list


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_phone("5555555555")
    john_record.add_birthday("28.09.1991")

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

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
