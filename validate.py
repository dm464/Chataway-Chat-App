""" Python3 program to validate
image file extension using regex
This function was taken from
https://www.geeksforgeeks.org/how-to-validate-image-file-extension-using-regular-expression/
"""
import re

def image_file(potential_image):
    """Returns whether the string refers to an image file or not"""

    # Regex to check valid image file extension.
    regex = "([^\\s]+(\\.(?i)(jpe?g|png|gif|bmp))$)"

    # Compile the ReGex
    compiled_regex = re.compile(regex)

    # If the string is empty
    # return false
    if potential_image is None:
        return False

    # Return if the string
    # matched the ReGex
    if re.search(compiled_regex, potential_image):
        return True
    return False
