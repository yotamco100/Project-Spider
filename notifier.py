# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from pushbullet import PushBullet
import time
from datetime import datetime
import logging
import twitter

#save logs
logging.basicConfig(filename="KyleNotifier-Log.txt", level=logging.DEBUG)

logging.info("Starting up!")
print("[{}] Starting up!".format(datetime.now()))

#twitter authentication
twitter_consumer_key = '' #YOUR KEYS HERE
twitter_consumer_secret = '' #YOUR KEYS HERE
twitter_access_token = '' #YOUR KEYS HERE
twitter_access_secret = '' #YOUR KEYS HERE
twitter = twitter.Api(consumer_key=twitter_consumer_key, consumer_secret=twitter_consumer_secret, access_token_key=twitter_access_token, access_token_secret=twitter_access_secret)
#authenticate with Twitter Apps

#my pushbullet token
pb = PushBullet("") #YOUR KEYS HERE
DMAlert = "THIS IS AN AUTOMATED MESSAGE FROM TECH'S SPIDERMONITOR\n--------------------------------------------------------\nThe counter's code has been erased from http://spidernation.net/."
print(DMAlert)

#website interaction
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7' #user agent just so bs4 won't be a cunt
url = "http://spidernation.net" # url to pull from
headers={'User-Agent':user_agent} #dictionary that Requests can read
response = requests.get(url,headers=headers) #open the requested webpage
soup = BeautifulSoup(response.text, "lxml") #create a soup object of the response
counterCheck = soup.find("p", { "class" : "date1" })

#loop for getting future changes
while(True):
    try:
        print("[{}] Checking for changes...".format(datetime.now()))
        logging.info("Checking...")
        response = requests.get(url,headers=headers) #open the requested webpage
        soup = BeautifulSoup(response.text, "lxml") #create a soup object of the response

        counterCheck2 = soup.find("p", { "class" : "date1" })
        if (counterCheck2 != counterCheck):
            print("[{}] Change detected! Pushing red alert to the group...".format(datetime.now()))
            logging.info("Changes Found! Pushing...")
            push = pb.push_link("SpiderNation Counter Update", "http://spidernation.net")
            twitter.PostDirectMessage(DMAlert, screen_name="YOUR FRIEND HERE")
            break
        elif (counterCheck2 == None): #this was done just in case if the counter changes OR disappears completely, even though it's probably not necessary
            print("[{}] Change detected! Pushing red alert to the group...".format(datetime.now()))
            logging.info("Changes Found! Pushing...")
            push = pb.push_link("SpiderNation Counter Update", "http://spidernation.net")
            twitter.PostDirectMessage(DMAlert, screen_name="YOUR FRIEND HERE")
            break
        else:
            print("[{}] Nothing found, 15 mins to next check.".format(datetime.now()))
            logging.info("Nothing found, 15 mins to next check.")
    except:
        print("Error occurred, trying in another 2.5 mins...")
        logging.info("Error occurred, trying in another 2.5 mins...")
        time.sleep(150)
        continue
    time.sleep(900)
