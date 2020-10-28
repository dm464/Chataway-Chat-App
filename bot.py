import os
from datetime import date, datetime
import requests
import dotenv
import validators
import validate

ABOUT = "about"
HELP = "help"
LOCATION = "location"
TIME = "time"
DATE = "date"
FUNSTRANSLATE = "funtranslate"
BOT_PIC = "https://media.istockphoto.com/vectors/robot-icon-\
vector-artificial-intelligence-vector-id1161996344"

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
BOT_INVALID_COMMAND_REPLY = (
    "Uh oh! '{}' is not a valid command.<br>Type '!! help' for guidance."
)
RENDERED_LINK_TEMPLATE = '<a class="message_link"href="{}" target="_blank">{}</a>'
RENDERED_IMAGE_TEMPLATE = '<br><img src="{}" alt="{}" class="message-image">'

try:
    dotenv_path = os.path.join(os.path.dirname(__file__), "ipstack.env")
    dotenv.load_dotenv(dotenv_path)
except AttributeError:
    pass
IPSTACK_KEY = os.environ["IPSTACK_KEY"]

def is_bot_command(message):
    """Return whether or not the message is a bot command"""
    return message.startswith("!!")

def bot_reply(message):
    """Return generated bot command that corresponds to the type of command"""
    message_arr = message.split(" ")
    command = message_arr[1]
    if command == ABOUT:
        return about_command()
    if command == HELP:
        return help_command()
    if command == LOCATION:
        return location_command()
    if command == TIME:
        return time_command()
    if command == DATE:
        return date_command()
    if command == FUNSTRANSLATE:
        return funtranslate_command(message)
    return invalid_command(message)

def about_command():
    """Returns the bot's information"""
    return (
        "How art thou? T'is I, none other than Sir Robot. I am hither to assist thee."
    )

def help_command():
    """Returns the bot's help command"""
    return BOT_HELP_REPLY

def location_command():
    """"Returns the location of the user"""
    url = "http://api.ipstack.com/check?access_key={}".format(IPSTACK_KEY)
    json_body = requests.get(url).json()
    city = json_body["city"]
    region = json_body["region_name"]
    country_code = json_body["country_code"]
    # For further enhancement, I can add flag emoji
    return BOT_LOCATION_REPLY.format(city, region, country_code)

def time_command():
    """Returns the current time"""
    time = datetime.now().strftime("%H:%M")
    return BOT_TIME_REPLY.format(time)

def date_command():
    """Returns the current date"""
    today = date.today().strftime("%B %d, %Y")
    return BOT_DATE_REPLY.format(today)

def funtranslate_command(message):
    """Returns the message translated into Shakespearean English"""
    message = message[len("!! {} ".format(FUNSTRANSLATE)) :]
    url = "https://api.funtranslations.com/translate/shakespeare.json?text={}".format(
        message
    )
    json_body = requests.get(url).json()
    translated_message = json_body["contents"]["translated"]
    return translated_message

def invalid_command(message):
    """Returns bot message for invalid bot command"""
    return BOT_INVALID_COMMAND_REPLY.format(message)

def is_link(message):
    """Returns whether the message is a url link or not"""
    if validators.url(message):
        return True
    return False

def is_image(message):
    """Returns whether message is an image or not"""
    return validate.image_file(message)

def render(message):
    """Returns message rendered into html link and or image"""
    if is_link(message):
        rendered_message = RENDERED_LINK_TEMPLATE.format(message, message)
        if is_image(message):
            rendered_message += RENDERED_IMAGE_TEMPLATE.format(message, message)
        return rendered_message
    return message
