from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import datetime
import json

#GPT-3 AI testing
import os
import openai


updater = Updater("5780822067:AAEM7xgo635DC4U-_VbiR7kGdEwFGiqglt4",
                  use_context=True)
  
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
       "Hello, welcome to the COVID-19 response bot. Please enter your questions / concerns to allow us to direct you to the right channels.")
    print('user started the bot!')
    

def help(update: Update, context: CallbackContext):
    #tells the user what the bot is about and what they can do with it
    update.message.reply_text("This bot can be used for questions / queries regarding COVID-19.")

  
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)

def texts(update: Update, context: CallbackContext):
    #receive text input from user and save it as text
    text = update.message.text.lower()

    openai.api_key = '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' # my openai key

    response = openai.Completion.create(
      model="text-davinci-002",
      prompt="Classify the urgency of a message as 0,1,2,3\n\nDefinition: Spam, nonsense messages. Unrelated to health issues.\nMessage: “fjakljfklasjfsadasl”\nUrgency: 0 \n\n##\n\nDefinition: User needs help but it is not time-critical at all, users can read the answers themselves on the Ministry of Health website\nMessages:  “what is covid”, “what is the number of cases today”\nUrgency: 1\n\n##\n\nDefinition: User needs help but help can be provided through an automated chatbot / text\nMessages: “I have covid can I go out\", “I am coughing what medicine can i get”, “I have covid but I share room with my brother where do I go”\nUrgency: 2\n\n##\nDefinition: User has serious issues that require the immediate attention of a call centre\nMessages: \"I cannot breathe, what do i do”, “My throat hurts… where can I go”\nUrgency: 3\n\nUser message: " + text + "\nUrgency:\n\n\n\n",
      temperature=0.7,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    response_dict = json.loads(str(response))
    print('response dict is', response_dict)
    urgency = int(response_dict['choices'][0]['text'])
    print(urgency)

    if urgency == 0:
        update.message.reply_text("Please enter a valid message \n eg. What are the symptoms of Covid?")

    elif urgency == 1:
        update.message.reply_text("You will be able to seek the answer to this query on the MOH website at \nmoh.gov.sg/faqs")

    elif urgency == 2:
        update.message.reply_text("Please seek further help at the chatbot below \nt.me/covidhelp")  #dummy bot work in progress

    elif urgency == 3:
        update.message.reply_text("Please hold on and do not leave your house. An assistant would be calling you shortly")
        

    print('reply given to user!')
  

#to handle incoming commands
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))  # Filters out unknown commands

#line to deal with texts 
updater.dispatcher.add_handler(MessageHandler(Filters.text, texts))
  
# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
updater.dispatcher.add_handler(MessageHandler(Filters.text, echo)) 

#start running the bot proper
updater.start_polling()


