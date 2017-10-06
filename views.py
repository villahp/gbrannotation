from flask import render_template, request, redirect, flash,url_for
from models import Category, Tweet, User, db
from annotation import app,ReusableForm,clf,mlb


def predict(sentence):
    predicted = clf.predict(sentence)
    inverse_pred = mlb.inverse_transform(predicted)
    return inverse_pred

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
            new_tweet = Tweet(user_id=0,text=sentence,category=', '.join(category_names).strip())
            db.session.add(new_tweet)
            db.session.commit()
        else:
            flash('All the form fields are required. ')
    return form


@app.route('/',methods=['POST','GET'])
def list_all():
    form = manual_test()
    return render_template(
        'list.html',
        categories=Category.query.all(),
        tweets=Tweet.query.all(),#.join(User).order_by(Tweet.created_at)
        form=form
    )


@app.route('/<name>',methods=['POST','GET'])
def list_tweets(name):
    form = manual_test()
    category = Category.query.filter_by(name=name).first()
    return render_template(
        'list.html',
        tweets=Tweet.query.filter_by(category=category).all(),# ]\.join(Priority).order_by(Priority.value.desc()),
        categories=Category.query.all(),
        form=form
    )
