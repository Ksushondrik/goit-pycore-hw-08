def input_error(func):

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter the argument for the command. Give me name and phone or birthday, please."
        except KeyError:
            return "No such name found"
        except IndexError:
            return "Enter the argument for the command. Give me name, please."
        except Exception as e:
            return f"Error: {e}"

    return inner
