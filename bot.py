import requests, json, os, dotenv, validators, validate
from datetime import date, datetime

ABOUT = "about"
HELP = "help"
LOCATION = "location"
TIME = "time"
DATE = "date"
FUNSTRANSLATE = "funtranslate"
BOT_PIC = "https://media.istockphoto.com/vectors/robot-icon-vector-artificial-intelligence-vector-id1161996344"

BOT_HELP_REPLY = "Do you need my help? Use the following commands: <br>\
!! about - get a description about me<br>\
!! help - displays list of bot commands<br>\
!! location - current location<br>\
!! time - current local time<br>\
!! date - current date<br>\
!! funtranslate message - I'll translate the message into Shakespearean English"
BOT_LOCATION_REPLY = "Your current location is {}, {} {}"
BOT_TIME_REPLY = "The time is {}"
BOT_DATE_REPLY = "Today is {}"
BOT_INVALID_COMMAND_REPLY = "Uh oh! \'{}\' is not a valid command.<br>Type \'!! help\' for guidance."
RENDERED_LINK_TEMPLATE = "<a class=\"message_link\"href=\"{}\" target=\"_blank\">{}</a>"
RENDERED_IMAGE_TEMPLATE = "<br><img src=\"{}\" alt=\"{}\" class=\"message-image\">"

try:
    dotenv_path = os.path.join(os.path.dirname(__file__), 'ipstack.env')
    dotenv.load_dotenv(dotenv_path)
except AttributeError:
    pass
IPSTACK_KEY=os.environ["IPSTACK_KEY"]

def is_bot_command(message):
    return message.startswith("!!")

def bot_reply(message):
    message_arr = message.split(" ")
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
        return invalid_command(message)

def about_command():
    return "How art thou? T'is I, none other than Sir Robot. I am hither to assist thee."
    
def help_command():
    return BOT_HELP_REPLY;

def location_command():
    url = "http://api.ipstack.com/check?access_key={}".format(IPSTACK_KEY)
    json_body = requests.get(url).json()
    city = json_body["city"]
    region = json_body["region_name"]
    country_code = json_body["country_code"]
    # For further enhancement, I can add flag emoji
    return BOT_LOCATION_REPLY.format(city, region, country_code)

def time_command():
    time = datetime.now().strftime("%H:%M")
    return BOT_TIME_REPLY.format(time)

def date_command():
    today = date.today().strftime("%B %d, %Y")
    return BOT_DATE_REPLY.format(today)

def funtranslate_command(message):
    message = message[len("!! {} ".format(FUNSTRANSLATE)):]
    url = "https://api.funtranslations.com/translate/shakespeare.json?text={}".format(message)
    json_body = requests.get(url).json()
    translated_message = json_body["contents"]["translated"]
    return translated_message

def invalid_command(message):
    return BOT_INVALID_COMMAND_REPLY.format(message)

def is_link(message):
    if validators.url(message):
        return True
    else:
        return False

def is_image(message):
    return validate.imageFile(message)

def render(message):
    if is_link(message):
        rendered_message = RENDERED_LINK_TEMPLATE.format(message, message)
        if is_image(message):
            rendered_message += RENDERED_IMAGE_TEMPLATE.format(message, message)
        return rendered_message
    else:
        return message