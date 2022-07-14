from datetime import date
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from datetime import datetime
my_date = datetime.now()

mail_content = 'Ringboy Notification - Someone is at the door - ' + my_date.isoformat()

#The mail addresses and password
sender_address = 'sender_address'
sender_pass = 'pass'
receiver_address = 'recv_address'
#Setup the MIME
message = MIMEMultipart()
message['From'] = "Ringboy <" + sender_address + ">"
message['To'] = receiver_address
message['Subject'] = mail_content
#The body and the attachments for the mail
message.attach(MIMEText(mail_content, 'plain'))
#Create SMTP session for sending the mail
session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
session.starttls() #enable security
session.login(sender_address, sender_pass) #login with mail_id and password
text = message.as_string()
session.sendmail(sender_address, receiver_address, text)
session.quit()
print('Mail Sent')