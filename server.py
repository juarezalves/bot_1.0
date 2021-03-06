# -*- coding: utf-8 -*-

from flask import Flask, request
import requests
import codecs
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

app = Flask(__name__)
FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = '!Rsf159753#'# <paste your verify token here>
PAGE_ACCESS_TOKEN = 'EAAEbmIHBis8BAH99ZA9kV4iZCwSuZCvHinF3RkPRQKoIiAWVTkWdwaWvotntR5Ge0oHpSrnhDGPC4DwtDnN9AbpIUn2kmmN7qZCjZCYLWcNPrDFTepdhNk7eZCjZC3hm9O1yrFBZANCofjcPxksOnlGobgHLbyg2sZCPOBVcbnkBABAZDZD'

def get_bot_response(message, bot): #"""This is just a dummy function, returning a variation of what the user said. Replace this function with one connected to chatbot."""
    resp = bot.get_response(message)
    app.logger.info(resp)
    if float(resp.confidence) > 0.5:
        return str(resp)     #"This is a dummy response to '{}'".format(message)
    else:
        return "Não entendi..."

def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"

def respond(sender, message, bot): #"""Formulate a response to the user and pass it on to a function that sends it."""
    response = get_bot_response(message, bot)
    send_message(sender, response)

def is_user_message(message): #"""Check if the message is a message from the user"""
    return (message.get('message') and message['message'].get('text') and not message['message'].get("is_echo"))

@app.route("/webhook", methods=['GET','POST'])

def listen(): #"""This is the main function flask uses to listen at the `/webhook` endpoint"""
    bot = ChatBot('ada01')
    bot.set_trainer(ListTrainer)
    for arq in os.listdir('arq'):
        corpus = codecs.open('arq/' + arq, 'r','iso8859-1').readlines()
        bot.train(corpus)

    if request.method == 'GET':
        return verify_webhook(request)
    if request.method == 'POST':
        payload = request.json
        event = payload['entry'][0]['messaging']
        for x in event:
            if is_user_message(x):
                text = x['message']['text']
                sender_id = x['sender']['id']
                respond(sender_id, text, bot)
    return "ok"


def send_message(recipient_id, text): # """Send a response to Facebook"""
    app.logger.info(text)
    payload = {'message': {'text': text}, 'recipient': {'id': recipient_id}, 'notification_type': 'regular'}

  #  payload = ({"recipient": {"id": recipient_id },
	#		"message": { "text": "teste botão resposta", "quick_replies":[{ "content_type":"text", "title":"Escolher pizzas", "payload":"<POSTBACK_PAYLOAD>" },
	#		{"content_type": "text","title": "Escolher bebidas","payload": "<POSTBACK_PAYLOAD>" } ] } })


    auth = {'access_token': PAGE_ACCESS_TOKEN}
    response = requests.post(FB_API_URL, params=auth, json=payload)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
    port = int (os.environ.get ("PORT", 5000))
    app.run (host='0.0.0.0', port=port)
