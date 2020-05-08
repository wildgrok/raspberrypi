#Sends email when Ip address changes
outfile = r"/home/pi/Desktop/ipchecker.out"

def writelog2(data):
    
    with open((outfile), 'a+') as f:
        f.write(data + '\n')

def sendnewip(ipaddr, toaddress, fromaddress, password):
    #Module for sending emails
    import smtplib
    from email.mime.text import MIMEText
    text = "Your new IP is: " + str(ipaddr)
    msg = MIMEText(text, 'plain')
    msg['From'] = fromaddress
    msg['To'] = toaddress
    msg['Subject'] = "IP Address Change"
    text = msg.as_string()
    #server = smtplib.SMTP(smtpserver, 587)
    #server = smtplib.SMTP("smtp.mail.yahoo.com",587)
    server = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465)
    server.login(fromaddress,password)
    server.sendmail(fromaddress, toaddress,text)
    server.quit()  

def updateipstore(ipaddr, ipstorepath):
    #Writes Current IP Address to the IP Store file
    currentip = open(ipstorepath, 'w')
    currentip.write(ipaddr)
    currentip.truncate()
    currentip.close()
    
def check_ip():
    
    import requests, os, sys
    #smtpserver = "smtp.mail.yahoo.com"
    fromaddress = str('jbesad@yahoo.com')  
    toaddress = str('jbesad@yahoo.com')
    ipstorepath = r"/home/pi/Desktop/IPstore.txt"
    #username = str('jbesad@yahoo.com')  
    password = str('mzamaakovmkxqxeg')
    
    if os.path.exists(outfile):
        os.remove(outfile)    
    writelog2(sys.version)    
    ipaddr = requests.get("https://api.ipify.org").text    
    if os.path.isfile(ipstorepath): #test if IP Store file exists
        currentip = open(ipstorepath, 'r+') #Open IP Store file for reading
        if currentip.read() != ipaddr: #Check if IP Address received is the same what is stored in IP Store file. Code below will run if currentip does not equal IP address received from IPIFY
            currentip.close()
            updateipstore(ipaddr, ipstorepath)
            sendnewip(ipaddr, toaddress, fromaddress, password) #Send email with new IP Address
            print("Your new IP is: " + str(ipaddr))
            writelog2("Your new IP is: " + str(ipaddr))
        else: #Runs if IP Store file doesn't exist
            updateipstore(ipaddr, ipstorepath) #Used to create IP store file
            print("IP not changed: " + str(ipaddr))
            writelog2("IP not changed: " + str(ipaddr))
    
# Run program 
if __name__ == '__main__':
    check_ip()


    
    