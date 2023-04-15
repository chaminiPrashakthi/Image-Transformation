import os
from flask import Flask, Response, jsonify, request,send_file
from flask_expects_json import expects_json
import base64
from PIL import Image
from flask_inputs import Inputs

from src import constants, validations

    
app = Flask(__name__)

'''
This function is used to process flipping the image
end point : GET -> /image_processing/flip_image 
requst body -> {"timestamp": {string time stamp},
                "description": {string},
                "image": {base 64 string}
                }
return -> sucess Response -> status 200 with encoded resized image
unsucess Response -> error code with error message
'''
   
@app.route("/image_processing/flip_image", methods=['GET'])
def flip_image():
    flipped_output = None
    request_data = request.get_json()
    validation, message = validations.validate_data_object(request_data, constants.FLIP)
    if(validation):
        image, description = process_request_body(request_data, constants.FLIP)
        valid, msg = validations.validate_description(constants.FLIP, description)
        if(valid):
            try:
                opened_visual_image = to_visual_image(image);
                flipped_image = opened_visual_image
                if(description in (constants.LEFT, constants.RIGHT)):
                    flipped_image = opened_visual_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                elif(description in (constants.TOP, constants.BOTTOM)):
                    flipped_image = opened_visual_image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                flipped_image.save("flipped_image.png")
                flipped_output = to_base64_image(flipped_image)
                os.remove("flipped_image.png")
                os.remove("image.png")
                return Response(flipped_output, status=200)
            except:
                return Response("Server Error", status= 500)
        else:
            return Response(msg, status= 400)
    else:
        return Response(message,status= 400)

'''
This function is used to process resizing the image
end point : GET -> /image_processing/resize_image 
requst body -> {"timestamp": {string time stamp},
                "description": {
                    "width" : {number},
                    "height": {number}
                },
                "image": {base 64 string}
                }
return -> sucess Response -> status 200 with encoded resized image
unsucess Response -> error code with error message
'''
         
@app.route("/image_processing/resize_image",  methods=['GET'])
def resize_image():
    resized_output = None

    request_data = request.get_json()
    validation, message = validations.validate_data_object(request_data, constants.RESIZE)
    if(validation):
        image, description, width, height = process_request_body(request_data, constants.RESIZE)
        valid, msg = validations.validate_description(constants.RESIZE, description)
        if(valid):
            try:
                opened_visual_image = to_visual_image(image);
            
                resized_image = opened_visual_image.resize((width, height))
                resized_image.save("resized_image.png")
                resized_output = to_base64_image(resized_image)
                os.remove("resized_image.png")
                os.remove("image.png")
                return Response(resized_output, status= 200)
            except:
                return Response("Server Error", status= 500)
        else:
            return Response(msg, status= 400)
    else:
        return Response(message,status= 400)
    
    
'''
This function is used to process gray scale the image
end point : GET -> /image_processing/grayscale_image 
requst body -> {"timestamp": {string time stamp},
                "description": {string},
                "image": {base 64 string}
                }
return -> sucess Response -> status 200 with encoded gray sclaed image
unsucess Response -> error code with error message
'''    
@app.route("/image_processing/grayscale_image", methods=['GET'])
def grayscale_image():

    request_data = request.get_json()
    validation, message = validations.validate_data_object(request_data, constants.GRAY_SCALE)
    if(validation):
        image, description = process_request_body(request_data, constants.GRAY_SCALE)
        try:
            opened_visual_image = to_visual_image(image);
            
            converted_image = opened_visual_image.convert('L')
            converted_image.save("converted_image.png")
            grayscaled_output = to_base64_image(converted_image)
            os.remove("converted_image.png")
            os.remove("image.png")
            return Response(grayscaled_output,status= 200)
        except:
            return Response("Server Error",status= 500)
    else:
        return Response(message,status= 400)


def to_visual_image(input_image):
    # Decode base64 String Data
    decodedData = base64.b64decode(input_image)
    
    # Write Image from Base64 File
    imgFile = open('image.png', 'wb')
    imgFile.write(decodedData)
    opened_image = Image.open("image.png")
    # imgFile.close()
    return opened_image

def to_base64_image(visual_image):
    encoded_string = None
    with open("image.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string;

def process_request_body(request_data, type):
    image = request_data["image"]
    description = request_data["description"]
    width = 0
    height = 0
    if(type == constants.RESIZE):
        width = description['width']
        height = description['height']
        return image, description, width, height
    return image, description, width, height
