from dataclasses import dataclass
from platform import platform
from matplotlib.pyplot import show
from more_itertools import last
from data_require import acquireMetIndex
from datetime import datetime,timedelta
import schedule
import time
import pandas as pd
import json
from myfunctionpool import *



symbolList = ['BTCUSDT','ETHUSDT','DOGEUSDT','ZECUSDT','LTCUSDT','ETCUSDT','BCHUSDT','XMRUSDT','DASHUSDT',
    'CRVUSDT','AAVEUSDT','COMPUSDT','MKRUSDT','UNIUSDT','SUSHIUSDT','DYDXUSDT','CAKEUSDT','CVXUSDT','LRCUSDT','RUNEUSDT',
    'ETHUSDT','BNBUSDT','AVAXUSDT','MATICUSDT','SOLUSDT','NEARUSDT','ADAUSDT','DOTUSDT','ATOMUSDT','ICPUSDT','TRXUSDT','ALGOUSDT',
    'LINKUSDT','ARUSDT','FILUSDT','HNTUSDT','GMTUSDT','THETAUSDT','AUDIOUSDT','GRTUSDT',
    'MANAUSDT','APEUSDT','SANDUSDT','AXSUSDT','GALAUSDT','ENJUSDT']




str_outputDir = '/Users/lucyzhang/Desktop/find crypto alphas/output/'
str_inputDir = '/Users/lucyzhang/Desktop/find crypto alphas/output/index.csv'

def writedata(picktime, NowPrice, powIndex, defiIndex, PlatformIndex, Web3Index, APPIndex, path = str_outputDir):
    NowPrice = json.dumps(NowPrice)
    data= [picktime, powIndex, defiIndex, PlatformIndex, Web3Index, APPIndex, NowPrice] 
    data = pd.DataFrame(data)
    data.to_csv(path + 'index.csv')



def readdata(path  = str_inputDir):
    dataread = pd.read_csv(path)
    data = dataread.values.tolist()
    powIndex = float(data[1][1])
    defiIndex = float(data[2][1])
    PlatformIndex = float(data[3][1])
    Web3Index = float(data[4][1])
    APPIndex = float(data[5][1])
    prices = data[6][1]
    prices = json.loads(prices)
    return prices,powIndex, defiIndex, PlatformIndex, Web3Index, APPIndex




def powIndexPct(Last,Now):
    inLast = Last[0:9]
    inNow = Now[0:9]
    pct = 0.3*(inNow[0]-inLast[0])/inLast[0] + 0.2 * (inNow[1]-inLast[1])/inLast[1] +\
        0.1*(inNow[2]-inLast[2])/inLast[2] + 0.1*(inNow[3]-inLast[3])/inLast[3] + \
            0.1*(inNow[4]-inLast[4])/inLast[4] + 0.1*(inNow[5]-inLast[5])/inLast[5] + 0.1*(inNow[6]-inLast[6])/inLast[6] +\
                0.1*(inNow[7]-inLast[7])/inLast[7] + 0.1*(inNow[8]-inLast[8])/inLast[8]

    return pct

def IndexPct(Last,Now,fromindex,toindex):
    inLast = Last[fromindex:toindex]
    inNow = Now[fromindex:toindex]
    pct = 0
    for i in range(len(inLast)):
        pct += (inNow[i]-inLast[i])/inLast[i]
    return pct/len(inLast)

def pctConvert(Pct):
    Pct = round(Pct*100,2)
    if Pct <= 0:
        Pct = str(Pct) + '%'
    else:
        Pct = '+'+str(Pct) + '%'
    return Pct

def showPct(symbolList):
    LastPrice,powIndex, defiIndex, PlatformIndex, Web3Index, APPIndex = readdata()
    timenow = datetime.now()
    picktime = timenow - timedelta(hours=11)
    try:
        NowPrice = acquireMetIndex(symbolList,str(picktime))
    except Exception as e:
        print(e)
        time.sleep(120)
        NowPrice = acquireMetIndex(symbolList,str(picktime))
    
    BTCPct = (NowPrice[0]-LastPrice[0])/LastPrice[0]
    BTCPctstr = pctConvert(BTCPct)

    ETHPct = (NowPrice[1]-LastPrice[1])/LastPrice[1]
    ETHPctstr = pctConvert(ETHPct)

    powPct = powIndexPct(LastPrice,NowPrice)
    powIndex *= 1+powPct
    powPctstr = pctConvert(powPct)

    defiPct = IndexPct(LastPrice,NowPrice,9,20)
    defiIndex *= 1+defiPct
    defiPctstr = pctConvert(defiPct)

    platformPct = IndexPct(LastPrice,NowPrice,20,32)
    PlatformIndex *= 1+platformPct
    platformPctstr = pctConvert(platformPct)

    web3Pct = IndexPct(LastPrice,NowPrice,32,40)
    Web3Index *= 1+web3Pct
    web3Pctstr = pctConvert(web3Pct)

    APPPct = IndexPct(LastPrice,NowPrice,40,46)
    APPIndex *= 1+APPPct
    APPPctstr = pctConvert(APPPct)
    writedata(picktime, NowPrice, powIndex, defiIndex, PlatformIndex, Web3Index, APPIndex)
    utcTime = datetime.utcnow()
    bot_text1 = "UTC Time: {}\nBenchmark\nBTC: {:.2f} ({}, hourly)\nETH: {:.2f} ({}, hourly)\n\nSectors\nPoW Index: {:.2f} ({}, hourly)\n".format(utcTime.strftime('%Y/%m/%d %H:%M'),NowPrice[0],BTCPctstr,NowPrice[1],ETHPctstr,powIndex,powPctstr)
    bot_text2 = "Defi Index: {:.2f} ({}, hourly)\nPlatform Index: {:.2f} ({}, hourly)\nWeb3 Index: {:.2f} ({}, hourly)\nNFT & Gaming Index: {:.2f} ({}, hourly)".format(defiIndex,defiPctstr,PlatformIndex,platformPctstr,Web3Index,web3Pctstr,APPIndex,APPPctstr)
    print("---------------------------------------------------------------------------------------------")
    print(bot_text1+bot_text2)
    print("---------------------------------------------------------------------------------------------")
    return bot_text1+bot_text2

if __name__ == "__main__":
    timenow = datetime.now()
    picktime = timenow - timedelta(hours=11)
    NowPrice = acquireMetIndex(symbolList,str(picktime))
    print(NowPrice)
    print(NowPrice[0:9])
    print(NowPrice[9:20])
    print(NowPrice[20:33])
    print(NowPrice[33:41])
    print(NowPrice[41:47])





