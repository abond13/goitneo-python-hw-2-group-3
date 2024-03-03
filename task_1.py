"""
    Домашнє завдання №2
    Завдання №1
"""
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Give me name please."
        except KeyError:
            return "No such contact."
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def print_help():
    return "Available commands:\n" + \
           "\tadd [name] [phone]\n" + \
           "\tchange [name] [phone]\n" + \
           "\tphone [name]\n" + \
           "\tall\n" + \
           "\texit"

@input_error
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    name, phone = args
    contacts[name]
    contacts[name] = phone
    return "Contact updated."

@input_error
def phone(args, contacts):
    name = args[0]
    return contacts[name]

def show_all(contacts):
    return "\n".join([f"{name} : {phone}" for name, phone in contacts.items()])

def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        if user_input:
            command, *args = parse_input(user_input)
        else:
            continue
        if command in ["close", "exit", "quit"]:
            print("Good bye!")
            break
        if command == "hello":
            print("How can I help you?")
        elif command == "help":
            print(print_help())
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
