import json
import os
from werkzeug.utils import secure_filename
from flask import Flask, request, Response
import base64
import mysql.connector
from mysql.connector import Error
from flask import abort
# from flask_basicauth import BasicAuth

from functools import wraps
import uuid
import time
from flask import jsonify
import bcrypt
import re
import datetime
from enum import Enum
import csv
import magic
import hashlib
import boto3
import logging
import statsd
# for enum34, or the stdlib version
# from aenum import Enum  # for the aenum version


app = Flask(__name__)
c = statsd.StatsClient('localhost',8125)
logging.basicConfig(filename='newLog7.log', level=logging.DEBUG)

# print(Animal.ant.value)


#
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])
user_name = ''
message=''
user_id = ''
paymentStatus = ''


host=""
port="3306"
user=""
passwd=""
database=''
bucketName = ""



list = []
# with open('category.csv') as csvfile:
#     readCSV = csv.reader(csvfile, delimiter=',')
#     for row in readCSV:
#         # print(row)
#
#         list.append(row[0])
list = ["spring2020","summer","fee"]


# global paymentStatus
# paymentStatus = Enum('paymentStatus', 'paid due past_due no_payment_required')

def check(authorization_header):
    # username = "f"
    # password = "f"
    encoded_uname_pass = authorization_header.split()[-1]
    data = base64.b64decode(encoded_uname_pass)

    # split the data on username:password
    user_data = (str(data.decode('utf-8'))).split(":")
    global user_name
    user_name = user_data[0]
    in_password = user_data[1]
    if app.config['TESTING'] == True:
        rootpw = 'passw0rd'
        mydb = mysql.connector.connect(
        host="",
        port="",
        user="",
        passwd="",
        database=''
    )


    else:

        mydb =mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        passwd=passwd,
        database=database

    )

    mycursor = mydb.cursor()

    sql = "SELECT * FROM user_value WHERE email_address = %s"
    adr = (user_name,)

    mycursor.execute(sql, adr)
    rows = mycursor.fetchall()
    if len(rows) > 0:
        for x in rows:

            salt = x[7]
            data_password = x[4]
            global user_id
            user_id = x[0]
            # salt = bcrypt.gensalt()

            hashed = bcrypt.hashpw(in_password.encode('utf8'), salt.encode('utf8'))
            hash_password = hashed.decode('utf-8')

            if data_password == hash_password:

                return True

            else:
                abort(401, 'invalid password')

    else:
        abort(401, 'user does not exists')


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authorization_header = request.headers.get('Authorization')
        if authorization_header and check(authorization_header):
            return f(*args, **kwargs)
        else:
            resp = Response()
            resp.headers['WWW-Authenticate'] = 'Basic'
            return resp, 401
        return f(*args, **kwargs)

    return decorated


def valid_cred(email_address, password):
    regex_email = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    regex_password = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,30}$"
    password_check = re.compile(regex_password)

    if ((re.search(regex_email, email_address) == None) or (re.search(regex_password, password) == None)):
        return False
    else:
        return True


# creation of user account
accounts = []





@app.route("/user", methods=["POST"])
def addAccount():
    # take user input
    print("the test")

    app.logger.info('Processing default request in user post77>>')
    c.incr('Countcreateuser',1)
    startCall = time.time()

    print(app.config['TESTING'])
    if app.config['TESTING'] == True:
        try:
            # first_name = request.json['first_name']
            # print("first")
            # print(first_name)
            # last_name = request.json['last_name']
            # email_address = request.json['email_address']
            #
            # password = request.json['password']
            input_data = request.data
            str_data = input_data.decode('utf8').replace("'", '"')
            test_data = json.loads(str_data)

            first_name = test_data['first_name']

            last_name = test_data['last_name']
            email_address = test_data['email_address']

            password = test_data['password']
            # throw bort(400) for less length password NIST
            account_created = time.time()
            account_updated = time.time()
            id = uuid.uuid4()
            flag = valid_cred(email_address, password)

            if flag != True:
                abort(400)
        except:
            abort(400)

        # post values in MySql database tables

        rootpw = 'passw0rd'
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user='user',
            passwd=rootpw,
            database='test_db'
        )




    else:
        print("inside this side>")

        try:
            first_name = request.json['first_name']
            print("first")
            print(first_name)
            last_name = request.json['last_name']
            email_address = request.json['email_address']
            #
            password = request.json['password']
            # first_name = "nameee"
            # print("first")
            # print(first_name)
            # last_name = "last"
            # email_address = "pareenam7@gmail.com"
            #
            # password = "Network1234!0"
            # throw bort(400) for less length password NIST
            account_created = time.time()
            account_updated = time.time()
            id = uuid.uuid4()
            flag = valid_cred(email_address, password)

            if flag != True:
                abort(400)
        except:
            abort(400)

        # post values in MySql database tables

        mydb = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            database=database

        )
        print(host)
        print("above was host")
    mycursor = mydb.cursor()

    salt = bcrypt.gensalt()
    print("hello i am here")
    hashed = bcrypt.hashpw(password.encode('utf8'), salt)

    startCall_db = time.time()

    hash_password = hashed.decode('utf-8')
    sql = "INSERT INTO user_value (id,first_name,last_name,email_address,password,account_created,account_updated,salt) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (str(id), first_name, last_name, email_address, hash_password, account_created, account_updated, salt)
    durCall_db = (time.time() - startCall_db)*1000
    c.timing("TimercreateuserDB", durCall_db)
    print("err")
    mycursor.execute(sql, val)
    mydb.commit()
    print("77777")
    data = {'id': id,
            'first_name': first_name,
            'last_name': last_name,
            'email_address': email_address,
            'account_created': account_created,
            'account_updated': account_updated
            }
    durCall = (time.time()-startCall)*1000
    c.timing("Timercreateuser",durCall)
    return jsonify(data)

    #    abort(400,'Please change your input')

    # try:

    #     sql = "INSERT INTO user_value (user_id,first_name,last_name,email_address,password,account_created,account_updated) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    #     val = (user_id,first_name,last_name,email_address,password,account_created,account_updated)
    #     mycursor.execute(sql, val)

    #     mydb.commit()
    #     data = {'first_name':first_name,
    #         'last_name' : last_name,
    #         'email_address' : email_address,
    #         'user_id':user_id }
    #     return jsonify(data)
    # except:
    #     abort(400)


