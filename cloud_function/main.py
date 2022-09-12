# pylint: disable=C0103
# pylint: disable=C0114

from google.cloud import vision
import sqlalchemy
import pandas as pd
import os
import json

vision_client = vision.ImageAnnotatorClient()

def main(data, context):

    # Variables
    drivername = "mysql+pymysql"
    username = "root"
    password = "root"
    database = "emotionsTable"
    project_id = "soaproyecto1"
    instance_region= "us-central1"
    instance_name= "instance"
    query_string = dict({"unix_socket": f"/cloudsql/{project_id}:{instance_region}:{instance_name}"})
    table = "emotions"

    print(table)
    print(username)

    
    if(data == {}):
        print("Analyzing default image:")
        imageURL = "images/default.jpg"
        with open(imageURL, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)

    else:
        imageURL = data["image"]
        print("Analyzing ", imageURL ," image:")
        bucket = data["bucket"]
        blob_uri = f"gs://{bucket}/{imageURL}"
        image = vision.Image(source=vision.ImageSource(image_uri=blob_uri))
        

    response = vision_client.face_detection(image=image)
    faces = response.face_annotations
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')


    for face in faces:
        result={  'anger': likelihood_name[face.anger_likelihood],
                  'joy': likelihood_name[face.joy_likelihood],
                  'sorrow': likelihood_name[face.sorrow_likelihood],
                  'surprise': likelihood_name[face.surprise_likelihood]
                }
        print(result)


    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    else:
        print(imageURL)
        result['imageUrl']=imageURL
        print(result)
        df = pd.DataFrame.from_dict(json.dumps(result))
        print(df)
        # Create a sql pool connection
        pool = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL(
                drivername=drivername,
                username=username,
                password=password,
                database=database,
                query=query_string,
            ),
            pool_size=5,
            max_overflow=2,
            pool_timeout=30,
            pool_recycle=1800
        )
        
        # Connect to the database and append the rows into the target table
        try:
            db_connection = pool.connect()
            frame = df.to_sql(table, db_connection, if_exists="append", index=False)
            db_connection.close()
            logging.info("Rows inserted into table successfully...")
        except Exception as e:
            return 'Error: {}'.format(str(e))

