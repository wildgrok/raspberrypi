#smtpserver = "smtp.mail.yahoo.com, 465"
fromaddress = str('jbesad@yahoo.com')  
toaddress = str('jbesad@yahoo.com')
username = str('jbesad@yahoo.com')  
password = str('mzamaakovmkxqxeg')
subject = "this is the subject"
message = "test"

def sendmail(toaddress, fromaddress, subject, message, password):
    #Module for sending emails
    import smtplib
    from email.mime.text import MIMEText
    msg = MIMEText(message, 'plain')
    msg['From'] = fromaddress
    msg['To'] = toaddress
    msg['Subject'] = subject
    text = msg.as_string()
    server = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465)
    server.login(fromaddress,password)
    server.sendmail(fromaddress, toaddress, text)
    server.quit()  


sendmail (toaddress, fromaddress, subject, message, password)
