import base64
import re
from PIL import Image
import io
from src import constants
import math


def validate_data_object(data_object, type):
    validation = True
    message = None
    if('image' not in data_object or 'description' not in data_object):
        message = 'Both Base64 Image value and description are required'
        validation = False
    elif('description' in data_object and type == constants.RESIZE):
        des_obj = data_object['description']
        if('width' not in des_obj or 'height' not in des_obj):
            message = 'if process type is Resizing, you must provide valid description with height and width.(ex: description: {width : 20, height: 20}) '
            validation = False
    elif(not is_valid_base64_image(data_object['image'])):
        message = 'The image file is not valid base64 image'
        validation = False
        
    return validation, message

def validate_description(update_type, description_val):
    validation = True
    message = None
    if(update_type == constants.FLIP and description_val not in constants.FLIP_LIST):
       message = 'Enter a valid Flipping type (ex: Top, Bottom, Left, Right)'
       validation = False
    elif(update_type == constants.RESIZE):
        try:
            width = math.isnan(description_val['width'])
            height = math.isnan(description_val['height'])
        except Exception:
            message = 'Enter the resolution in (width, height) format (ex: (20,20))'
            validation = False 
    return validation, message
        
        
           
    
def is_valid_base64_image(image_string):
    # checking valid base64 image string 
    try:
        image = base64.b64decode(image_string)
        img = Image.open(io.BytesIO(image))
        return True
    except Exception:
        return False