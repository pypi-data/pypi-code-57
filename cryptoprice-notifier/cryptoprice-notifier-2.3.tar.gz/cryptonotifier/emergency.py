# Importing All Required Packages
import smtplib
from email.mime.multipart import MIMEMultipart
from config import mail, mail_password


# function to send email for emergency price alert
def emergency_update(email, coin, price):
    recipent_email_address = email

    msg = MIMEMultipart()

    password = mail_password
    msg['From'] = mail
    msg['To'] = recipent_email_address

    message = """From:bitcoinupdate2020@gmail.com
To: {}
Subject:{} Price Below Threshold
{} Price crossed below Threshold\n
Current Price: {} ,\n
Buy Or Sell Now.\n
Also Join us here\n
Telgram: https://t.me/projectcomplete\n
Twitter: https://twitter.com/BitcoinUpdate2\n\n
Regards Anurag Gothi
""".format(email, coin.upper(), coin.upper(), price)

    # Stablishing the gmail sever to send mails
    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    # Login using gmail account
    server.login(msg['From'], password)

    # sending the mail
    server.sendmail(msg['From'], msg['To'], message.encode('utf-8'))

    server.quit()

    print('Emergency Update Sent\n\n')