# update funnction

@app.route("/user", methods=["PUT"])
@login_required
def updateAccount():
    # take user input
    # pass a global username after validation from above
    c.incr('Countupdateuser', 1)
    startCall = time.time()


    if app.config['TESTING'] == True:
        try:
            # first_name = request.json['first_name']
            # print("first")
            # print(first_name)
            # last_name = request.json['last_name']
            # email_address = request.json['email_address']
            #
            # password = request.json['password']
            input_data = request.data
            str_data = input_data.decode('utf8').replace("'", '"')
            test_data = json.loads(str_data)

            first_name = test_data['first_name']

            last_name = test_data['last_name']
            email_address = test_data['email_address']

            password = test_data['password']
            # throw bort(400) for less length password NIST
            account_created = time.time()
            account_updated = time.time()
            id = uuid.uuid4()
            flag = valid_cred(email_address, password)

            if flag != True:
                abort(401)
        except:
            abort(401)

        # post values in MySql database tables

        rootpw = 'passw0rd'
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user='user',
            passwd=rootpw,
            database='test_db'
        )


    else:

        try:
            first_name = request.json['first_name']
            last_name = request.json['last_name']
            email_address = user_name

            if request.json['email_address'] != user_name:
                return abort(400)

            password = request.json['password']
            # account_created = time.time()
            account_updated = time.time()
        except:
            abort(400)
        # user_id = uuid.uuid4()

        # post values in MySql database tables

        mydb = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            database=database

        )

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf8'), salt)

    hash_password = hashed.decode('utf-8')
    startCall_db = time.time()
    sql = "UPDATE  user_value SET first_name = %s,last_name = %s,password = %s, account_updated = %s, salt = %s WHERE email_address = %s"
    val = (first_name, last_name, hash_password, account_updated, salt, email_address)



    durCall = (time.time() - startCall)*1000
    c.timing("Timerupdateuser", durCall)

    try:
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        mydb.commit()
        durCall_db = (time.time() - startCall_db) * 1000
        c.timing("TimerupdateuserDB", durCall_db)
        return '', 204


    except:
        abort(400)


@app.route("/test1", methods=["GET"])
def test7():
    return True


# get user details
@app.route("/user", methods=["GET"])
@login_required
def getAccount():
    # take user input\
    c.incr('Countgetuser', 1)
    startCall = time.time()
    if app.config['TESTING'] == True:
        email_address = user_name
        print(email_address)

        # pass a global username after validation from above

        # user_id = uuid.uuid4()

        # post values in MySql database tables

        rootpw = 'passw0rd'
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user='user',
            passwd=rootpw,
            database='test_db'
        )



    else:

        email_address = user_name
        print(email_address)

        # pass a global username after validation from above

        # user_id = uuid.uuid4()

        # post values in MySql database tables

        mydb = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            database=database

        )

    mycursor = mydb.cursor()
    startCall_db = time.time()

    sql = "SELECT * FROM user_value WHERE email_address = %s"
    val = (email_address,)
    # mycursor.execute(sql, val)
    durCall = (time.time() - startCall)*1000
    c.timing("Timergetuser", durCall)

    try:
        # print(x)
        mycursor.execute(sql, val)

        myresult = mycursor.fetchall()
        durCall_db = (time.time() - startCall_db) * 1000
        c.timing("TimergetuserDB", durCall_db)
        for x in myresult:
            data = {'id': x[0],
                    'first_name': x[1],
                    'last_name': x[2],
                    'email_address': x[3],
                    'account_created': x[5],
                    'account_updated': x[6]
                    }

        print(jsonify(data))
        return jsonify(data)


    except:
        abort(400)





############################### use it for bill ############################################

