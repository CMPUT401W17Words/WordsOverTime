
import smtplib
def SendWordsOverTimeEmail(emailTo, htmlLink, date):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("WordsOverTimeProject@gmail.com", "Words1234")
    msg = "\r\n".join([
        "From: WordsOverTimeProject@gmail.com",
      "To: %s" % emailTo,
      "Subject: WordsOverTime request complete!",
      "",
      "Your request submitted on %s has been completed, and you can see your data and download your CSV files at: %s" % (date, htmlLink)
    ])    
    server.sendmail("YOUR EMAIL ADDRESS", emailTo, msg)
    server.quit()
    
    
SendWordsOverTimeEmail("dmhamilt@ualberta.ca", "https://www.google.com", "January 1st")
