from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import csv
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
from nltk.tokenize import sent_tokenize, TweetTokenizer

a=[]
b=[]
sec={'jayesh':'prongs','vedant':'vedant','kapil':'kapil'}
app = Flask(__name__)


@app.route('/')
def main():
    return render_template('home.html')


@app.route('/home')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('comment.html')


@app.route('/login', methods=['POST'])
def do_admin_login():
    b=sec.keys()
    for i in b:
        if i==request.form['form-username']:
            if request.form['form-password'] == sec.get(i):
                session['logged_in'] = True
        else:
            flash('wrong password!')
    return home()


@app.route('/result', methods=['POST'])
def result():
    with open('dataset.csv', 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)
    cl = NaiveBayesClassifier(your_list)
    data=request.form['comment']
    print(data)
    sent = TextBlob(data)
    num = sent.sentiment.polarity
    a.insert(0,num)
    if num > 0:
        a.insert(1,"Positive")
    if num < 0:
        a.insert(1, "Negative")
    if num == 0:
        a.insert(1, "Neutral")
    blob = TextBlob(data, classifier=cl)
    i=2
    for s in blob.sentences:
        emo=s.classify()
        a.insert(2,emo)
        i=i+1
    return render_template('result.html',a=a)


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
app.run(debug=True)