@app.route("/bill", methods=["POST"])
@login_required
def create_bill():
    c.incr('Countcreatebill', 1)
    startCall = time.time()
    if app.config['TESTING'] == True:
        input_data = request.data
        str_data = input_data.decode('utf8').replace("'", '"')
        test_data = json.loads(str_data)

        vendor = test_data['vendor']

        bill_date = test_data['bill_date']
        due_date = test_data['due_date']
        amount_due = test_data['amount_due']
        category_list = test_data['categories']
        paymentStatus = Enum('paymentStatus', 'paid due past_due no_payment_required')
        payment = test_data['paymentStatus']

        if payment == 'paid':
            payment_status = paymentStatus.paid.value
        elif payment == 'due':
            payment_status = paymentStatus.due.value
        elif payment == 'past_due':
            payment_status = paymentStatus.past_due.value
        elif payment == 'no_payment_required':
            payment_status = paymentStatus.no_payment_required.value
        else:
            payment_status = 'invalid'

        created_ts = time.time()
        updated_ts = time.time()
        id = uuid.uuid4()
        owner_id = user_id

        # post values in MySql database tables

        rootpw = 'passw0rd'
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user='user',
            passwd=rootpw,
            database='test_db'
        )






    else:
        try:
            vendor = request.json['vendor']

            # datetime.datetime.strptime(request.json['bill_date'], '%Y-%m-%d')

            bill_date = request.json['bill_date']
            due_date = request.json['due_date']
            try:
                date_format = '%Y-%m-%d'
                date_obj_bill = datetime.datetime.strptime(bill_date, date_format)
                date_obj_due = datetime.datetime.strptime(due_date, date_format)


            except ValueError:
                abort(400, 'incorrect date values')
            amount_due = request.json['amount_due']
            # category values
            category_list = request.json['categories']
            # print(all(item in list for item in category_list))
            # print("************************")
            # # list = []
            # list = list(category_list.split(" "))
            # print(list)

            categories = "oo"
            paymentStatus = Enum('paymentStatus', 'paid due past_due no_payment_required')
            payment = request.json['paymentStatus']

            if payment == 'paid':
                payment_status = paymentStatus.paid.value
            elif payment == 'due':
                payment_status = paymentStatus.due.value
            elif payment == 'past_due':
                payment_status = paymentStatus.past_due.value
            elif payment == 'no_payment_required':
                payment_status = paymentStatus.no_payment_required.value
            else:
                payment_status = 'invalid'
            # print(payment_status)
            if payment_status == 'invalid':
                abort(400, 'invalid payment status')

            created_ts = time.time()
            updated_ts = time.time()
            id = uuid.uuid4()
            owner_id = user_id

            # post values in MySql database tables

            mydb = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                passwd=passwd,
                database=database

            )

            mycursor = mydb.cursor()

            mylist = json.dumps(category_list)
            # print("json>>>")
            # print(mylist)
            # salt = bcrypt.gensalt()
            # hashed = bcrypt.hashpw(password.encode('utf8'), salt)
            #
            # hash_password = hashed.decode('utf-8')
            if amount_due <= 0.00:
                abort(400, 'amount is not valid')
            startCall_db = time.time()

            sql = "INSERT INTO bill (id,created_ts,updated_ts,owner_id,vendor,bill_date,due_date,amount_due,categories,paymentStatus) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (
            str(id), created_ts, updated_ts, owner_id, vendor, bill_date, due_date, amount_due, mylist, payment_status)
            print("bill7")
            # mycursor.execute(sql, val)
            print("xhjasjdgj")
            # mydb.commit()
            data = {'id': id,
                    'created_ts': created_ts,
                    'updated_ts': updated_ts,
                    'owner_id': owner_id,
                    'vendor': vendor,
                    'bill_date': bill_date,
                    'due_date': due_date,
                    'amount_due': amount_due,
                    'categories': json.loads(mylist),
                    'payment_status': payment_status
                    }
        # return jsonify(data)
        except:
            abort(400, 'invaid input')
        print(updated_ts)
        sql = "INSERT INTO bill (id,created_ts,updated_ts,owner_id,vendor,bill_date,due_date,amount_due,categories,paymentStatus) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (
        str(id), created_ts, updated_ts, owner_id, vendor, bill_date, due_date, amount_due, mylist, payment_status)
        print("bill7")
        mycursor.execute(sql, val)
        durCall = (time.time() - startCall)*1000
        c.timing("Timercreatebill", durCall)
        print("xhjasjdgj")
        mydb.commit()
        durCall_db = (time.time() - startCall_db) * 1000
        c.timing("TimercreatebillDB", durCall_db)
        data = {'id': id,
                'created_ts': created_ts,
                'updated_ts': updated_ts,
                'owner_id': owner_id,
                'vendor': vendor,
                'bill_date': bill_date,
                'due_date': due_date,
                'amount_due': amount_due,
                'categories': json.loads(mylist),
                'payment_status': payment_status
                }
        return jsonify(data)


