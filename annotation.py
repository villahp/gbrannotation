
import os
import config
import re
from flask import Flask,render_template,request,flash
from wtforms import Form, TextAreaField, validators
from sklearn.externals import joblib
from TwitterAPI import TwitterAPI,TwitterRestPager
from threading import Thread
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.POSGRESQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)
db = SQLAlchemy(app)
thread = None

clf = joblib.load(os.path.join(config.APP_STATIC, 'gbr_multi_label.pkl'))
mlb = joblib.load(os.path.join(config.APP_STATIC, 'mlb.pkl'))
api = TwitterAPI(config.CONSUMER_KEY, config.CONSUMER_SECRET,
                 config.ACCESS_TOKEN_KEY, config.ACCESS_TOKEN_SECRET, auth_type='oAuth2')
SEARCH_TERM = ['Great Barrier Reef','GBR','greatbarrierreef']


def predict(sentence):
    predicted = clf.predict(sentence)
    inverse_pred = mlb.inverse_transform(predicted)
    return inverse_pred


def processing_tweet(text):
    return ('%s' % (text)).encode('utf-8')


def background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        iterator = TwitterRestPager(api, 'search/tweets', {'q': SEARCH_TERM}).get_iterator(wait=2)
        try:
            for item in iterator:
                if 'text' in item:
                    # print(item['text'])
                    # id_str = item['id_str']
                    # created = item['created_at']
                    # text = item['text']
                    # print(id_str, created, text)
                    # name = item['user']['screen_name']
                    # loc = item['user']['location']
                    # user_created = item['user']['created_at']
                    # print('User: ' + name, loc, user_created)


                    user_id = item['user']['id']
                    user_name = item['user']['name'].encode('utf-8')
                    user_screen_name = item['user']['screen_name'].encode('utf-8')
                    user_loc = item['user']['location'].encode('utf-8')
                    user_created = item['user']['created_at']
                    user = User.query.filter_by(id=item['user']['id']).first()
                    if user is None:
                        user = User(id=user_id, name=user_name,
                                    screen_name=user_screen_name,
                                    created_at=user_created, location=user_loc)
                    tweet_id_str = item['id_str'].encode('utf-8')
                    tweet_created = item['created_at']
                    tweet_text = item['text']
                    tweet_text = re.sub(r'http\S+', ' ', tweet_text, re.IGNORECASE)
                    tweet_text = re.sub(r'[^\w\d\s]', ' ', tweet_text)
                    tweet_text = re.sub(r'\s+', ' ', tweet_text).encode('utf-8')

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
                elif 'message' in item:
                    # something needs to be fixed before re-connecting
                    raise Exception(item['message'])
        except Exception as e:
            print ('Error: ' + e.message)
            pass


def startThreadInViews():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()


def manual_test():
    form = ReusableForm(request.form)
    print form.errors
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
    app.run(debug=True)



