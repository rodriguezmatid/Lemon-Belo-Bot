import requests
import telebot
import tweepy
import dotenv as _dotenv
import os as _os

_dotenv.load_dotenv()

#############################################################################################################################################################
########################################################################## CRIPTOYA #########################################################################
#############################################################################################################################################################

USDC_Belo= round(requests.get('https://criptoya.com/api/belo/USDC/ARS').json()['totalBid'],1)
USDT_Belo= round(requests.get('https://criptoya.com/api/belo/USDT/ARS').json()['totalBid'],1)
DAI_Belo= round(requests.get('https://criptoya.com/api/belo/DAI/ARS').json()['totalBid'],1)
USDC_Lemon= round(requests.get('https://criptoya.com/api/lemoncash/USDC/ARS').json()['totalBid'],1)
USDT_Lemon= round(requests.get('https://criptoya.com/api/lemoncash/USDT/ARS').json()['totalBid'],1)
DAI_Lemon= round(requests.get('https://criptoya.com/api/lemoncash/DAI/ARS').json()['totalBid'],1)

if USDC_Lemon > USDC_Belo:
    conviene_USDC = "🍋"
else:
    conviene_USDC = "🟣"

if USDT_Lemon > USDT_Belo:
    conviene_USDT = "🍋"
else:
    conviene_USDT = "🟣"

if DAI_Lemon > DAI_Belo:
    conviene_DAI = "🍋"
else:
    conviene_DAI = "🟣"

scrapeo = ("Precios de stables al momento\n"
                  "$USDC."f"{conviene_USDC} Belo: " f"{USDC_Belo} vs Lemon: " f"{USDC_Lemon}\n"
                  "$USDT."f"{conviene_USDT} Belo: " f"{USDT_Belo} vs Lemon: " f"{USDT_Lemon}\n"
                  "$DAI. "f"{conviene_DAI} Belo: " f"{DAI_Belo} vs Lemon: " f"{DAI_Lemon}")

#############################################################################################################################################################
########################################################################## TWITTER ##########################################################################
#############################################################################################################################################################

# Authenticate to Twitter
TW_API_KEY = _os.environ["TWITTER_API_KEY"]
TW_API_SECRET = _os.environ["TWITTER_API_SECRET"]
TW_ACCESS_TOKEN = _os.environ["TWITTER_ACCESS_TOKEN"]
TW_ACCESS_SECRET = _os.environ["TWITTER_ACCESS_SECRET"]

auth = tweepy.OAuthHandler(TW_API_KEY, TW_API_SECRET)
auth.set_access_token(TW_ACCESS_TOKEN, TW_ACCESS_SECRET)

api_twitter = tweepy.API(auth)
#x

try:
    api_twitter.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# ########## Read the last tweet ##########

id = api_twitter.get_user(screen_name='LemonBeloBot')
last_tweet = api_twitter.user_timeline(user_id = id, count = 1, tweet_mode = 'extended')
for tweet in last_tweet:
    last_tweet = tweet.full_text

# ########## Twittea ##########

if scrapeo != last_tweet:
    api_twitter.update_status(scrapeo)
else:
    print("The price didn't change")

#############################################################################################################################################################
########################################################################## TELEGRAM #########################################################################
#############################################################################################################################################################

T_TOKEN = _os.environ["TELEGRAM_TOKEN"]
CHANNEL_1 = _os.environ["CID_CHANNEL_1"]

bot_telegram = telebot.TeleBot(T_TOKEN)
bot_telegram.send_message(CHANNEL_1, scrapeo)