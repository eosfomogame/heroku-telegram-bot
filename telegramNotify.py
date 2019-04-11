import redis
import sys
import telegram
import time
import os
print("sys.argv[0])
print("sys.argv[1])
print("sys.argv[2])
bot = telegram.Bot(token="774069694:AAF9d0Rzrh3qpWEwBYIrH5m6D_6wslSC5_M")

x=0
y=0
while x==0 and y<60:
    try:
        bot.send_photo(chat_id="-1001389647670", photo=open(sys.argv[1], 'rb'),caption=sys.argv[2]+"\n"+sys.argv[3])
        x=1
    except Exception as e:
        print(e)
        y+=1#mi 
        time.sleep(1)
        
        
os.remove(sys.argv[1])  
