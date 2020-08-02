import pandas as pd
import base64
import os
import pdfkit
import boto3
import datetime

from configparser import ConfigParser

configure = ConfigParser()
configure.read("secret.ini")

ACCESS_KEY = configure.get("AWS", "ACCESS_KEY")
SECRET_KEY = configure.get("AWS", "SECRET_KEY")
BUCKET = configure.get("AWS", "BUCKET")


def store_file_as_pdf(get_latest_ca):
    ca_array = []
    now = datetime.datetime.now().strftime("%d-%b-%Y")
    filename = f"Daily Report ( {now} ).pdf"
    ret2 = store_file(filename, get_latest_ca, 'pdf')
    return ret2, filename


def store_file(filename, data, typ="pdf"):
    if typ == 'pdf':
        df = pd.DataFrame(data=data)
        df.fillna('-')
        directory = os.path.dirname(os.path.realpath(__file__))
        html_file_path = os.path.join("Daily Report.html")
        pdf_file_path = os.path.join(filename)
        fd = open(html_file_path, 'w')
        intermediate = df.to_html()
        fd.write(intermediate)
        fd.close()
        pdfkit.from_file(html_file_path, pdf_file_path)
    uploaded = upload_to_aws(filename, filename)
    return uploaded


def upload_to_aws(local_file, s3_file):
    bucket = BUCKET
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
