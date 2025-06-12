from flask import Flask,render_template,url_for,request
app = Flask(__name__)
import smtplib
import pymysql
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

db_config = {
    "host" : "localhost",
    "user" : "root",
    "password" : "Root",
    "database" : "ECOMM"
}
@app.route("/")
def landing():
    return render_template("home.html")

@app.route("/register1")
def register1():
    return render_template("register.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/register2",methods=["POST","GET"])
def register2():
    username = request.form["username"]
    fullname = request.form["fullname"]
    email = request.form["email"]
    mobile = request.form["mobile"]
    password = request.form["password"]
    cpassword = request.form["cpassword"]

    #Checking for duplicate username

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM USERS WHERE USERNAME = %s"
    cursor.execute(query,(username))
    data = cursor.fetchone()
    conn.close()
    
    if data is not None:
        return render_template("register.html",msg="usernameexist")
    elif password != cpassword:
        return render_template("register.html",msg="wrongpassword")
    else:

        otp = random.randint(1111,9999)

        # uhcp qbhp pssh ollg

        body = f"OTP For Validation is {otp}"
    
        msg = MIMEMultipart()
        msg["From"] = "glpriyanka540@gmail.com"
        msg["To"] = email
        msg["Subject"] = "OTP For Validation"
        msg.attach(MIMEText(body,'plain'))

        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("glpriyanka540@gmail.com","uhcp qbhp pssh ollg")
        server.send_message(msg)
        server.quit()
        return render_template("otpverification.html",username=username,fullname=fullname,email=email,mobile=mobile,password=password,otp=otp)
@app.route("/register3",methods=["POST","GET"])
def register3():
    username = request.form["username"]
    fullname = request.form["fullname"]
    email = request.form["email"]
    mobile = request.form["mobile"]
    password = request.form["password"]
    otp = request.form["otp"]
    cotp = request.form["cotp"]

    if str(otp) != str(cotp):
        newotp = random.randint(1111,9999)

        # uhcp qbhp pssh ollg

        body = f"OTP For Validation is {newotp}"
    
        msg = MIMEMultipart()
        msg["From"] = "glpriyanka540@gmail.com"
        msg["To"] = email
        msg["Subject"] = "OTP For Validation"
        msg.attach(MIMEText(body,'plain'))

        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("glpriyanka540@gmail.com","uhcp qbhp pssh ollg")
        server.send_message(msg)
        server.quit()
        return render_template("otpverification.html",msg="wrongotp",username=username,fullname=fullname,email=email,mobile=mobile,password=password,otp=newotp)
    else:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO USERS VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(query,(username,fullname,email,mobile,password))
        conn.commit()
        conn.close()
        return render_template("home.html",msg="accountcreated")
@app.route("/login1")
def login1():
    return render_template("login.html")
@app.route("/login2",methods=["POST","GET"])
def login2():
    username = request.form["username"]
    password = request.form["password"]
    
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM USERS WHERE USERNAME = %s"
    cursor.execute(query,(username))
    data = cursor.fetchone()
    conn.close()

    if data is None:
        return render_template("login.html",msg="nouser")
    if data[-1] != password:
        return render_template("login.html",msg="wrongpassword")
    else:
        return render_template("user_home.html",username=username)
@app.route("/forgotpassword")
def forgotpassword():
    return render_template("forgotpassword1.html")
@app.route("/forgotpassword1",methods=["POST","GET"])
def forgotpassword1():
    username = request.form["username"]


    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM USERS WHERE USERNAME = %s"
    cursor.execute(query,(username))
    data = cursor.fetchone()
    conn.close()

    if data is None:
        return render_template("forgotpassword1.html",msg="nouser")
    else:
        newotp = random.randint(1111,9999)

        # uhcp qbhp pssh ollg

        body = f"OTP For Validation is {newotp}"
    
        msg = MIMEMultipart()
        msg["From"] = "glpriyanka540@gmail.com"
        msg["To"] = data[2]
        msg["Subject"] = "OTP For Validation"
        msg.attach(MIMEText(body,'plain'))

        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("glpriyanka540@gmail.com","uhcp qbhp pssh ollg")
        server.send_message(msg)
        server.quit()

        return render_template("forgotpassword2.html",username=data[0],email=data[2],otp=newotp)
@app.route("/forgotpassword2",methods=["POST","GET"])
def forgotpassword2():
    username = request.form["username"]
    email = request.form["email"]
    otp = request.form["otp"]
    cotp = request.form["cotp"]
    password = request.form["password"]
    cpassword = request.form["cpassword"]

    
    if str(otp) != str(cotp):
        newotp = random.randint(1111,9999)

        #uhcp qbhp pssh ollg

        body = f"OTP For Validation is {newotp}"
    
        msg = MIMEMultipart()
        msg["From"] = "glpriyanka540@gmail.com"
        msg["To"] = email
        msg["Subject"] = "OTP For Validation"
        msg.attach(MIMEText(body,'plain'))

        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("glpriyanka540@gmail.com","uhcp qbhp pssh ollg")
        server.send_message(msg)
        server.quit()

        return render_template("forgotpassword2.html",msg="wrongotp",username=username,email=email,otp=newotp)
    elif password != cpassword:
        return render_template("forgotpassword3.html",msg="wrongpassword",username=username,email=email)
    else:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "UPDATE USERS SET PASSWORD = %s WHERE USERNAME = %s"
        cursor.execute(query,(password,username))
        conn.commit()
        conn.close()
        return render_template("login.html",msg="passwordreset")
