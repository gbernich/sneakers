from __future__ import absolute_import, division, print_function
import requests, time, random, string, os
from bs4 import BeautifulSoup
import time
import sys
import os
import webbrowser
import threading
import getpass
  
nb = 1
  
numCartAttempts = 10
  
def bot(to,nb):
    headers = {
                'GBer-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate, sdch, br',
                'Accept-Language': 'en-GB,en;q=0.8',
                'Upgrade-Insecure-Requests': '1'
            }
    # link = input('Input solebox shoe link for thread ' + str(nb) + ':\t')
    # aid = input('Please input the size id for thread ' + str(nb) + ':\t')
    # aid = int(aid)
    # login = input('Input solebox account email for thread ' + str(nb) + '(use a different account per thread): \t')
    # password = input('Enter your solebox account password for thread ' + str(nb) + ':\t')
    link = sys.argv[5]
    aid = sys.argv[4]
    aid = int(aid)
    login = sys.argv[1]
    password = sys.argv[2]
  
    s = requests.Session()
    s.cookies.clear()
    s.headers.update(headers)
    print('Logging in....')
    r = s.get('https://www.solebox.com/en/my-account/')
    stoken = BeautifulSoup(r.text, "html.parser").find('input', {'name': 'stoken'}).get('value')
    s.headers.update({
                'Origin': 'https://www.solebox.com',
                'Referer': 'https://www.solebox.com/en/my-account/',
            })
  
    r = s.post("https://www.solebox.com/index.php?lang=1&",
                       data={
                           'stoken': stoken, 
                           'lang': '1',  
                           'cl':'user',
                           'actcontrol':'user',
                           'fnc': 'login_noredirect',
                           'lgn_usr': login,
                           'lgn_pwd': password
  
                       })
    r = s.get(link)
    stoken = BeautifulSoup(r.text, "html.parser").find('input', {'name': 'stoken'}).get('value')
    cnid = BeautifulSoup(r.text, "html.parser").find('input', {'name': 'cnid'}).get('value')
  
    anid = BeautifulSoup(r.text, "html.parser").find('input', {'name': 'anid'}).get('value')
    parentid = BeautifulSoup(r.text, "html.parser").find('input', {'name': 'parentid'}).get('value')
    panid = BeautifulSoup(r.text, "html.parser").find('input', {'name': 'panid'}).get('value')
      
  
    hour = (time.strftime("%H"))
    hour = int(hour)
    sechour = hour * 60 * 60
  
  
    min1 = (time.strftime("%M"))
    min1 = int(min1)
    secmin1 = min1 * 60
  
    sec = (time.strftime("%S"))
    sec = int(sec)
  
    total = sec + secmin1 + sechour
  
    if to != "now":
      total1 = to.split(':')
      tohour = total1[0]
      tomin = total1[1]
      tosec = total1[2]
      tohour = int(tohour)
      tomin = int(tomin)
      tosec = int(tosec)
    
      tohoursec = tohour * 60 * 60
      tominsec = tomin * 60
      totalsec = tohoursec + tominsec + tosec
    
      diff = totalsec - total
  
  
      print ('Waiting ' + str(diff))
      time.sleep(diff)
      print ("It's time! Starting bot...")
    # else continue

    s.headers.update({
                'Origin': 'https://www.solebox.com',
                'Referer': link,
            })
    result = None
    attemptCount = 0
    while result is None and attemptCount < numCartAttempts:
        r = s.post("https://www.solebox.com/index.php?lang=1&",
                           data={
                               'stoken': stoken, 
                               'lang': '1',  
                               'cnid': cnid,
                               'listtype': 'list',
                               'actcontrol': 'details',
                               'cl': "details",
                               'aid': aid,
                               'anid': anid,
                               'parentid': parentid,
                               'panid':panid,
                               'fnc':'tobasket',
                               'am':'1'
  
                           })
        if 'successfully' in r.text:
          result = 'OK'
        else:
          attemptCount += 1
          print ('Error adding to cart, trying again...')
          pass

    if result != 'OK':
      # Quit if it didn't work
      print ("ERROR: Failed to add to cart after", numCartAttempts, "attempts")
      return

    print ('Added to cart!')
  
    r = s.get('https://www.solebox.com/en/cart/')
  
    s.headers.update({
                'Origin': 'https://www.solebox.com',
                'Referer': 'https://www.solebox.com/en/cart/',
            })
  
    r = s.post("https://www.solebox.com/index.php?lang=1&",
                       data={
                           'stoken': stoken, 
                           'lang': '1',  
                           'cl':'user'
  
                       })
    print ('Checking out...')
  
  
    r = s.get('https://www.solebox.com/index.php?cl=payment&lang=1')
  
    r = s.post("https://www.solebox.com/index.php?lang=1&",
                       data={
                           'stoken': stoken, 
                           'lang': '1',  
                           'cl':'payment',
                           'actcontrol':'payment',
                           'fnc': 'validatepayment',
                           'paymentid': 'globalpaypal'
  
                       })
    webbrowser.open_new_tab(r.url)
    print ('Opening paypal...')
    print ("If your browser hasen't opened, paste this link:")
    print (r.url)
#print ('Welcome to the Solebox bot, before using this bot, you will need 1 solebox account per thread you like to run, please signup at: https://www.solebox.com/en/my-account/ and add your billing address to your account(s)')
# threads = input('How many threads would you like? \t')
threads = 1
# to = input('What time does it drop at? (in hh:mm:ss): ')
to = sys.argv[3]
bot(to,nb)
  
time.sleep(500)