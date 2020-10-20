import requests, json
from datetime import date, datetime

ABOUT = "about"
HELP = "help"
LOCATION = "location"
TIME = "time"
DATE = "date"
FUNSTRANSLATE = "funtranslate"

def is_bot_command(message):
    message_arr = message.split(" ")
    if message_arr[0]=="!!":
        commands = [ABOUT, HELP, LOCATION, TIME, DATE, FUNSTRANSLATE]
        if message_arr[1] in commands:
            return True
        else:
            return False
    else:
        return False


def bot_reply(message):
    message_arr = message.split(" ")
    print(message_arr)
    command = message_arr[1]
    if command == ABOUT:
        return about_command()
    elif command == HELP:
        return help_command()
    elif command == LOCATION:
        return location_command()
    elif command == TIME:
        return time_command()
    elif command == DATE:
        return date_command()
    elif command == FUNSTRANSLATE:
        return funtranslate_command(message)
    else:
        return "Uh oh! That's not a valid command. Type \"!! Help\" for guidance"

def about_command():
    return "How art thou? T'is I, none other than Sir Robot. I am hither to assist thee."
    
def help_command():
    ret_str = "Though needeth my help? Use the following commands: \n"
    ret_str += "!! about - gives bot description\n"
    ret_str += "!! help - displays list of commands\n"
    ret_str += "!! location - gives current location\n"
    ret_str += "!! time - gives current local time\n"
    ret_str += "!! date - give current date\n"
    ret_str += "!! funtranslate <message> - I'll translate the message into old English\n"
    return ret_str;

def location_command():
    return "Location: Sorry, still need location API"

def time_command():
    time = datetime.now().strftime("%H:%M")
    return "The time is " + time

def date_command():
    today = date.today().strftime("%B %d, %Y")
    return "Today is " + today

def funtranslate_command(message):
    url = "https://api.funtranslations.com/translate/shakespeare.json?text={}".format(message)
    json_body = requests.get(url).json()
    translated_message = json_body["contents"]["translated"]
    return translated_message