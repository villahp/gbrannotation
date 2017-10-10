
import os
import config
import re
from flask import Flask,render_template,request,flash,redirect, url_for
from wtforms import Form, TextAreaField, validators
from sklearn.externals import joblib
import tweepy
from threading import Thread
from flask_sqlalchemy import SQLAlchemy
from models import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gbrannotation.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)
db = SQLAlchemy(app)
thread = None

clf = joblib.load(os.path.join(config.APP_STATIC, 'gbr_multi_label.pkl'))
mlb = joblib.load(os.path.join(config.APP_STATIC, 'mlb.pkl'))
auth = tweepy.AppAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
SEARCH_TERM = ['Great Barrier Reef','GBR','greatbarrierreef']

auth = tweepy.AppAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def predict(sentence):
    predicted = clf.predict(sentence)
    inverse_pred = mlb.inverse_transform(predicted)
    return inverse_pred


def background_thread():
    """Example of how to send server generated events to clients."""
    # while True:
    tweetCount = 0
    message = ''
    if (not api):
        message = "Can't Authenticate to Twitter"
        return message
    else:

        while True:
            try:
                if (config.max_id <= 0):
                    if (not config.sinceId):
                        new_tweets = api.search(q=SEARCH_TERM, count=config.tweetsPerQry)
                    else:
                        new_tweets = api.search(q=SEARCH_TERM, count=config.tweetsPerQry,
                                                since_id=config.sinceId)
                else:
                    if (not config.sinceId):
                        new_tweets = api.search(q=SEARCH_TERM, count=config.tweetsPerQry,
                                                max_id=str(config.max_id - 1))
                    else:
                        new_tweets = api.search(q=SEARCH_TERM, count=config.tweetsPerQry,
                                                max_id=str(config.max_id - 1),
                                                since_id=config.sinceId)
                if not new_tweets:
                    print("No more tweets found")
                    break
                for item in new_tweets:
                    print (item.text)
                    user_id = item.author.id
                    user_name = item.author.name
                    user_screen_name = item.author.screen_name
                    user_loc = item.author.location
                    user_created = item.author.created_at
                    user = User.query.filter_by(id=user_id).first()
                    if user is None:
                        user = User(id=user_id, name=user_name,
                                    screen_name=user_screen_name,
                                    created_at=user_created, location=user_loc)
                    tweet_id_str = item.id_str
                    tweet_created = item.created_at
                    tweet_text = item.text
                    tweet_text = re.sub(r'http\S+', ' ', tweet_text, re.IGNORECASE)
                    tweet_text = re.sub(r'[^\w\d\s]', ' ', tweet_text)
                    tweet_text = re.sub(r'\s+', ' ', tweet_text)

                    category = predict([tweet_text])
                    category_names = []
                    for i in range(len(category[0])):
                        category_names.append(Category.query.filter_by(id=category[0][i] - 1).first().name)
                    category_result = ', '.join(category_names).strip()
                    tweet = Tweet(id_str=tweet_id_str, user_id=user.id, text=tweet_text, created_at=tweet_created,
                                  category=category_result)
                    db.session.add(user)
                    db.session.add(tweet)
                    db.session.commit()
                tweetCount += len(new_tweets)
                print("Downloaded {0} tweets".format(tweetCount))
                config.max_id = new_tweets[-1].id
            except tweepy.TweepError as e:
                # Just exit if any error
                print("some error : " + str(e))
                print('Disconnect with twitter')
                break


def startThreadInViews():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()


def manual_test():
    form = ReusableForm(request.form)
    print(form.errors)
    if request.method == 'POST':
        sentence = request.form['sentence']
        if form.validate():
            # Classify sentence, display result and store in db
            category = predict([sentence])
            category_names = []
            for i in range(len(category[0])):
                category_names.append(Category.query.filter_by(id=category[0][i]-1).first().name)
            new_tweet = Tweet(user_id=0, text=sentence, category=', '.join(category_names).strip())
            db.session.add(new_tweet)
            db.session.commit()
        else:
            flash('All the form fields are required. ')
    return form


class ReusableForm(Form):
    sentence = TextAreaField('Sentence:', validators=[validators.required()])

@app.route('/', methods=['GET', 'POST'])
@app.route('/<int:page>', methods=['GET', 'POST'])
def list_all(page=1):
    form = manual_test()
    startThreadInViews()
    tweets = Tweet.query.order_by(Tweet.id.desc()).paginate(page, config.TWEETS_PER_PAGE, error_out=False)
    return render_template(
        'list.html',
        categories=Category.query.all(),
        tweets=tweets,
        form=form
    )

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)


