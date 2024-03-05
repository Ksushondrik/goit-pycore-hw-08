import decor as de
from classes import AddressBook, Record, Birthday
from datetime import datetime, timedelta
import pickle


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@de.input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@de.input_error
def change_contact(args, book: AddressBook):
    name, phone, new_phone, *_ = args
    record = book.find(name)
    if isinstance(record, Record):
        record.edit_phone(phone, new_phone)
        return "Contact updated."
    else:
        raise Exception("Not found!")


@de.input_error
def show_phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if isinstance(record, Record):
        return f"Contact name: {record.name},\t phones: {'; '.join(phone.value for phone in record.phones)}"
    else:
        raise Exception("Not found!")


@de.input_error
def show_all(book: AddressBook):
    if len(book) > 0:
        for name, record in book.data.items():
            print(record)
        return f"It's all"
    else:
        raise Exception("No mach to show!")


@de.input_error
def add_birthday(args, book: AddressBook):
    name, date, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if isinstance(record, Record):
        record.add_birthday(date)
        return message
    else:
        raise Exception("Not found!")


@de.input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if isinstance(record, Record):
        return f"Contact name: {record.name},\t birthday: {record.birthday}."
    else:
        raise Exception("Not found!")


@de.input_error
def soon_birthdays(book: AddressBook):
    today = datetime.today().date()
    congratulation_list = []
    for name, record in book.items():
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
    if not congratulation_list:
        return f"There are no birthday parties this week"
    else:
        print("List of greetings for the current week:")
        a = "Name"
        b = "Birthday"
        c = "Day_for_greetings"
        s = f"|| {a:>15} | {b:>20} | {c:>20} ||"
        print(s)
        for line in congratulation_list:
            a = line["Name"]
            b = line["Birthday"]
            c = line["Day_for_greetings"]
            s = f"|| {a:>15} | {b:>20} | {c:>20} ||"
            print(s)
        return f"It's all!"


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(book, file)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()    # Повернення нової адресної книги, якщо файл не знайдено
