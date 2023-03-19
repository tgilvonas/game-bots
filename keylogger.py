# This keylogger is for debug purposes

from pynput.keyboard import Key, Listener
import logging, json, time

print('Key logger')

listOfKeys={}
keyNumber=0
beginLogging=0
momentOfTime=0

log_dir = ""

def get_milliseconds():
    return int(round(time.time() * 1000))

def log_key(key, action):
    global listOfKeys
    global keyNumber
    global beginLogging
    global momentOfTime
    if beginLogging == 1:
        keyHappened = {
            'action': '',
            'key': '',
            'wait': 0
        }
        keyHappened['action']=action
        keyHappened['key']=str(key)
        keyHappened['wait']=get_milliseconds()-momentOfTime
        momentOfTime=get_milliseconds()
        listOfKeys['key'+str(keyNumber)]=keyHappened
        keyNumber+=1

def on_press(key):
    global listOfKeys
    global momentOfTime
    if str(key)=="'q'":
        global beginLogging
        beginLogging=1
        momentOfTime=get_milliseconds()
    if key == Key.esc:
        with open('logged_keys.json', 'w') as f:
            print(listOfKeys)
            json.dump(listOfKeys, f)
        return False
    #logging.info(" pressed: "+str(key))
    log_key(key, 'pressed')

def on_release(key):
    log_key(key, 'released')

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