@app.route("/bill/<id>", methods=["PUT"])
@login_required
def update_bill(id):
    c.incr('Countupdatebill', 1)
    startCall = time.time()
    # validate the owner
    print("id>>>")
    print(id)
    if app.config['TESTING'] == True:
        rootpw = 'passw0rd'
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user='user',
            passwd=rootpw,
            database='test_db',

        )
        import json
        input_data = request.data
        str_data = input_data.decode('utf8').replace("'", '"')
        test_data = json.loads(str_data)

        vendor = test_data['vendor']

        bill_date = test_data['bill_date']
        due_date = test_data['due_date']
        amount_due = test_data['amount_due']
        category_list = test_data['categories']
        # paymentStatus = Enum('paymentStatus', 'paid due past_due no_payment_required')
        payment = test_data['paymentStatus']



    else:
        vendor = request.json['vendor']

        # datetime.datetime.strptime(request.json['bill_date'], '%Y-%m-%d')

        bill_date = request.json['bill_date']
        due_date = request.json['due_date']
        amount_due = request.json['amount_due']
        payment = request.json['paymentStatus']

        # category values
        category_list = request.json['categories']
        mydb = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            database=database

        )
    mycursor = mydb.cursor()

    sql = "SELECT * FROM bill WHERE  id = %s"
    adr = (id,)
    try:

        mycursor.execute(sql, adr)
        rows = mycursor.fetchall()
    except:
        abort(401, 'invalid details')
    if len(rows) < 1:
        abort(404, 'invalid bill details')
    for x in rows:
        if user_id != x[3]:
            abort(401, 'you are not the owner')
    try:

        try:
            date_format = '%Y-%m-%d'
            date_obj_bill = datetime.datetime.strptime(bill_date, date_format)
            date_obj_due = datetime.datetime.strptime(due_date, date_format)


        except ValueError:
            abort(400, 'incorrect date values')

        print(all(item in list for item in category_list))
        print("************************")
        # list = []
        # list = list(category_list.split(" "))
        # print(list)

        categories = "oo"
        paymentStatus = Enum('paymentStatus', 'paid due past_due no_payment_required')

        if payment == 'paid':
            payment_status = paymentStatus.paid.value
        elif payment == 'due':
            payment_status = paymentStatus.due.value
        elif payment == 'past_due':
            payment_status = paymentStatus.past_due.value
        elif payment == 'no_payment_required':
            payment_status = paymentStatus.no_payment_required.value
        else:
            payment_status = 'invalid'
        if payment_status == 'invalid':
            abort(400, 'invalid payment status')

        created_ts = time.time()
        updated_ts = time.time()
        # id = uuid.uuid4()
        owner_id = user_id
    except:
        abort(400, 'invaid details')

    # post values in MySql database tables

    mycursor = mydb.cursor()
    import json

    mylist = json.dumps(category_list)
    # print("json>>>")
    # print(mylist)
    # salt = bcrypt.gensalt()
    # hashed = bcrypt.hashpw(password.encode('utf8'), salt)
    #
    # hash_password = hashed.decode('utf-8')]
    if amount_due <= 0.00:
        abort(400, 'amount is not valid')
    try:
        startCall_db = time.time()
        sql = "UPDATE bill SET vendor = %s,bill_date = %s,due_date = %s, amount_due = %s, categories = %s, paymentStatus = %s WHERE owner_id = %s AND id = %s"
        val = (vendor, bill_date, due_date, amount_due, mylist, payment_status, str(user_id), str(id))
        print(user_id)
        print(id)

        mycursor.execute(sql, val)
        # if mycursor.rowcount < 1:
        #     abort(400,'Wrong user login/bill number')
        mydb.commit()

        "fetch attachment if any"
        mycursor = mydb.cursor()
        print(id)

        sql = "SELECT * FROM file_detail WHERE  bill_id = %s"
        adr = (id,)

        mycursor.execute(sql, adr)
        rows = mycursor.fetchall()
        durCall_db = (time.time() - startCall_db) * 1000
        c.timing("TimerupdatebillDB", durCall_db)
        print("len")
        print(len(rows))

        if len(rows) > 0:
            for k in rows:
                attachment = {
                    'file_name': k[0],
                    'url': k[3],
                    'id': k[2],
                    'upload_date': k[4]
                }


        else:
            attachment = {}

        data = {'id': id,
                'created_ts': created_ts,
                'updated_ts': updated_ts,
                'owner_id': owner_id,
                'vendor': vendor,
                'bill_date': bill_date,
                'due_date': due_date,
                'amount_due': amount_due,
                'categories': json.loads(mylist),
                'payment_status': payment_status,
                'attachment': attachment
                }
        durCall = (time.time() - startCall)*1000
        c.timing("Timerupdatebill", durCall)
        return jsonify(data)
    except:
        return (400, 'invalid data')


