from flask import Blueprint, render_template, session, request
from flask_login import  login_required, current_user
from random import choice
from train_module import process
from time import sleep
from app import app
import json
from flask_pymongo import PyMongo

#uri = "mongodb+srv://ynstf:ynstf2023@cluster0.s6fqvmm.mongodb.net/db_msgs"
uri = "mongodb://ynstf:ynstf2023@iad2-c12-1.mongo.objectrocket.com:53515,iad2-c12-2.mongo.objectrocket.com:53515,iad2-c12-0.mongo.objectrocket.com:53515/db_msgs?replicaSet=747aaeac3c6c4f359b4ffc81cfd04230"
mongo = PyMongo(app, uri=uri)


home = Blueprint('home', __name__)

@home.route('/')
def home_page():
    title = "MoBoot"
    email = "younessatif1.0@gmail.com"
    github = "github.com/ynstf/"
    linkedIn = "linkedin.com/in/ynstf/"
    return render_template('home/index.html', title = title, email = email, github = github, linkedIn = linkedIn)


@home.route('/welcome')
@login_required
def welcome():
    title = f"MoBoot : Welcome {session['last_name']}!"


    # get data from mongo database and jsonifay it
    #try :
    db = mongo.db
    data = db.messages.find({"user_id":f"{session['id']}"},{"_id":False,"msgs":True})
    data = list(data)[:]
    data = json.dumps(data)
    data = json.loads(data)
    """except :
        doc = {"user_id":f"{session['id']}","msgs":{"msg":" ","response":" "}}
        db.messages.insert_one(doc)
        data = list(data)[:]
        data = json.dumps(data)
        data = json.loads(data)"""

    #load welcome page with all messages for the current user
    return render_template('home/welcome.html',title=title,nick_name=session['last_name'],data=data)



@home.route("/get")
def get_bot_reponse():

    #make respons from the boot
    userText = request.args.get('msg')
    resp = str(process(userText))

    #save the messages in mongodb database
    db = mongo.db
    if userText.strip()=="":

        #make respanse for the empty messages if user enter empty message
        empty = ["message khawi!!!","gol chi 7aja","hdar m3aaya!","ma tb9ach tsayfet message khawi :("]
        resp = str(choice(empty))
        sleep(1.5)

        #save the resp
        doc = {"user_id":f"{session['id']}","msgs":{"msg":f"{userText}","response":f"{resp}"}}
        db.messages.insert_one(doc)

        #send the resp to the welcome page
        return resp
    
    #save the resp
    doc = {"user_id":f"{session['id']}","msgs":{"msg":f"{userText}","response":f"{resp}"}}
    db.messages.insert_one(doc)

    #send the response to the welcome page
    return resp

@home.route('/admin', methods=['GET', 'POST'])
def admin():
    try:
        if current_user.email=="admin":
            
            import mysql.connector
            from flask_pymongo import PyMongo
            from app.forms.users import sherch
            from app import app
            import json

            
            form = sherch()
            title_admin = "shhhh! : secret page"

            #read all messages
            """mongo = PyMongo(app, uri=uri)
            db = mongo.db
            msgs = db.messages.find({},{"_id":False,"user_id":True,"msgs":True})
            msgs = list(msgs)[:]
            msgs = json.dumps(msgs)
            msgs = json.loads(msgs)"""

            #read all users
            mydb = mysql.connector.connect(
                host="pk1l4ihepirw9fob.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
                user="knjxnvb5k5pd0ypg",
                password="ygshse0motylmxp8",
                port=3306,
                database="x40kaa6wfl5txd75"
                )
            mycursor = mydb.cursor()
            sql = "SELECT * FROM user"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            data = ""
            for i in range(len(myresult)):
                data+=f" {myresult[i]} \n"

            if request.method == "GET":
                return render_template("home/admin.html",title=title_admin,form=form,dbs=myresult,msgs=msgs)
            

            
            vari = request.form.get('reserch')
            return  render_template("home/admin.html",title=title_admin,vari=vari,form=form,dbs=myresult,msgs=msgs)
        else :
            return  render_template('errors/404.html', title="page not found!"), 404
        
    except:
        return  render_template('errors/404.html', title="page not found!"), 404
