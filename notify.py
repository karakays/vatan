import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import user_mail

# TODO secure password securely
user_pwd = None


def notify(item):
    server = smtplib.SMTP(host='smtp.gmail.com', port='587')
    server.ehlo()
    server.starttls()
    server.login(user_mail, user_pwd)
    mime_msg = MIMEMultipart()
    mime_msg['From'] = user_mail
    mime_msg['To'] = user_mail
    mime_msg['Subject'] = 'Vatan: Price change event'
    mime_msg.attach(MIMEText(prepare_content(item)))
    server.sendmail(user_mail, user_mail, mime_msg.as_string())
    server.close()


def prepare_content(item):
    t = read_template('mail')
    return t.substitute(ITEM=item.name, PRICE=item.amount)


def read_template(filename):
    with open(filename, mode='r') as file_res:
        content = file_res.read()
        return Template(content)
