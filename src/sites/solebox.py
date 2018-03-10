from __future__ import absolute_import, division, print_function
import requests, time, random, string, os
from bs4 import BeautifulSoup
import time
import datetime
import sys
import os
import webbrowser
import threading
import getpass
  
# Define constants  
NUM_CART_ATTEMPTS = 10
STOCK_QUERY_DELTA = 10 # seconds
  
def isInStock(s, link, aid):
  # Parse webpage 
  pageSource  = s.get(link)
  isAvailable = BeautifulSoup(pageSource.text, "html.parser").find('a', {'id': aid}).parent.get('class')
  
  # Get the availability of the shoe
  if "inactive" in isAvailable:
    print("Out of Stock")
    return False
  else:
    print("In Stock")
    return True

def addToCart(s, stoken, cnid, aid, anid, parentid, panid):
  result       = None
  attemptCount = 0

  while result is None and attemptCount < NUM_CART_ATTEMPTS:
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
      print('Added to cart!')
      return True
    else:
      attemptCount += 1
      print('Error adding to cart, trying again...')

  if result != 'OK':
    # Quit if it didn't work
    #print ("ERROR: Failed to add to cart after", NUM_CART_ATTEMPTS, "attempts")
    return False

def bot():
    headers = {
                'GBer-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate, sdch, br',
                'Accept-Language': 'en-GB,en;q=0.8',
                'Upgrade-Insecure-Requests': '1'
            }

    # Get input args
    mode     = sys.argv[5]
    link     = sys.argv[6]
    aid      = int(sys.argv[4])
    login    = sys.argv[1]
    password = sys.argv[2]
    timeout  = sys.argv[3]
  
    # Start a web session
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
  
    # Login
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

    # Parse webpage 
    r = s.get(link)
    stoken   = BeautifulSoup(r.text, "html.parser").find('input', {'name': 'stoken'}).get('value')
    cnid     = BeautifulSoup(r.text, "html.parser").find('input', {'name': 'cnid'}).get('value')
    anid     = BeautifulSoup(r.text, "html.parser").find('input', {'name': 'anid'}).get('value')
    parentid = BeautifulSoup(r.text, "html.parser").find('input', {'name': 'parentid'}).get('value')
    panid    = BeautifulSoup(r.text, "html.parser").find('input', {'name': 'panid'}).get('value')

    # Decide when to attempt to cart
    if timeout != "now":
      tmp = timeout.split(':')

      # Get the release time in seconds (from start of day)
      releaseTime = {}
      releaseTime['hours']        = int(tmp[0])
      releaseTime['minutes']      = int(tmp[1])
      releaseTime['seconds']      = int(tmp[2])
      releaseTime['totalseconds'] = (3600*releaseTime['hours']) + (60*releaseTime['minutes']) + (releaseTime['seconds'])

      # Get current date
      now  = datetime.datetime.now()
      now  = datetime.date(now.year, now.month, now.day)

      # Calculate absolute release time, in seconds
      releaseTime['absolute']  = time.mktime(now.timetuple()) + releaseTime['totalseconds']
      
      # Calculate difference between release time and current time
      diff = releaseTime['absolute'] - time.time() + 0.001
  
      # Sleep until the shoes release
      print ('Sleeping for ' + str(diff))
      time.sleep(diff)
      print ("Started bot at " + str(datetime.datetime.now()))

    # Set the web URL to the sneakers
    s.headers.update({
                'Origin': 'https://www.solebox.com',
                'Referer': link,
            })

    # Attempt to cart sneakers in release mode (makes 10 attempts)
    if mode == 'release':
      result = addToCart(s, stoken, cnid, aid, anid, parentid, panid)
      if result == False:
        print ("ERROR: Failed to add to cart after several attempts")
        return

    # Attempt to cart sneakers in restock mode (checks if shoe is available every so often)
    elif mode == 'restock':
      result = None
      while isInStock(s, link, aid) == False:
        time.sleep(STOCK_QUERY_DELTA)

      result = addToCart(s, stoken, cnid, aid, anid, parentid, panid)
      if result == False:
        print ("ERROR: Failed to add to cart after several attempts")
        return

    # Invalid Mode
    else: 
      print ("ERROR: Invalid mode. Must be release or restock.")

    # If the script ever makes it here, we carted
    # successfully. So, go to the cart and checkout
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

    # Control web browser
    webbrowser.open_new_tab(r.url)
    print ('Opening paypal...')
    print ("If your browser hasen't opened, paste this link:")
    print (r.url)

# Start Bot
bot()
  
time.sleep(500)