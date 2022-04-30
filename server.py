from flask import *
from sqlite3 import *



# NOTES 
# CART --> COULD USE A CART TABLE WITH UID AQS PRI KEY AND MULTIPLE COLUMNS PER UID IF UNABLE TO CREATE A TABLE WITH UID
#  OR CAN APPEND INTO STRING OUTSIDE BEFORE RUNNING THE COMMAND? --> CHECK IF METHOD WORKS BEFORE IMPLEMENTING


# currentuser = None
# currentuser = "maniss" #For testing purposes

db = connect("cablefi.db")
c = db.cursor()
c.execute("SELECT Name, Price FROM CAT")
data = c.fetchall()
db.commit()
db.close()
pricedic = {}

for item in data:
    name, price = item[0], item[1]
    pricedic[name] = price



# pricedic = {"1.5M typec":11, "1.0M typec":9, "0.5M typec":7, '0.5M iphone': 7, '1.0M iphone': 9, '1.5M iphone': 11, '1.0M ethernet': 7, '5.0M ethernet': 9, '10.0M ethernet': 11, '0.5M Micro USB': 7, '1.0M Micro USB': 9, '1.5M Micro USB': 11, '0.5M Audio': 7, '1.0M Audio': 9, '1.5M Audio': 11, '0.5M HDMI': 7, '1.0M HDMI': 9, '1.5M HDMI': 11}

app = Flask(__name__)


#################### RENDER ONLY ZONE :) ############################

@app.route("/testpage") # directory to test html pages
def tester():
    return render_template("ethernet.html")


@app.route("/")
def index():
    return render_template("index.html",)


    
@app.route("/login", methods = ["POST"])
def login():
    return render_template("login.html")
    
@app.route("/signup", methods = ["POST"])    
def signup():
    return render_template("signup.html")

@app.route("/erroruid", methods = ["POST"])
def erroruid():
    return render_template("erroruid.html")
    

@app.route("/error", methods = ["POST"])    
def error():
    return render_template("error.html")


@app.route("/home/<user>", methods = ["POST"])
def home(user):
    return render_template("Home.html",user = user)
    
@app.route("/typec/<user>" , methods = ["POST"])
def typec(user):
    return render_template("typec.html",user = user)

@app.route("/iphone/<user>", methods = ["POST"])
def iphone(user):
    return render_template("lightning.html",user = user)

@app.route("/ethernet/<user>", methods = ["POST"])
def ethernet(user):
    return render_template("ethernet.html",user=user)

@app.route("/micro/<user>", methods = ["POST"])
def micro(user):
    return render_template("micro.html",user = user)

@app.route("/audio/<user>", methods = ["POST"])
def audio(user):
    return render_template("audio.html",user = user)

@app.route("/hdmi/<user>", methods = ["POST"])
def hdmi(user):
    return render_template("hdmi.html",user = user)

# @app.route("/fibre", methods = ["POST"])
# def fibre():
#     return render_template("temp.html")    


# @app.route("/dongle", methods = ["POST"])
# def dongle():
#     return render_template("temp.html")

# @app.route("/success1", methods = ["POST"])
# def success1():
#     return render_template("success1.html")    


@app.route("/success2" ,  methods = ["POST"])
def success2(user):
    return render_template("temp.html",user = user)

@app.route("/logout" , methods = ["POST"])
def logout():
    user = None
    return redirect("/", code = 302)


#################### END OF RENDER ONLY ZONE :( ############################



@app.route("/verify", methods = ["POST"])
def verification():

    user = request.form.get("Username")
    password = request.form.get("Password")


    db = connect("cablefi.db")
    c = db.cursor()
    c.execute('''SELECT * FROM USERS WHERE UserID = :name AND Password = :pword ''', {"name": user, "pword": password})
    check = c.fetchall()
    db.commit()
    db.close()
     
    if len(check)>0:    
        return redirect(url_for("home", user = user) ,code = 307)

    else:
        return redirect(url_for("error", user = user), code = 307)      

