from TwitterAPI import TwitterAPI


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
    print(item)
    # print(item['text'] if 'text' in item else item)

# print('\nQUOTA: %s' % r.get_rest_quota())