@app.route("/forgotpassword3",methods=["POST","GET"])
def forgotpassword3():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    cpassword = request.form["cpassword"]
    print(username)
    print(email)
    print(password)
    print(cpassword)

    if password != cpassword:
        return render_template("forgotpassword3.html",msg="wrongpassword",username=username,email=email)
    else:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "UPDATE USERS SET PASSWORD = %s WHERE USERNAME = %s"
        cursor.execute(query,(password,username))
        conn.commit()
        conn.close()
        return render_template("login.html",msg="passwordreset")
@app.route("/addtocart1",methods=["POST","GET"])
def addtocart1():
    username = request.form["username"]
    product_id = request.form["productid"]
    product_name = request.form["productname"]
    product_price = request.form["productprice"]
    
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM CART WHERE USERNAME = %s AND PRODUCT_ID = %s"
    cursor.execute(query,(username,product_id))
    data = cursor.fetchone()
    print(data)
    conn.close()
    if data is None:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO CART (USERNAME,PRODUCT_ID,PRODUCT_NAME,PRODUCT_PRICE) VALUES (%s,%s,%s,%s)"
        cursor.execute(query,(username,product_id,product_name,product_price))
        conn.commit()
        conn.close()
        return render_template("user_home.html",username=username,msg="p1")
    else:
        qty = int(data[-1]) + 1
        price = int(data[-2]) * qty
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "UPDATE CART SET QUANTITY = %s WHERE PRODUCT_ID = %s AND USERNAME = %s"
        cursor.execute(query,(qty,product_id,username))
        conn.commit()
        conn.close()

        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "UPDATE CART SET PRODUCT_PRICE = %s WHERE PRODUCT_ID = %s AND USERNAME = %s"
        cursor.execute(query,(price,product_id,username))
        conn.commit()
        conn.close()
        
        return render_template("user_home.html",username=username,msg="p2")
@app.route("/shoppingcart/<username>")
def shoppingcart(username):
    
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM CART WHERE USERNAME = %s"
    cursor.execute(query,(username))
    data = cursor.fetchall()
    conn.close()
   
    if len(data) == 0:
        return render_template("user_home.html",username=username,msg="noproductsincart")
    else:
        total = 0
        for i in data:
            total += int(i[-2])
        return render_template("shopping_cart.html",data=data,username=username,grandtotal=total)
@app.route("/user_home2/<username>")
def user_home2(username):
    return render_template("user_home.html",username=username)
@app.route("/deleteproduct/<pid>/<username>")
def deleteproduct(pid,username):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "DELETE FROM CART WHERE PRODUCT_ID = %s"
    cursor.execute(query,(pid))
    conn.commit()
    conn.close()

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM CART WHERE USERNAME = %s"
    cursor.execute(query,(username))
    data = cursor.fetchall()
    conn.close()
   
    if len(data) == 0:
        return render_template("user_home.html",username=username,msg="noproductsincart")
    else:
        total = 0
        for i in data:
            total += int(i[-2])
        return render_template("shopping_cart.html",data=data,username=username,grandtotal=total)

@app.route("/success",methods=["POST","GET"])
def success():
    username = request.form["username"]


    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "INSERT INTO ORDERS (USERNAME,PRODUCT_ID,PRODUCT_NAME,PRODUCT_PRICE,QUANTITY) SELECT USERNAME,PRODUCT_ID,PRODUCT_NAME,PRODUCT_PRICE,QUANTITY FROM CART"
    cursor.execute(query,)
    conn.commit()
    conn.close()


    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "DELETE FROM CART WHERE USERNAME = %s"
    cursor.execute(query,(username))
    conn.commit()
    conn.close()
    return render_template("user_home.html",username=username)
@app.route("/failure",methods=["POST","GET"])
def failure():
    username = request.form["username"]
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM CART WHERE USERNAME = %s"
    cursor.execute(query,(username))
    data = cursor.fetchall()
    conn.close()
   
    if len(data) == 0:
        return render_template("user_home.html",username=username,msg="noproductsincart")
    else:
        total = 0
        for i in data:
            total += int(i[-2])
        return render_template("shopping_cart.html",data=data,username=username,grandtotal=total)
@app.route("/orders/<username>")
def orders(username):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM ORDERS WHERE USERNAME = %s"
    cursor.execute(query,(username))
    data = cursor.fetchall()
    conn.close()
    return render_template("userorders.html",data=data,username=username)
@app.route("/success1",methods=["POST","GET"])
def success1():
    username = request.form["username"]
    productid = request.form["productid"]
    productname = request.form["productname"]
    productprice = request.form["productprice"]
    quantity = request.form["quantity"]

    print(username)
    print(productid)
    print(productname)
    print(productprice)
    print(quantity)

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "INSERT INTO ORDERS (USERNAME,PRODUCT_ID,PRODUCT_NAME,PRODUCT_PRICE,QUANTITY) VALUES (%s,%s,%s,%s,%s)"
    cursor.execute(query,(username,productid,productname,productprice,quantity))
    conn.commit()
    conn.close()

    return render_template("user_home.html",username=username)
app.run()