# get user details
@app.route("/bill/<id>", methods=["GET"])
@login_required
def getBill(id):
    c.incr('Countgetbill', 1)
    startCall = time.time()
    # take user input
    # pass a global username after validation from above

    email_address = user_name

    # user_id = uuid.uuid4()

    # post values in MySql database tables
    paymentStatus = Enum('paymentStatus', 'paid due past_due no_payment_required')
    if app.config['TESTING'] == True:
        rootpw = 'passw0rd'
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user='user',
            passwd=rootpw,
            database='test_db'
        )
    else:

        mydb = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            database=database

        )
    try:
        mycursor = mydb.cursor()

        sql = "SELECT * FROM bill WHERE id = %s"
        adr = (id,)

        mycursor.execute(sql, adr)
        rows = mycursor.fetchall()
    except:
        abort(400, 'Error in data')
    if len(rows) < 1:
        abort(404, 'invalid  bill details')
    else:
        for x in rows:
            print(x)
            if user_id != x[3]:
                abort(401, 'you are not the bill owner')

            "fetch attachment if any"
            mycursor = mydb.cursor()
            print(id)
            startCall_db = time.time()

            sql = "SELECT * FROM file_detail WHERE  bill_id = %s"
            adr = (id,)

            mycursor.execute(sql, adr)
            rows = mycursor.fetchall()
            durCall_db = (time.time() - startCall_db) * 1000
            c.timing("TimergetbillDB", durCall_db)
            print("len")
            print(len(rows))

            if len(rows) > 0:
                for k in rows:
                    attachment = {
                        'file_name': k[0],
                        'url': k[3],
                        'id': k[2],
                        'upload_date': k[4]
                    }


            else:
                attachment = {}

            data = {'id': x[0],
                    'created_ts': x[1],
                    'updated_ts': x[2],
                    'owner_id': x[3],
                    'vendor': x[4],
                    'bill_date': x[5],
                    'due_date': x[6],
                    'amount_due': x[7],
                    'categories': json.loads(x[8]),
                    'paymentStatus': paymentStatus(int(x[9])).name,
                    'attachment': attachment
                    }
        durCall = (time.time() - startCall)*1000
        c.timing("Timergetbill", durCall)
        return jsonify(data)

    # mycursor.execute(sql, val)


@app.route("/v2/bills", methods=["GET"])
@login_required
def getBills():
    c.incr('Countgetbills', 1)
    startCall = time.time()
    # take user input
    # pass a global username after validation from above

    email_address = user_name

    # user_id = uuid.uuid4()

    # post values in MySql database tables
    paymentStatus = Enum('paymentStatus', 'paid due past_due no_payment_required')
    if app.config['TESTING'] == True:
        rootpw = 'passw0rd'
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user='user',
            passwd=rootpw,
            database='test_db'
        )
    else:

        mydb = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            database=database

        )
    mycursor = mydb.cursor()
    startCall_db = time.time()

    sql = "SELECT * FROM bill WHERE owner_id = %s"
    adr = (user_id,)

    mycursor.execute(sql, adr)
    rows = mycursor.fetchall()
    durCall_db = (time.time() - startCall_db) * 1000
    c.timing("TimergetbillsDB", durCall_db)
    dict = []

    if len(rows) < 1:
        abort(404, 'No bills associated with this user')
    else:

        for x in rows:
            print(len(rows))
            print(x[0])

            if user_id != x[3]:
                abort(401, 'you are not the bill owner')
            data = {'id': x[0],
                    'created_ts': x[1],
                    'updated_ts': x[2],
                    'owner_id': x[3],
                    'vendor': x[4],
                    'bill_date': x[5],
                    'due_date': x[6],
                    'amount_due': x[7],
                    'categories': json.loads(x[8]),
                    'paymentStatus': paymentStatus(int(x[9])).name
                    }
            # dict.append((data))
        durCall = (time.time() - startCall)*1000
        c.timing("Timergetbills", durCall)
        print("her")
        return (jsonify(rows))

    # mycursor.execute(sql, val)


@app.route("/user7", methods=["POST"])
def u1():
    flag = request.data
    print(flag)
    if app.config['TESTING'] == True:
        abort(401)
    else:
        return ""


