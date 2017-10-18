import smtplib
from vatan import config
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# TODO secure password securely
user_pwd = None


def send_mail(item, snapshot):
    print 'in mailer.send_mail:'
    server = smtplib.SMTP(host='smtp.gmail.com', port='587')
    server.ehlo()
    server.starttls()
    server.login(config.user_mail, user_pwd)
    mime_msg = MIMEMultipart()
    mime_msg['From'] = config.user_mail
    mime_msg['To'] = config.user_mail
    mime_msg['Subject'] = 'Vatan: Price change event'
    mime_msg.attach(MIMEText(prepare_content(item.name, item.amount, snapshot.amounr)))
    server.sendmail(config.user_mail, config.user_mail, mime_msg.as_string())
    server.close()


def prepare_content(item_name, price, last_price):
    t = read_template('mail')
    return t.substitute(ITEM=item_name, PRICE=price, LAST_PRICE=last_price)


def read_template(filename):
    with open(filename, mode='r') as file_res:
        content = file_res.read()
        return Template(content)
