import io
import os
from google.cloud import vision
from google.cloud.vision import types


def detect_properties(image_path):
    client = vision.ImageAnnotatorClient()
    #load image into memory
    with io.open(image_path, "rb") as image_file:
        content = image_file.read()

    image = types.Image(content = content) 
    properties = client.image_properties(image=image).image_properties_annotation
    
    max_red = properties.dominant_colors.colors[0].color.red
    fraction = 0
    for color in properties.dominant_colors.colors:
        testval = color.color.red * color.color.green * color.color.blue
        if color.color.red > max_red:
            max_red = color.color.red
        if testval >= 1100000:  
            fraction = fraction + color.pixel_fraction
    return max_red, fraction

def main():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/pi/Desktop/fyp/web_app/key/fyp-ghmcs-cd159d1de565.json"

    no_weeds = os.path.join(
        os.getcwd(), 
        "static/ghapp/images/no_weeds.jpeg"
        )
    lots_of_weeds = os.path.join(
        os.getcwd(), 
        "static/ghapp/images/a_lot_of_weeds.jpeg"
        )
    lots_of_weeds_2 = os.path.join(
        os.getcwd(), 
        "static/ghapp/images/a_lot_of_weeds_2.jpeg"
        )
    few_weeds = os.path.join(
        os.getcwd(), 
        "static/ghapp/images/few_weeds.jpeg"
        )

    def weed_detection():
        print ("No weeds")
        print (detect_properties(no_weeds))
        print ("With a few weeds: ")
        print (detect_properties(few_weeds))
        print ("With more weeds: ")
        print (detect_properties(lots_of_weeds))
        print ("With more weeds 2: ")
        print (detect_properties(lots_of_weeds_2))

    weed_detection()

if __name__ == "__main__":
    main()
