import redis
import sys
import telegram
import time
import os
token = os.environ['TELEGRAM_TOKEN']
bot = telegram.Bot(token)

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
