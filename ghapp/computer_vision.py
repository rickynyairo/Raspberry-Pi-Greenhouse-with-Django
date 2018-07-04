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
    labels = client.label_detection(image=image).label_annotations
    #annotation_response = client.annotate_image({"image":{"source":{"image_uri":image_path}}})
    properties = client.image_properties(image=image).image_properties_annotation

    print("Labels: ")
    for label in labels:
        print (label.description)

    print ("Properties")
    for color in properties.dominant_colors.colors:
        print('fraction: {}'.format(color.pixel_fraction))
        print('\tr: {}'.format(color.color.red))
        print('\tg: {}'.format(color.color.green))
        print('\tb: {}'.format(color.color.blue))
        print('\ta: {}'.format(color.color.alpha))

def main():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\Users\Ricky Nyairo\\Downloads\\fyp-ghmcs-cd159d1de565.json'
    sample_grass = os.path.join(
        os.getcwd(), 
        "static\ghapp\images\sample_grass_1.jpeg"
        )
    sample_grass_with_red_dot = os.path.join(
        os.getcwd(), 
        "static\ghapp\images\sample_grass_with_red_dot.jpg"
        )
    sample_grass_with_red_dots = os.path.join(
        os.getcwd(), 
        "static\ghapp\images\sample_grass_with_red_dots.jpg"
        )
    print("No red dot:")
    detect_properties(sample_grass)
    print("With red dot:")
    detect_properties(sample_grass_with_red_dot)
    print("With red dots:")
    detect_properties(sample_grass_with_red_dots)

if __name__ == "__main__":
    main()
