__author__ = 'python'

# Schedule Library imported
import schedule
import time
import send_mail
import web_get_page
import ipchecker

# Functions setup

def everyhour():
    print("I am running every hour")

def sendmail():
    send_mail.sendmail()
    
def get_data():
    web_get_page.get_data()
    
def check_ip():
    ipchecker.check_ip()
    
# Task scheduling
# After every 10mins geeks() is called.
#schedule.every(1).minutes.do(geeks)
#schedule.every(1).minutes.do(sendmail)
#schedule.every(2).minutes.do(get_data)
schedule.every().day.at("00:00").do(check_ip)
schedule.every().day.at("08:00").do(get_data)
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