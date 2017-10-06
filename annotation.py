from flask import Flask
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import os
from sklearn.externals import joblib
import config


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.POSGRESQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)

clf = joblib.load(os.path.join(config.APP_STATIC, 'gbr_multi_label.pkl'))
mlb = joblib.load(os.path.join(config.APP_STATIC, 'mlb.pkl'))
class ReusableForm(Form):
    sentence = TextAreaField('Sentence:', validators=[validators.required()])


from views import *


if __name__ == '__main__':
    app.run(debug=True)



