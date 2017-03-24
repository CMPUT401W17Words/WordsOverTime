
import smtplib
def SendWordsOverTimeEmail(emailTo, htmlLinks, date):
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
    
    
SendWordsOverTimeEmail("dmhamilt@ualberta.ca", ["https://www.google.com"], "January 1st")
