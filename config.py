import os

CONSUMER_KEY = 'cJKWunqiKARqu3AYuvjnj1QXZ'
CONSUMER_SECRET = 'ucSRktoUggHa6LfhhvYETzzDKoq2AOKQLhkAQg8FFEzs2cAExQ'
ACCESS_TOKEN_KEY = '1376654834-CqlPgTkTlEKSQ7HAaiWsA0D9viOKIcgl5lNz5FO'
ACCESS_TOKEN_SECRET = '09dqiuh39UHgxoXkIdueKqpUwbgGkKN6qHpX3grDEYqqY'

POSGRESQL='postgresql://cuongpx:cuongpham@localhost/gbrannotation'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'ml_model')