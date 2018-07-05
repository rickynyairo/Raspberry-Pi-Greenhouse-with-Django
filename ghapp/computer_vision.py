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
    fraction = properties.dominant_colors.colors[0].pixel_fraction
    for color in properties.dominant_colors.colors:
        if color.color.red > max_red:
            max_red, fraction = color.color.red, color.pixel_fraction
    return max_red, fraction

def main():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/pi/Desktop/fyp/web_app/key/fyp-ghmcs-cd159d1de565.json"
    sample_grass = os.path.join(
        os.getcwd(), 
        "static/ghapp/images/sample_grass_1.jpeg"
        )
    sample_grass_with_red_dot = os.path.join(
        os.getcwd(), 
        "static/ghapp/images/sample_grass_with_red_dot.jpg"
        )
    sample_grass_with_red_dots = os.path.join(
        os.getcwd(), 
        "static/ghapp/images/sample_grass_with_red_dots.jpg"
        )
    print ("No red dot:")
    print (detect_properties(sample_grass))
    print ("With red dot:")
    print (detect_properties(sample_grass_with_red_dot))
    print ("With red dots:")
    print (detect_properties(sample_grass_with_red_dots))

if __name__ == "__main__":
    main()
