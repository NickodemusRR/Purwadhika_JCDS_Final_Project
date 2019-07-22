from flask import Flask, render_template, request, jsonify, redirect, url_for, abort
import requests
import prediction   # file prediction --> package to make prediction
import graph        # file graph.py --> package to create graphic
import mdb          # file mdb.py --> package to connect with MongoDB database
# import jsondb   # using json database
import mysql.connector

app = Flask(__name__)

sqldb = mysql.connector.connect(
    host = 'localhost',
    user = 'guest',
    passwd = '12345CobaFlask',
    database = 'framingham'
)
mycursor = sqldb.cursor()

# ===== home route ===========================
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = mdb.login(username, password)
        # user = jsondb.login(username, password)   # uncomment when using database.json
        if user == username:
            return redirect(url_for('predict', user=user))
        else:
            return render_template('error_login.html')

# ===== signup route ===========================
@app.route('/signup', methods=['GET', 'POST'])
def sign():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = mdb.signup(username, password)
        # user = jsondb.signup(username, password)  # uncomment when using database.json  
        if user == username:
            data = {"username" : user}
            query = 'INSERT INTO users (username) VALUES (%(username)s)'
            mycursor.execute(query, data)
            sqldb.commit()
            return redirect(url_for('predict', user=user))
        else:
            return render_template('error_signup.html')

# ===== prediction route ===========================
@app.route('/predict/<string:user>')
def predict(user):
    return render_template('prediction.html', user=user)

# ===== prediction result route ===========================
@app.route('/result', methods=['POST'])
def result():
    body = request.form
    # user input
    # 'male' 'age' 'currentSmoker' 'cigsPerDay' 'BPMeds' 'prevalentStroke' 'prevalentHyp' 
    # 'diabetes' 'totChol' 'sysBP' 'diaBP' 'BMI' 'heartRate'
    
    user = body['user']
    male = int(body['sex'])
    age = int(body['age'])
    smoker = int(body['smoker'])
    cigs = int(body['cigs'])
    BP = int(body['BP'])
    stroke = int(body['stroke'])
    hyp = int(body['hyp'])
    dia = int(body['dia'])
    chol = int(body['chol']) 
    sysBP = int(body['sysBP'])
    diaBP = int(body['diaBP'])
    BMI = int(body['BMI'])
    heart = int(body['heart'])
    glucose = int(body['glucose'])

    X = [[male, age, smoker, cigs, BP, stroke, hyp, dia, chol, sysBP, diaBP, BMI, heart]]
    predict = prediction.prediction(X)
    
    if predict == 0:
        result = 'Congratulations {}! You are health, please continue to maintain your condition.'.format(user)
    elif predict == 1:
        result = 'We\'re sorry {}. You have a risk of coronary heart disease, please consult a doctor immediately.'.format(user)
    
    Z = {'totChol':chol, 'sysBP':sysBP, 'diaBP':diaBP, 'BMI':BMI, 'heartRate':heart, 'glucose':glucose}
    graphic = graph.create_graphic(Z)
    
    data = dict(body)
    data['TenYearCHD'] = int(predict)
    query = """UPDATE users
     SET male = %(sex)s, age = %(age)s, currentSmoker = %(smoker)s, cigsPerDay = %(cigs)s, BPMeds = %(BP)s, 
     prevalentStroke = %(stroke)s, prevalentHyp = %(hyp)s, diabetes = %(dia)s, totChol = %(chol)s, 
     sysBP = %(sysBP)s, diaBP = %(diaBP)s, BMI = %(BMI)s, 
     heartRate = %(heart)s, glucose = %(glucose)s, TenYearCHD = %(TenYearCHD)s 
     WHERE username = %(user)s"""
    mycursor.execute(query, data)
    sqldb.commit()
    return render_template('result.html', result=result, graphic=graphic)

# ===== error route ===========================
@app.errorhandler(404)
def error(error):
    return render_template('error.html')

if __name__ == "__main__":
    app.run(debug=True)