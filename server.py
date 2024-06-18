from flask import Flask, request, redirect, url_for, render_template,request,flash
from pymongo import MongoClient
import urllib
import os
from dotenv import load_dotenv

app=Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')


url = os.getenv('url')
client= MongoClient(url)
try:
    client.admin.command('ping')
    print("You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
@app.route('/')
def home_page():
    print("Home page")
    return render_template("homepage.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        name=request.form['name']
        username=request.form['username']
        email=request.form['email']
        employment_type=request.form['employment_type']
        password=request.form['password']
        user_info={
            'name':name,
            'username':username,
            'email':email,
            'employment_type':employment_type,
            'password':password
        }
        client.Employee_database.Employee_details.insert_one(user_info)
        result = client.loginPageCluster.customer.insert_one(user_info)

        if result.acknowledged:
            print(f"Document inserted with ID: {result.inserted_id}")
            return redirect(url_for('login'))
        else:
            print("Document insertion failed")
            return redirect(url_for('register'))
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        result=client.Employee_database.Employee_details.find_one({'username':username,'password':password})
        if result:
            return redirect(url_for('dashboard',username=username))
        else:
            flash('INVALID CREDENTIALS')
            return redirect(url_for('login'))
    return render_template("login.html")

@app.route('/dashboard/<username>', methods=['GET', 'POST'])
def dashboard(username):
    print("Dashboard")
    Employee_details=client.Employee_database.Employee_details.find_one({'username':username})    
    if Employee_details:
        print("User found and data fetched succesfully:")
        return render_template("dashboard.html",username=Employee_details['username'],data=Employee_details)
    else:
       return "User not found",404      

@app.route('/logout')
def logout():
    Flask("Are you sure you want to logout?")
    return redirect(url_for('home_page'))
    
    
if __name__=='__main__':
    app.run(debug=True)