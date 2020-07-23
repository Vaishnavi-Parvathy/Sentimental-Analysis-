from flask import Flask, render_template,request, jsonify
import tweepy
from textblob import TextBlob
app = Flask(__name__)
app.config["DEBUG"] = True

cons_key="zJQyiylJYFuutBTOzomm2ZgDc"
cons_sec="gPXYZSZ7jVqjTOIG48p4CYzs7fx9fmaWHFPnmSMp4DF10Bla3D"
acc_token="1269151933559762945-wZYKQZRbSRaTuDkxW29PnLVaTUJmea"
acc_sec="uGyK2OpmhiCyE20b7D0b26adNOosmdDT0FPmtCsLjHqqt"

auth = tweepy.OAuthHandler(cons_key,cons_sec)
auth.set_access_token(acc_token,acc_sec)
api = tweepy.API(auth)

@app.route('/')
def hello_world():
    
    return render_template('home.html')

@app.route('/results',methods=['GET', 'POST'])
def show_result():
    if request.method=='POST':
        result = request.form['keyword']
    neutral, positive, negative = 0,0,0
    tweetData = {}
    id = 0
    tweets = api.search(q=result,count = 100,rpp = 1500)
    for tweet in tweets:
        blob = TextBlob(tweet.text)
        polarity = blob.sentiment.polarity
        
        if polarity == 0:
            tweetData[id] = {
                'text': tweet.text,
                
                'polarity': round(polarity, 2),
            }
            neutral += 1
        elif polarity > 0:
            tweetData[id] = {
                'text': tweet.text,
                
                'polarity': round(polarity, 2),
            }
            positive += 1
        elif polarity < 0:
            tweetData[id] = {
                'text': tweet.text,
                
                'polarity': round(polarity, 2),
            }
            negative += 1
        id += 1

     
    
    if(positive>negative) and (positive>neutral):
        outcome = 'positive'
        msg = "Outcome: Over the analysis the result falls on a positive edge. :)"
    elif(negative> neutral):
        outcome = 'negative'
        msg = "Outcome: Over the analysis the result falls on the negative edge. :("
    else:
        outcome = 'neutral'
        msg = "Outcome: Over the analysis, the results are claimed to be neutral. :| "
    values = [positive, negative, neutral]
    labels = ["positive", "negative", "neutral"]
    return render_template('result.html', msg=msg, labels=labels, values=values, keyword=result, outcome=outcome, tweetData=tweetData) 
app.run()