@app.route("/bill/<id>", methods=["DELETE"])
@login_required
def delBill(id):
    c.incr('Countdeletebill', 1)
    startCall = time.time()
    if app.config['TESTING'] == True:
        rootpw = 'passw0rd'
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user='user',
            passwd=rootpw,
            database='test_db'
        )

    else:
        mydb = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            database=database

        )

    mycursor = mydb.cursor()

    sql = "SELECT * FROM bill WHERE id = %s"
    adr = (id,)

    mycursor.execute(sql, adr)
    rows = mycursor.fetchall()
    if len(rows) < 1:
        abort(404, 'Bill not Found')
    for x in rows:

        if x[3] != user_id:
            abort(401, 'you are not the bill owner')
    try:
        mycursor = mydb.cursor()

        sql = "DELETE FROM bill WHERE  owner_id = %s AND id = %s"
        adr = (user_id, id)

        mycursor.execute(sql, adr)

        mydb.commit()


    except:
        abort(400, 'invalid details')
    print("here to delte file")
    print(id)
    startCall_db = time.time()
    sql = "SELECT * FROM file_detail WHERE  bill_id = %s"
    adr = (id,)
    durCall_db = (time.time() - startCall_db) * 1000
    c.timing("TimerdelbillDB", durCall_db)

    mycursor.execute(sql, adr)
    rows = mycursor.fetchall()
    print("rows")
    print(rows)
    if len(rows) < 1:
        print("do nothing>>")
    else:
        for x in rows:
            filename = x[0]
            print("i got name>")
            print(filename)

    # app.config['UPLOADED_ITEMS_DEST'] = UPLOAD_FOLDER
    # filename='j.pdf'
    # os.remove(os.path.join(app.config['UPLOADED_ITEMS_DEST'], filename))
    print("before try")
    durCall = (time.time() - startCall)*1000
    c.timing("Timerdelbill", durCall)
    try:



        UPLOAD_FOLDER = '/home/pareen/Documents'


        print("bucket")
        print("bucketName")
        app.config['UPLOADED_ITEMS_DEST'] = UPLOAD_FOLDER
        s3 = boto3.resource("s3")
        obj = s3.Object(bucketName, filename)
        obj.delete()

        # os.remove(os.path.join(app.config['UPLOADED_ITEMS_DEST'], filename))

        return 'Done deletion', 204
    except:
        abort(400, 'invalid details')


@app.route("/bill/<bill_id>/file/<file_id>", methods=["PUT"])
@login_required
def updateBillFie(id):
    abort(400, 'Cannot update a attachment')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




def uploadFilenew(id):
    import boto3


    Key = "Original Name and type of the file you want to upload into s3"
    outPutname = "Output file name(The name you want to give to the file after we upload to s3)"
    file = request.files['file']

    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file.filename, bucketName, file.filename)


@app.route("/bill/<id>/file", methods=["POST"])
@login_required

def uploadFile(id):
    c.incr('Countuploadfile', 1)
    startCall = time.time()
    print("metadata777777>>>>>>>>>>>>>>>>")
    print(request.get_json())
    print(">>>>>>>>>>>>>over metadata")
    # check valid bill
    if app.config['TESTING'] == True:
        rootpw = 'passw0rd'
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user='user',
            passwd=rootpw,
            database='test_db'
        )

    else:
        mydb = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            database=database

        )
    mycursor = mydb.cursor()

    sql = "SELECT * FROM bill WHERE  id = %s"
    adr = (id,)
    try:

        mycursor.execute(sql, adr)
        rows = mycursor.fetchall()
    except:
        abort(401, 'invalid details')
    if len(rows) < 1:
        abort(404, ' bill does not exist')
    for x in rows:
        if user_id != x[3]:
            abort(401, 'you are not the authorized owner')

    mycursor = mydb.cursor()
    print(id)

    sql = "SELECT * FROM file_detail WHERE  bill_id = %s"
    adr = (id,)

    mycursor.execute(sql, adr)
    rows = mycursor.fetchall()

    if len(rows) == 1:
        abort(400, 'Delete existing attachment to add new one')
    UPLOAD_FOLDER = '/home/pareen/Documents'
    app.secret_key = "secret key"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    # check if the post request has the file part
    if 'file' not in request.files:
        abort(400, 'invalid details')
    file = request.files['file']
    print(file.filename)
    if file.filename == '':
        abort(400, 'invalid details')
    if file and allowed_file(file.filename):
        file_id = uuid.uuid4()

        filename = secure_filename(file.filename)
        name = filename.split(".")
        newname = name[0] + str(file_id) + "." + name[1]
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], newname))
        # # resp = jsonify({'message': 'File successfully uploaded'})
        # # resp.status_code = 201
        # # return resp
        # file_url = UPLOAD_FOLDER + "/" + newname
        # upload_date = datetime.date.today().strftime('%y-%m-%d')
        # mime = magic.Magic(mime=True)

        upload_date = datetime.date.today().strftime('%y-%m-%d')
        Key = "Original Name and type of the file you want to upload into s3"
        outPutname = "Output file name(The name you want to give to the file after we upload to s3)"
        file = request.files['file']
        url = '/home/ubuntu/' + newname
        file.save(newname)
        startCall_s3 = time.time()
        import boto3
        #http = chilkat.CkHttp()
        s3_client = boto3.client('s3')
        response = s3_client.upload_file(url, bucketName, newname)

        durCall_s3 = (time.time() - startCall_s3) * 1000
        c.timing("TimercreatefileS3", durCall_s3)

        metadata=''
        #retval = http.S3_FileExists(bucketName, file.filename)
        metadata = s3_client.head_object(Bucket=bucketName, Key=newname)
        #metadata = json.dumps(metadata_json)
        startCall_db = time.time()
        sql = "INSERT INTO file_detail (file_name,bill_id,file_id,file_url,upload_date,metadata) VALUES (%s,%s,%s,%s,%s,%s)"

        val = (newname, str(id), str(file_id), str(url), upload_date, str(metadata))

        durCall_db = (time.time() - startCall_db) * 1000
        c.timing("TimercreatefileDB", durCall_db)

        durCall = (time.time() - startCall)*1000
        c.timing("Timercreatefile", durCall)

        mycursor.execute(sql, val)
        mydb.commit()
        data = {'id': file_id,
                'file_name': newname,
                'url': url,
                'upload_date': upload_date,
                'metadata':str(metadata)

                }
        return jsonify(data)
    else:
        resp = jsonify({'message': 'Allowed file types are  pdf, png, jpg, jpeg'})
        resp.status_code = 400
        return resp


