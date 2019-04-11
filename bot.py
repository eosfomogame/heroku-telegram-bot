# -*- coding: utf-8 -*-
import requests
import json
from time import sleep
import os #delete file, rename file
import matplotlib.pyplot as plt
import csv
import subprocess 
#from datetime import datetime #time




def lastlinedata(par=0,file='data.txt'):   #0 first element 1 second element
    with open(file, 'r') as f:
        lines = f.read().splitlines()
        last_line = (lines[-1]).split(',', 1)
        return last_line[par]

if os.path.isfile('data.txt'):
    lastline_rec=lastlinedata(par=1)
    os.remove("data.txt")
    file = open('data.txt','a')
    file.writelines("0,"+str(lastline_rec) + '\n')
    file.close()
    
    
if os.path.isfile('data.txt'):
    if float(lastline_rec)>0:
        buy=float(lastline_rec)
        sell=0
        rems=buy
    elif float(lastline_rec)<0:
        buy=0
        sell=-float(lastline_rec)
        rems=float(lastline_rec)
    
else:
    sell=0
    buy=0
    rems=0
silent_trades=buy-sell     
tid=0
tidControl=0

maxprice=0
minprice=0


number=0



url = "https://api.bitfinex.com/v1/trades/btcusd"





while True:
    try:
        response = requests.request("GET", url)
        j=response.json()
    except Exception as e:
        print("type error: " + str(e))


     
    for x in range(0,100):

        if j[x]['type']=="sell" and tid < int(j[x]['tid']):
            sell=sell+float(j[x]['amount'])

        if j[x]['type']=="buy" and tid < int(j[x]['tid']):
            buy=buy+float(j[x]['amount'])

    number=number+1
    seconds=10
    tid=int(j[0]['tid'])
    lastpriceBTC=float(j[0]['price'])
    if rems==0 or rems==float(lastline_rec):                         
        semilastpriceBTC=lastpriceBTC
        
    if tid > tidControl:
        tidControl=int(j[0]['tid'])
        print(tid)


        if maxprice < (buy-sell):
            maxprice=buy-sell

        if minprice > (buy-sell):
            minprice=(buy-sell)


                        
        print("total: "+str(sell+buy))
        print("total sell: "+str(sell/(sell+buy))+"  "+str(sell))
        print("total buy: "+str(buy/(sell+buy))+"  "+str(buy))
        print("minspread: "+str(minprice)+" maxspread: "+str(maxprice))
        print("spread: "+str(buy-sell))
        print("variation: "+str((buy-sell) - rems))
        print("----------------------------------------")



       
        if (buy-sell) - rems > 30:  
            
            seconds=6
            silent_trades=buy-sell  

        elif (buy-sell) - rems < -30:
            
            seconds=5
            silent_trades=buy-sell  




        
            
            
            



        file = open('data.txt','a')
        file.writelines(str(number)+","+str(buy-sell) + '\n')
        file.close()

        plt.ion()
        x = []
        y = []


        with open('data.txt','r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            for row in plots:
                x.append(int(row[0]))                    
                y.append(float(row[1]))

        
            



        #color chart
        if (buy-sell) > rems:
            color='g.--'
        elif (buy-sell) < rems:
            color='r.--'
        else:
            color='k.--'

        plt.clf() 
        #plt.plot(x,y, label='Loaded from file!')
        plt.plot(x, y, color, label="{0:.2f}".format((buy-sell)), linewidth=0.5) #https://matplotlib.org/2.1.1/api/_as_gen/matplotlib.pyplot.plot.html
        plt.pause(0.0001)
        plt.xlabel('Time')
        plt.pause(0.0001)
        plt.ylabel('BTC')
        plt.pause(0.0001)
        
        if (buy-sell)-rems > 100 and rems!=0:
            plt.annotate("HUGE\nPUMP!", (x[-1],y[-1]), xytext=(x[-1], y[-2]),arrowprops=dict(facecolor="g"))
        elif (buy-sell)-rems < -100 and rems!=0:
            plt.annotate("HUGE\nDUMP!", (x[-1],y[-1]), xytext=(x[-1], y[-2]),arrowprops=dict(facecolor="r"))
        plt.pause(0.0001)   
        plt.title("min: "+"{0:.2f}".format(minprice)+" max: "+"{0:.2f}".format(maxprice))
        plt.pause(0.0001)
        plt.grid(True) #griglia
        plt.pause(0.0001)
        plt.legend() #label
        plt.draw()
        plt.pause(0.0001)
        plt.savefig('data.png')
        plt.pause(0.0001)
        if seconds==6:          
            os.rename('data.png', 'data'+str(x[-1])+'.png')
            subprocess.Popen(['python',"telegramNotify.py",'data'+str(x[-1])+'.png',"Buy "+"{0:.0f}".format((buy-sell) - rems)+" BTC","BTC price: "+str(lastpriceBTC)+" ({0:.2f}".format((lastpriceBTC/semilastpriceBTC*100)-100)+"%)"],shell=True)                                                               


        elif seconds==5:                       
            os.rename('data.png', 'data'+str(x[-1])+'.png')
            subprocess.Popen(['python',"telegramNotify.py",'data'+str(x[-1])+'.png',"Sell "+"{0:.0f}".format((buy-sell) - rems)+" BTC","BTC price: "+str(lastpriceBTC)+" ({0:.2f}".format((lastpriceBTC/semilastpriceBTC*100)-100)+"%)"],shell=True)     #shell True non mostra la shell                                                              
            
        elif (buy-sell) - silent_trades > 250:
            os.rename('data.png', 'data'+str(x[-1])+'.png')
            subprocess.Popen(['python',"telegramNotify.py",'data'+str(x[-1])+'.png',"Buy silent "+"{0:.0f}".format((buy-sell) - silent_trades)+" BTC","BTC price: "+str(lastpriceBTC)+" ({0:.2f}".format((lastpriceBTC/semilastpriceBTC*100)-100)+"%)"],shell=True)     #shell True non mostra la shell-->                                                          
            silent_trades=buy-sell    
        elif (buy-sell) - silent_trades < -250:       
            os.rename('data.png', 'data'+str(x[-1])+'.png')
            subprocess.Popen(['python',"telegramNotify.py",'data'+str(x[-1])+'.png',"Sell silent "+"{0:.0f}".format((buy-sell) - silent_trades)+" BTC","BTC price: "+str(lastpriceBTC)+" ({0:.2f}".format((lastpriceBTC/semilastpriceBTC*100)-100)+"%)"],shell=True)                                                                  
            silent_trades=buy-sell
        
        
        rems=(buy-sell)
        semilastpriceBTC=lastpriceBTC
            
    plt.pause(seconds)
