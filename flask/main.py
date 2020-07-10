import schedule
import time
from flask import request
from flask import Flask,render_template,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from forms import SignupForm,LoginForm
import pymysql
from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'wether'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# mydb = mysql.connect()
# cursor =mydb.cursor()
# cursor.execute("SELECT * from wether_stuff")
# data = cursor.fetchall()
# print(data)

app.config['SECRET_KEY']= '16b9999ebab1ceadddabee4ae5d59c1d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/User data'
db = SQLAlchemy(app)




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60),nullable=False)

    def __repr__(self):
        return f"User('{self.name}','{self.username}','{self.email}')"


@app.route('/')
def app1():
    return render_template('index.html')

@app.route('/data')
def app3():
    return render_template('data.html',data=data)

def app2():
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    page= requests.get("https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168#.XnOrCIgzZPZ")
    soup=BeautifulSoup(page.content,"html.parser")
    seven_day=soup.find(id="seven-day-forecast")
    item=seven_day.find_all(class_="tombstone-container")
    today=item[0]
    period_name=today.find(class_="period-name").get_text()
    short_desc=today.find(class_="short-desc").get_text()
    temp=today.find(class_="temp").get_text()

    period_name=[item.find(class_="period-name").get_text() for item in item]
    # print(period_name)
    # print(short_desc)
    # print(temp)
    wether_stuff = pd.DataFrame (
        {
            'period_name':period_name,
            'short_desc':short_desc,
            'temp':temp
        }
    )
    # print(wether_stuff)
    mydb = mysql.connect()
    sql="INSERT INTO `wether_stuff`(`id`, `period_name`, `short_desc`, `temp`) VALUES (%s,%s,%s)"
    cursor =mydb.cursor()
    cursor.execute(sql)
    mydb.commit()
    print('done')


    return render_template('index.html',wether_stuff=wether_stuff)

@app.route('/app2/',methods=['POST','GET'])
def main():
    try:
        app2()
        schedule.every(10).seconds.do(app2)
        while True:
            schedule.run_pending()
            time.sleep(1)
    except : 
        return "wether_stuff error"

@app.route('/register/',methods=['GET', 'POST'])
def register():
    form=SignupForm()
    if request.method=='POST':
        '''Add Entery in to Database'''
        name=request.form.get('Name')
        username=request.form.get('username')
        email=request.form.get('Email')
        password=request.form.get('password')
        entery=User(name=name , username=username , email=email , password=password)
        db.session.add(entery)
        db.session.commit()
    return render_template('register.html',form=form)



@app.route('/login/',methods=['GET', 'POST'])
def login():
    form=LoginForm()
    return render_template('login.html',form=form)

app.run(debug=True)