@app.route("/bill/<bill_id>/file/<file_id>", methods=["DELETE"])
@login_required
def deleteFile(bill_id, file_id):
    c.incr('Countdeletefile', 1)
    startCall = time.time()
    if len(bill_id) < 1:
        abort(400, 'invalid details')
    if len(file_id) < 1:
        abort(400, 'invalid details')

    UPLOAD_FOLDER = '/home/pareen/Documents'

    if app.config['TESTING'] == True:
        rootpw = 'passw0rd'
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user='user',
            passwd=rootpw,
            database='test_db'
        )

    else:
        mydb = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            database=database

        )

    sql = "SELECT * FROM bill WHERE id = %s"
    adr = (str(bill_id),)
    mycursor = mydb.cursor()

    mycursor.execute(sql, adr)
    rows = mycursor.fetchall()
    if len(rows) < 1:
        abort(404, 'Bill not Found')
    for x in rows:

        if x[3] != user_id:
            abort(401, 'you are not the bill owner')

    mycursor = mydb.cursor()

    sql = "SELECT * FROM file_detail WHERE file_id = %s AND bill_id = %s"
    adr = (file_id, bill_id)

    mycursor.execute(sql, adr)
    rows = mycursor.fetchall()
    print(rows)
    if len(rows) < 1:
        abort(404, 'File / Bill combination not Found')
    else:
        for x in rows:
            filename = x[0]

    # app.config['UPLOADED_ITEMS_DEST'] = UPLOAD_FOLDER
    # filename='j.pdf'
    # os.remove(os.path.join(app.config['UPLOADED_ITEMS_DEST'], filename))
    durCall = (time.time() - startCall)*1000
    c.timing("Timerdeletefile", durCall)
    try:

        mycursor = mydb.cursor()
        startCall_db = time.time()

        sql = "DELETE FROM file_detail WHERE  file_id = %s"
        adr = (file_id,)

        mycursor.execute(sql, adr)

        mydb.commit()
        durCall_db = (time.time() - startCall_db) * 1000
        c.timing("TimerdelbillDB", durCall_db)
        app.config['UPLOADED_ITEMS_DEST'] = UPLOAD_FOLDER
        startCall_s3 = time.time()
        s3 = boto3.resource("s3")
        obj = s3.Object(bucketName, filename)
        obj.delete()
        durCall_s3 = (time.time() - startCall_s3) * 1000
        c.timing("TimerdelfileS3", durCall_s3)

        #os.remove(os.path.join(app.config['UPLOADED_ITEMS_DEST'], filename))

        return 'Done deletion', 204
    except:
        abort(400, 'invalid details')





@app.route("/bill/<bill_id>/file/<file_id>", methods=["GET"])
@login_required
def getFile(bill_id, file_id):
    c.incr('Countgetfile', 1)
    startCall = time.time()
    if len(bill_id) < 1:
        abort(400, 'invalid details')
    if len(file_id) < 1:
        abort(400, 'invalid details')

    UPLOAD_FOLDER = '/home/pareen/Documents'

    if app.config['TESTING'] == True:
        rootpw = 'passw0rd'
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user='user',
            passwd=rootpw,
            database='test_db'
        )

    else:
        mydb = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            database=database

        )

    sql = "SELECT * FROM bill WHERE id = %s"
    adr = (str(bill_id),)
    mycursor = mydb.cursor()

    mycursor.execute(sql, adr)
    rows = mycursor.fetchall()
    if len(rows) < 1:
        abort(404, 'Bill not Found')
    for x in rows:

        if x[3] != user_id:
            abort(401, 'you are not the bill owner')

    startCall_db = time.time()
    mycursor = mydb.cursor()

    sql = "SELECT * FROM file_detail WHERE file_id = %s AND bill_id = %s"
    adr = (file_id, bill_id)
    durCall_db = (time.time() - startCall_db) * 1000
    c.timing("TimergetfileDB", durCall_db)

    mycursor.execute(sql, adr)
    rows = mycursor.fetchall()
    print(rows)
    if len(rows) < 1:
        abort(404, 'File / Bill combination not Found')
    else:
        if len(rows) > 0:
            for k in rows:
                attachment = {
                    'file_name': k[0],
                    'url': k[3],
                    'id': k[2],
                    'upload_date': k[4]
                }

    durCall = (time.time() - startCall)*1000
    c.timing("Timerdelfile", durCall)
    return jsonify(attachment)
@app.route("/", methods=["GET"])
def hello_world():
  app.logger.info('Processing default request in 1>')
  return "Hello from Flask7!"








