# Python3 program to validate 
# image file extension using regex 
# This function was taken from https://www.geeksforgeeks.org/how-to-validate-image-file-extension-using-regular-expression/
import re
 
# Function to validate 
# image file extension .  
def imageFile(str):
 
    # Regex to check valid image file extension.
    regex = "([^\\s]+(\\.(?i)(jpe?g|png|gif|bmp))$)"
     
    # Compile the ReGex
    p = re.compile(regex)
 
    # If the string is empty 
    # return false
    if (str == None):
        return False
 
    # Return if the string 
    # matched the ReGex
    if(re.search(p, str)):
        return True
    else:
        return False
