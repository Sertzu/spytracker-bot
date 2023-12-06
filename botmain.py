import time
import os
from datetime import datetime

import telegram
import yfinance as yf

stockup = u"\U0001f4c8"
stockdown = u"\U0001f4c9"

def getaverages():
    print("Getting Averages")
    data = yf.download(tickers="^GSPC", period="200d", interval="1d")
    data200d = list(data.Close)
    SMA200d = sum(data200d)/len(data200d)
    data5d = data200d[-5:]
    SMA5d = sum(data5d)/len(data5d)
    CURRENT = data200d[-1]
    print("Got Averages")
    return SMA200d, SMA5d, CURRENT


def main():
    time.sleep(60)
    print("Trying to get Token!")
    token = os.getenv('BOT_TOKEN')
    if token is None:
        with open("token", 'r') as file:
            token = file.read()
    print("Token is:")
    print(token)
    bot = telegram.Bot(token=token)
    print("Starting...")
    announcement = 0
    while True:
        currentHour = datetime.now().hour
        if currentHour == 21 and announcement == 0:
            SMA200d, SMA5d, CURRENT = getaverages()
            SMA200d = round(SMA200d, 2)
            SMA5d = round(SMA5d, 2)
            CURRENT = round(CURRENT, 2)
            if SMA200d >= CURRENT:
                bot.send_message(chat_id="@SP_SMA_TRACKER",
                                 text=f"{stockdown} {stockdown} {stockdown}\n\nCurrent Mode: HOLD CASH\n\nSMA200D: {SMA200d} pts\nSMA5D: {SMA5d} pts\nCURRENT: {CURRENT} pts",
                                 parse_mode=telegram.ParseMode.HTML)
            else:
                bot.send_message(chat_id="@SP_SMA_TRACKER",
                                 text=f"{stockup} {stockup} {stockup}\n\nCurrent Mode: BUY LETF\n\nSMA200D: {SMA200d} pts\nSMA5D: {SMA5d} pts\nCURRENT: {CURRENT} pts",
                                 parse_mode=telegram.ParseMode.HTML)
            announcement = 1
        else:
            print("Waiting...")
            time.sleep(600)


if __name__ == "__main__":
    main()