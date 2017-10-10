import os

CONSUMER_KEY = 'cJKWunqiKARqu3AYuvjnj1QXZ'
CONSUMER_SECRET = 'ucSRktoUggHa6LfhhvYETzzDKoq2AOKQLhkAQg8FFEzs2cAExQ'
ACCESS_TOKEN_KEY = '1376654834-CqlPgTkTlEKSQ7HAaiWsA0D9viOKIcgl5lNz5FO'
ACCESS_TOKEN_SECRET = '09dqiuh39UHgxoXkIdueKqpUwbgGkKN6qHpX3grDEYqqY'

POSGRESQL='postgresql://cuongpx:cuongpham@localhost/gbrannotation'
SQLITE='sqlite://annotation.db'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'ml_model')

TWEETS_PER_PAGE = 10

CATEGORY_LIST = ['beach','boat_tour','cruise','fishing_charter','forest','general','hiking',
 'horse_riding','island','jet_tour','sailing','scenic_flight_tour',
 'scuba_diving','scuba_doo','sky_diving','snorkeling','snorkeling_tour',
 'submarine_creature','surfing','swimming','valley','waterfall',
 'watersport','whale_watching']

maxTweets = 10000000 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
sinceId = None
max_id = -1
