import os
import boto3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from get_daily_data import get_daily_data
from convert_daily_data_to_pdf import store_file_as_pdf
from get_user_list import get_user_list
from configparser import ConfigParser

configure = ConfigParser()
configure.read("secret.ini")


ACCESS_KEY = configure.get("AWS", "ACCESS_KEY")
SECRET_KEY = configure.get("AWS", "SECRET_KEY")
BUCKET = configure.get("AWS", "BUCKET")
REGION = configure.get("AWS", "REGION")
SENDER = configure.get("AWS", "SENDER")


def get_client():
    return boto3.client(
        's3',
        REGION,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )


def send_email(sender, recipient, aws_region, subject, file_name, actual_filename):
    BODY_TEXT = "Hello,\r\nPlease find the attached file."
    BODY_HTML = """\
    <html>
    <head></head>
    <body>
    <h6>Hello</h6>
    <p>Please find the attached daily report.</p>
    <p>Thank You.</p>
    <p>SIH2020.</p>
    </body>
    </html>
    """
    CHARSET = "utf-8"
    client = boto3.client('ses', region_name=aws_region, aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY,)
    msg = MIMEMultipart('mixed')
    # Add subject, from and to lines.
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    msg_body = MIMEMultipart('alternative')
    textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
    htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)
    # Add the text and HTML parts to the child container.
    msg_body.attach(textpart)
    msg_body.attach(htmlpart)
    # Define the attachment part and encode it using MIMEApplication.
    att = MIMEApplication(open(file_name, 'rb').read())
    att.add_header('Content-Disposition', 'attachment',
                   filename=actual_filename)
    if os.path.exists(file_name):
        print("File exists")
    else:
        print("File does not exists")
    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.
    msg.attach(msg_body)
    # Add the attachment to the parent container.
    msg.attach(att)
    try:
        # Provide the contents of the email.
        response = client.send_raw_email(
            Source=msg['From'],
            Destinations=[
                msg['To']
            ],
            RawMessage={
                'Data': msg.as_string(),
            }
        )
    # Display an error if something goes wrong.
    except Exception as e:
        print(e)
        return
    else:
        print("Email sent! Message ID:", response['MessageId'])


def app(event=None, context=None):
    latest_ca = get_daily_data()
    response, filename = store_file_as_pdf(latest_ca)
    if not response:
        print("Some error occurred")
        return
    else:
        if os.path.exists(filename):
            mailing_list = [user.get('email') for user in get_user_list()]
            print(mailing_list)
            print(filename)
            for email in mailing_list:
                send_email(SENDER, email, REGION,
                           'Daily Report', f"./{filename}", filename)
            os.remove(filename)
        else:
            print("The file does not exist")