@app.route("/create", methods = ["POST"])
def create(user):   

    name = request.form.get('Name')
    email = request.form.get('email')
    ID = request.form.get('uid')
    password = request.form.get('password')
    address = request.form.get('Address')
    deets = [name, email, ID, password, address]

    db = connect("cablefi.db")
    c = db.cursor()
    
    try:
        c.execute('''INSERT INTO USERS(Name,email,UserID,Password,Address) VALUES(?,?,?,?,?)''' ,deets)
        c.execute('''CREATE TABLE {}(Item TEXT NOT NULL,Colour TEXT NOT NULL, QUANTITY INTEGER NOT NULL, Price NUMERIC NOT NULL)'''.format(ID))
        db.commit()
        db.close()
        user = ID
        return redirect(url_for("home", user = user), code = 307,)

    except:
        return redirect(url_for("erroruid", user = user), code = 307)

@app.route("/cart/<user>", methods = ["POST"] )
def cart(user):
    currentuser = user
    db = connect("cablefi.db")
    c = db.cursor()
    c.execute("SELECT Item, Colour, QUANTITY, Price From {}".format(currentuser))
    data = c.fetchall()
    db.commit()
    db.close()
    return render_template("cart.html", data = data, user = user)
    # render_template() takes 1 positional argument but 2 were given
    

@app.route("/update/<user>", methods = ["POST"])
def update(user):
    db = connect("cablefi.db")
    c = db.cursor()
    item = request.form.get("item")
    colour = request.form.get("Colour")
    quantity = int(request.form.get("quantity"))
    currentuser = user
    print("line 185")
    # if quantity < existing:
    #     c.execute("UPDATE {0} SET QUANTITY = QUANTITY - {1} WHERE Item = '{2}';".format(currentuser, quantity, item))   

    # else:
    #     c.execute("UPDATE {0} SET QUANTITY = QUANTITY + {1} WHERE Item = '{2}';".format(currentuser, quantity, item))
    if quantity == 0:
        c.execute("DELETE FROM {0} WHERE Item = '{1}'".format(currentuser, item))
        print("line 193")
    else:
        c.execute("UPDATE {0} SET QUANTITY = {1}, Price = {2} WHERE Item = '{3}' AND Colour = '{4}'".format(currentuser, quantity, quantity*pricedic[item], item, colour))
        print("line 196")
        print("user = {0} quantity = {1} pricetot = {2} item = {3} colour = {4}".format(currentuser, quantity, quantity*pricedic[item], item, colour))
    db.commit()
    db.close()

    print("line 200")
    return redirect(url_for("cart", user = user), code = 307)

@app.route("/add/<user>", methods = ["POST"])
def add(user): 
    currentuser = user
    global pricedic
    item = request.form.get('item')
    quantity = int(request.form.get('Quantity') )
    colour = request.form.get("colour")
    site = request.form.get('site')
    data = [item, colour, quantity, quantity*pricedic[item]]
    db = connect("cablefi.db")
    c = db.cursor()
    print(data, type(quantity))
    # try: 
    c.execute("UPDATE CAT SET Quantity = Quantity - {0} WHERE Name = '{1}' AND Colour = '{2}'".format(int(quantity),item, colour ))

    c.execute("SELECT QUANTITY FROM {0} WHERE Item = '{1}' AND  Colour = '{2}'".format(currentuser, item, colour) )
    existing = c.fetchall()

    if existing:
        existing = existing[0][0]
        quantity += existing

        c.execute("UPDATE {0} SET QUANTITY = {1}, Price = {2} WHERE Item = '{3}' AND  Colour = '{4}' ".format(currentuser, quantity, quantity*pricedic[item], item, colour))
        
    else:

        c.execute("INSERT INTO {}(Item, Colour, QUANTITY, Price) VALUES(?,?,?,?)".format(currentuser), data)
            #sqlite3.OperationalError: unrecognized token: "0.5mtypec" --> fixed
    db.commit()
    db.close()


    
    print(quantity, site, currentuser,colour, pricedic[item], type(quantity))
    return redirect(url_for(site , user = user), code = 307)




app.run( debug = True, port= 5000 )