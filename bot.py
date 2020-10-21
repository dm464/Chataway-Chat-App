import requests, json, os, dotenv, validators
from datetime import date, datetime

ABOUT = "about"
HELP = "help"
LOCATION = "location"
TIME = "time"
DATE = "date"
FUNSTRANSLATE = "funtranslate"

try:
    dotenv_path = os.path.join(os.path.dirname(__file__), 'ipstack.env')
    dotenv.load_dotenv(dotenv_path)
except AttributeError:
    pass
IPSTACK_KEY=os.environ["IPSTACK_KEY"]

def is_bot_command(message):
    message_arr = message.split(" ")
    if message_arr[0]=="!!":
        return True
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
        return "Uh oh! \'{}\' is not a valid command.<br>Type \'!! help\' for guidance.".format(message)

def about_command():
    return "How art thou? T'is I, none other than Sir Robot. I am hither to assist thee."
    
def help_command():
    ret_str = "Do you need my help? Use the following commands: <br>"
    ret_str += "!! about - get a description about me<br>"
    ret_str += "!! help - displays list of bot commands<br>"
    ret_str += "!! location - current location<br>"
    ret_str += "!! time - current local time<br>"
    ret_str += "!! date - current date<br>"
    ret_str += "!! funtranslate message - I'll translate the message into Shakespearean English"
    return ret_str;

def location_command():
    url = "http://api.ipstack.com/check?access_key={}".format(IPSTACK_KEY)
    json_body = requests.get(url).json()
    city = json_body["city"]
    region = json_body["region_name"]
    country_code = json_body["country_code"]
    # For further enhancement, I can add flag emoji
    return "Your current location is {}, {} {}".format(city, region, country_code)

def time_command():
    time = datetime.now().strftime("%H:%M")
    return "The time is " + time

def date_command():
    today = date.today().strftime("%B %d, %Y")
    return "Today is " + today

def funtranslate_command(message):
    message = message[len("!! {} ".format(FUNSTRANSLATE)):]
    url = "https://api.funtranslations.com/translate/shakespeare.json?text={}".format(message)
    json_body = requests.get(url).json()
    translated_message = json_body["contents"]["translated"]
    return translated_message

def render(message):
    valid=validators.url(message)
    if valid == True:
        return "<a href=\"{}\" target=\"_blank\">{}</a>".format(message, message)