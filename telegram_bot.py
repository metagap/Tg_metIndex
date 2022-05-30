from asyncore import dispatcher
import requests
from config import tel_api
from telegram.ext import *
from telegram import *
from metaIndex import *


def job(symbolList):
    base_url = 'https://api.telegram.org/bot'+ tel_api + '/sendMessage'
    delete_url = 'https://api.telegram.org/bot'+ tel_api + '/deleteMessage'
    index_text = showPct(symbolList)

    parameters = {
        'chat_id' : '-1001658360515',
        'text' : index_text
    }

    resp = requests.get(base_url,parameters)
    resp = resp.json()
    resp = resp["result"]["message_id"]

    time.sleep(3500)
    delete_parameters = {
        'chat_id' : '-1001658360515',
        'message_id': resp
    }
    requests.get(delete_url,delete_parameters)


schedule.every().hours.at(":00").do(job,symbolList)

while True:
    schedule.run_pending()
    time.sleep(1)



