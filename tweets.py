from TwitterAPI import TwitterAPI
from backup_views import *
import re

SEARCH_TERM = ['Great Barrier Reef','GBR','greatbarrierreef']


CONSUMER_KEY = 'cJKWunqiKARqu3AYuvjnj1QXZ'
CONSUMER_SECRET = 'ucSRktoUggHa6LfhhvYETzzDKoq2AOKQLhkAQg8FFEzs2cAExQ'
ACCESS_TOKEN_KEY = '1376654834-CqlPgTkTlEKSQ7HAaiWsA0D9viOKIcgl5lNz5FO'
ACCESS_TOKEN_SECRET = '09dqiuh39UHgxoXkIdueKqpUwbgGkKN6qHpX3grDEYqqY'


api = TwitterAPI(CONSUMER_KEY,
                 CONSUMER_SECRET,
                 ACCESS_TOKEN_KEY,
                 ACCESS_TOKEN_SECRET,
                 auth_type='oAuth2')

r = api.request('search/tweets', {'q': SEARCH_TERM})

for item in r:
    id_str = item['id_str']
    created = item['created_at']
    text = item['text']
    text = re.sub(r'http\S+',' ',text,re.IGNORECASE)
    text = re.sub(r'[^\w\d\s]',' ',text)
    text = re.sub(r'\s+',' ',text)
    print(id_str,created,text)
    # fav = item['favorite_count']
    #
    name = item['user']['screen_name']
    # description = item['user']['description']
    loc = item['user']['location']
    user_created = item['user']['created_at']
    print('User: '+ name,loc,user_created)
    user = User.query.filter_by(id=item['user']['id']).first()
    if user is None:
        user = User(id=item['user']['id'], name=item['user']['name'], screen_name=item['user']['screen_name'],
               created_at=item['user']['created_at'], location=item['user']['location'])

    # # Need pre-processing
    category = predict([text])
    category_names = []
    for i in range(len(category[0])):
        category_names.append(Category.query.filter_by(id=category[0][i] - 1).first().name)
    category_result = ', '.join(category_names).strip()
    tweet = Tweet(id_str=item['id_str'], user_id=user.id, text=text, created_at=item['created_at'],
                  category=category_result)
    db.session.add(user)
    db.session.add(tweet)
    db.session.commit()

print('\nQUOTA: %s' % r.get_rest_quota())