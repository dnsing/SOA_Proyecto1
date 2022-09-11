# pylint: disable=C0103
# pylint: disable=C0114

from google.cloud import vision


vision_client = vision.ImageAnnotatorClient()


def main(data, context):
    print("Contexto", context)
    print("Evento", event)
    if(data == {}):
        print("Analyzing default image")
        imageURL = "images/default.jpg"
        with io.open(path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)

    else:
        imageURL = data["image"]
        print("Analyzing", imageURL ,"image")
        bucket = data["bucket"]
        blob_uri = f"gs://{bucket}/{imageURL}"
        image = vision.Image(source=vision.ImageSource(image_uri=blob_uri))
        

    response = vision_client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    for face in faces:
        result={'anger: {}'.format(likelihood_name[face.anger_likelihood])
                'joy: {}'.format(likelihood_name[face.joy_likelihood])
                'surprise: {}'.format(likelihood_name[face.surprise_likelihood])
                }
        print(result)


    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
