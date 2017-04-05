
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

#depreciated email function, kept as example.
def SendWordsOverTimeEmail(emailTo, htmlLinks, date, csvList):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("WordsOverTimeProject@gmail.com", "Words1234")
    msgbody = "Your request submitted on %s has been completed, and you can see your data and download your CSV files at:\n"
    for link in htmlLinks:
        msgbody = msgbody + link+"\n"
    msg = "\r\n".join([
        "From: WordsOverTimeProject@gmail.com",
      "To: %s" % emailTo,
      "Subject: WordsOverTime request complete!",
      "",
      msgbody
    ])    
    server.sendmail("YOUR EMAIL ADDRESS", emailTo, msg)
    server.quit()
    
#send_mail(["dmhamilt@ualberta.ca"], ["https://www.google.com", "http://www.sharktank.com"], ["tests.py", "urls.py"],[],[])    
def send_mail(send_to_list, htmlLinks, files=None, errors=None, matrices=None):
    if isinstance(send_to_list, str):
        send_to_list = [send_to_list]
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("WordsOverTimeProject@gmail.com", "Words1234")
    msgbody = "Your request  has been completed, and you can see your data and download your CSV files at:\n"
    for link in htmlLinks:
        msgbody = msgbody + link+"\n"

    msg = MIMEMultipart()
    msg['From'] = "WordsOverTimeProject@gmail.com"
    msg['To'] = ', '.join(send_to_list)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "WordsOverTime request complete!"

    # Description of errors in the message body
    msgbody = msgbody + "\n"
    if (errors != None):
        for analysis,error in errors.items():
            if (error != None):
                for e in error:
                    msgbody = msgbody + "Error in analysis " + analysis + ": " + e + "\n"

    for f in files or []:
        ff = open(f)
        part = MIMEText(ff.read())
        part.add_header('Content-Disposition', 'attachment', filename = f)
        msg.attach(part)
    
    # Attach a zip folder containing matrices from cos distance and N closest neighbors analyses    
    for f in matrices or []:
        ff = open(f)
        part = MIMEText(ff.read())
        part.add_header('Content-Disposition', 'attachment', filename = f)
        msg.attach(part)
                
    msg.attach(MIMEText(msgbody))
    for send_to in send_to_list:
        server.sendmail("WordsOverTimeProject@gmail.com", send_to, msg.as_string())
    server.quit()

#send_mail(["dmhamilt@ualberta.ca"], ["https://www.google.com", "http://www.sharktank.com"], ["tests.py", "urls.py"])

def send_error_mail(send_to_list, error_type=''):
    if isinstance(send_to_list, str):
        send_to_list = [send_to_list]
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("WordsOverTimeProject@gmail.com", "Words1234")
    msgbody = "Unfortuneately, your %s request failed. Plase contact support, or retry. Maybe you made a spelling mistake?" % error_type

    msg = MIMEMultipart()
    msg['From'] = "WordsOverTimeProject@gmail.com"
    msg['To'] = ', '.join(send_to_list)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "WordsOverTime request failed."
    for send_to in send_to_list:
        server.sendmail("WordsOverTimeProject@gmail.com", send_to, msg.as_string())
    server.quit()