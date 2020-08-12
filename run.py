import os
import json
from flask import Flask, render_template, redirect, request, url_for, session, flash, Markup
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'doggiedatabase'
app.config['MONGO_URI'] = 'mongodb+srv://doggieuser:doggiepassword@doggiecluster.wtitg.mongodb.net/doggiedatabase?retryWrites=true&w=majority'

mongo = PyMongo(app)


@app.route('/')
def index():
  
    data = []
    with open("data/doggie.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("index.html", page_title="Doggie Daycare", doggie=data)

@app.route('/about')
def about():
    data = []
    with open("data/doggie.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("about.html", page_title="Doggie About")

@app.route('/contact', methods=['POST', 'GET'])
def contact():
    data = []
    with open("data/doggie.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("contact.html", page_title="Doggie Contact")

@app.route('/daycare')
def daycare():
    data = []
    with open("data/doggie.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("daycare.html", page_title="Doggie Daycare", doggie=data) 

@app.route('/grooming', methods=['POST', 'GET'])
def grooming():
    data = []
    with open("data/doggie.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("grooming.html", page_title="Doggie Grooming", doggie=data)
    

@app.route('/insert_booking', methods=['POST'])
def insert_booking():
    doggiebook = mongo.db.doggiebook
    doggiebook.insert_one(request.form.to_dict())
    return redirect(url_for('confirm'))


@app.route('/confirm')
def confirm():
    data = []
    with open("data/doggie.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("confirm.html", page_title="Doggie Confirmation", doggie=data)


#########################################

# REGISTER------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.doggielogin.find_one(
            {"email_address": request.form.get("email_address").lower()})

        if existing_user:
            flash("Username already taken")
            return redirect(url_for("register"))

        register = {
            "email_address": request.form.get("email_address").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "first_name": request.form.get("first_name").lower(),
            "last_name": request.form.get("last_name").lower(),
            "petname": request.form.get("petname").lower()
        }
        mongo.db.doggielogin.insert_one(register)

         # put the user in session cookie
        session["user"] = request.form.get("email_address").lower()
        flash("Registration sucessfull")
        return redirect(url_for("profile", email_address=session["user"]))
    return render_template("register.html", page_title="Doggie Register")

# LOGIN-----------------------------------------------------


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        existing_user = mongo.db.doggielogin.find_one(
            {"email_address": request.form.get("email_address").lower()})

        if existing_user:
            # password match check
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("email_address").lower()
                flash("Nice to see you again, {}!".format(
                        request.form.get("email_address")))
                return redirect(url_for(
                        "profile", email_address=session["user"]))
            else:
                # invalid password
                flash("Incorrect credentials.")
                return redirect(url_for("login"))

        else:
            # the username is not registered
            flash("Incorrect credentials")
            return redirect(url_for("login"))
    return render_template("login.html", page_title="Doggie Login")

# USER'S PROFILE -----------------------
@app.route("/profile/<email_address>", methods=['GET', 'POST'])
def profile(email_address):
    
    # get the session username from db
    email_address = mongo.db.doggielogin.find_one(
       {"email_address": session["user"]})["email_address"]

    if session["user"]:
        return render_template("profile.html", email_address=email_address, page_title="Doggie Profile")

    return redirect(url_for("profile"))



# LOGOUT -----------------------------------

@app.route("/logout")
def logout():
    # remove user from current session cookie

    flash("You have been logged out. See you soon!")
    session.pop("user")
    return redirect(url_for("login"))


# DELETE PROFILE ------------------------------

@app.route("/delete_profile/<email_address>", methods=["GET", "POST"])
def delete_profile(email_address):
    mongo.db.doggielogin.remove({"email_address": session["user"]})
    session.clear()
    flash("Your profile has been deleted.")
    return redirect(url_for("index"))

#@app.route('/update_email/<email_address>', methods=["GET", "POST"])
#def update_email(email_address):
#    emailupdate = mongo.db.doggielogin
#    emailupdate.update({"email_address": session["user"]},
 #   {
 #       'email_address':request.form.get('email_address'),
  #      'petname':request.form.get('petname'),
   #     'first_name': request.form.get('first_name'),
    #    'last_name': request.form.get('last_name')
  #  })
   # return redirect(url_for('index'))


##########################################



@app.route('/overnight')
def overnight():
    data = []
    with open("data/doggie.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("overnight.html", page_title="Doggie Sleepover", doggie=data)

@app.route('/prices')
def prices():
    data = []
    with open("data/doggie.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("prices.html", page_title="Doggie Prices", doggie=data)

@app.route('/viewbooking')
def viewbooking():
    return render_template('viewbooking.html',
                           doggiebook=mongo.db.doggiebook.find(), page_title="Doggie Bookings")

@app.route('/edit_booking/<task_id>', methods=['POST', 'GET'])
def edit_booking(task_id):
    the_task =  mongo.db.doggiebook.find_one({"_id": ObjectId(task_id)})
    edit_login =  mongo.db.doggielogin.find()
    edit_pets = mongo.db.doggiepets.find()
    return render_template('editbooking.html', task=the_task, login=edit_login, pets=edit_pets)


@app.route('/update_booking/<task_id>', methods=['POST', 'GET'])
def update_booking(task_id):
    tasks = mongo.db.doggiebook
    tasks.update( {'_id': ObjectId(task_id)},
    {
        'email_address':request.form.get('email_address'),
        'petname':request.form.get('petname'),
        'service': request.form.get('service'),
        'date': request.form.get('date')
    })
    return redirect(url_for('viewbooking'))

@app.route('/delete_booking/<task_id>')
def delete_booking(task_id):
    mongo.db.doggiebook.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('viewbooking'))

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)