@app.route("/v1/bill/due/<x>",methods=["GET"])
def get_lambda(x):
    import boto3
    from datetime import datetime, timedelta
    app.logger.info('check here>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.')


    dynamodb = boto3.client('dynamodb',region_name='us-east-1')
    response = dynamodb.get_item(TableName='dynamo', Key={'email_address': {'S': user_name}})
    print("typeeeee")
    print(type(response))

    print("response7777")
    print(response)
    app.logger.info(response)
    app.logger.info('s ')
    c = 0
    k="e"
    app.logger.info('length if response')

    for s in response:
        c = c + len(s)
    if c > 17:
        k="r"

    dynamodb.put_item(TableName='dynamo', Item={'email_address': {'S': user_name}})
    app.logger.info(c)
    app.logger.info('value of k')
    app.logger.info(k)
    app.logger.info('dne777777777777777777')



    import datetime
    d = datetime.datetime.today()
    print(d)
    from datetime import datetime, timedelta
    com_date = (datetime.now() + timedelta(days=int(x)+1)).strftime('%Y-%m-%d')
    if app.config['TESTING'] == True:
        rootpw = 'passw0rd'
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user='user',
            passwd=rootpw,
            database='test_db'
        )

    else:
        mydb = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            database=database

        )

    sql = "SELECT * FROM bill WHERE due_date < %s"
    adr = (str(com_date),)
    mycursor = mydb.cursor()
    links=""

    mycursor.execute(sql, adr)
    rows = mycursor.fetchall()
    print("The original list is : " + str(rows))

    # print(type(l))

    res = [lis[0] for lis in rows]
    # print(res)
    print("h37")
    for i in res:
        print(i)
        links = links + "http://54.146.213.179:8080/bill/"+i +",   "

    message={ "email_address" : user_name,"links" : links,"stat":k}

    sqs = boto3.client('sqs',region_name='us-east-1')

    sns_queue_url = ''




    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageAttributes={
            'Title': {
                'DataType': 'String',
                'StringValue': 'The Whistler'
            },
            'Author': {
                'DataType': 'String',
                'StringValue': 'John Grisham'
            },
            'WeeksOn': {
                'DataType': 'Number',
                'StringValue': '6'
            }
        },
        MessageBody=(
            'Information about current NY Times fiction bestseller for '
            'week of 12/11/2016.'
        )
    )

    import json
    import boto3
    topic_arn = ""
    app.logger.info("message is77>>")
    app.logger.info(message)

    client = boto3.client('sns', region_name='us-east-1')
    response = client.publish(
        TargetArn=arn,
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure='json'
    )

    return "check your email"


@app.route("/user71", methods=["GET"])

def getFiledemo():
    c.incr('testcount1',2)
    app.logger.info('Processing default request in user71')
    return "Hello from Flask7!"



if __name__ == '__main__':
    # db_connection = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="very_strong_password"
    # )

    from ec2_metadata import ec2_metadata

    data = (ec2_metadata.user_data).decode('utf-8')
    print(data)
    k = data.split("\n")
    print("k is 7>>>>>>>>>>>>")
    print(k)
    print("this was k")
    print("\n")
    print("k[0] is>>>>>")
    print(k[0])
    print("\n")
    print("k[1] is>>>")
    print(k[1])
    print("prints are done")

    #
    bucketName = (k[0].split("="))[1]
    #
    #
    host = (k[1].split("="))[1]
    #
    #
    print("db if printed7>>7")
    db_connection = mysql.connector.connect(
         host=host,
         port=port,
         user=user,
         passwd=passwd,
         database=database

     )

    db_cursor = db_connection.cursor()

    db_cursor.execute("CREATE DATABASE IF NOT EXISTS network1")
    print(db_connection)
    db_cursor.execute("use network1")
    db_cursor.execute("drop table if exists bill")
    db_cursor.execute(
         "CREATE TABLE IF NOT EXISTS user_value(id varchar(200), first_name varchar(255), last_name varchar(255), email_address varchar(255), password varchar(255), account_created varchar(255), account_updated varchar(255), salt varchar(255))")
    db_cursor.execute(
        "CREATE TABLE IF NOT EXISTS bill(id varchar(200), created_ts varchar(255), updated_ts varchar(255), owner_id varchar(255), vendor varchar(255), bill_date varchar(255), due_date varchar(255), amount_due varchar(255), categories varchar(255), paymentStatus varchar(255))")
    db_cursor.execute(
         "CREATE TABLE IF NOT EXISTS file_detail(file_name varchar(200), bill_id varchar(255), file_id varchar(255), file_url varchar(255), upload_date varchar(255), metadata varchar(255))")
    print(db_cursor.execute("select * from user_value"))
    #app.config['TESTING'] = False
    #app.run(host="0.0.0.0", port=3000, debug=True)
    print("hello i am in")
    #app.run()
    app.config['TESTING'] = False
    #app.run()
    app.logger.info('Processing default request')
    app.run(host="0.0.0.0", port=8080)
    # print("ok")
