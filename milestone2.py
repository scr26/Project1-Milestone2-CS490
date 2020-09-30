import tweepy
import webbrowser
import time
import flask 
import os
import random
from dotenv import load_dotenv
from tweepy import OAuthHandler
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
import json
from os.path import join, dirname
import requests
import urllib.request
import urllib
import wget

dotenv_path = join(dirname(__file__),'Twitter.env')
load_dotenv(dotenv_path)

spoonacular_key = os.environ['SPOONACULAR_KEY']


# Authentication Info see Twitter.env for more detailed information

twitterConsumerKey = os.environ["TWITTER_CONSUMER_KEY"]
twitterConsumerSecret = os.environ["TWITTER_CONSUMER_SECRET"]

accessToken = os.environ["ACCESS_TOKEN"]
accessTokenSecret = os.environ["ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuthHandler(twitterConsumerKey,twitterConsumerSecret)
auth.set_access_token(accessToken,accessTokenSecret)

api = tweepy.API(auth)


app = flask.Flask(__name__)
 
@app.route('/')
 
def index():
    
    foodList = ['French Toast','Poutine','Chicken Nuggets','Veggie Burger','Sushi','Tacos','Dosa','Pho','Chicken Kebab','Pizza','Lobster']
    chosenOne = random.choice(foodList)

    search = api.search(chosenOne)
    length = len(search) - 2
    
    randomNumber = random.randint(0,length)


    text = search[randomNumber].text
    date = search[randomNumber].created_at
    screenName = search[randomNumber].user.screen_name
    name = search[randomNumber].user.name
    url = search[randomNumber].user.url
    
    
    
    #Spoonacular Part Below
    
    # Getting url & Title & ID    
    url = "https://api.spoonacular.com/recipes/complexSearch?query={}&apiKey={}".format(chosenOne,spoonacular_key)
    response = requests.get(url)
    json_body = response.json()
    title = json.dumps(json_body["results"][0]["title"],indent=2)
    ID = json.dumps(json_body["results"][0]["id"],indent = 2)
    
    
    #Getting original link to the recipe
    url = "https://api.spoonacular.com/recipes/{}/information?includeNutrition=false&apiKey={}".format(ID,spoonacular_key)
    response = requests.get(url)
    json_body = response.json()

    linkToRecipe = json.dumps(json_body["sourceUrl"],indent = 2)
    
    #link to image
    imageLink = json.dumps(json_body["image"],indent=2)
    
    
    
    

    
    return flask.render_template(
        
        "index.html",
        chosenOne = chosenOne,
        text = text,
        date = date,
        screenName = screenName,
        url = url,
        #Take Down Below two when sumbitting real thing
        linkToRecipe=linkToRecipe,
        imageLink=imageLink
        #sourceUrl = sourceUrl,
        #image = image
        
        
        
        )
    
app.run(
    
    port=int(os.getenv('PORT',8080)),
    host = os.getenv('IP','0.0.0.0')
    
    )
    
    