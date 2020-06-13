__author__ = 'python'
# Schedule Library imported
import schedule
import time
import send_mail
import web_get_page
import web_get_page_world
import ipchecker
import subprocess




# Functions setup

def copy_to_website():
    rc = subprocess.call("/var/www/html/upload.sh")

def everyhour():
    print("I am running every hour")

def sendmail():
    send_mail.sendmail()
    
def get_data():
    print('getting data USA')
    web_get_page.get_data()
    
def get_data_spain():
    print('getting data Spain')
    web_get_page_world.get_data()    
    
def check_ip():
    ipchecker.check_ip()
    
# Task scheduling
# After every 10mins geeks() is called.
#schedule.every(1).minutes.do(geeks)
#schedule.every(1).minutes.do(sendmail)
#schedule.every(60).minutes.do(get_data)
#schedule.every(1).minutes.do(check_ip)

schedule.every().day.at("00:30").do(check_ip)
schedule.every().day.at("06:30").do(get_data)
schedule.every().day.at("07:00").do(get_data_spain)
schedule.every().day.at("07:30").do(copy_to_website)



# # After every hour geeks() is called.
schedule.every().hour.do(everyhour)
#
# # Every day at 12am or 00:00 time bedtime() is called.
# schedule.every().day.at("00:00").do(bedtime)
#
# # After every 5 to 10mins in between run work()
# schedule.every(5).to(10).minutes.do(work)
#
# # Every monday good_luck() is called
# schedule.every().monday.do(good_luck)
#
# # Every tuesday at 18:00 sudo_placement() is called
# schedule.every().tuesday.at("18:00").do(sudo_placement)

# Loop so that the scheduling task
# keeps on running all time.
while True:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)