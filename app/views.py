import string

from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
import random
from django.core.mail import send_mail

# Create your views here.
def xyz(request):
    return render(request, "home.html")

def signup(request):
    email = request.POST['email']
    psw = request.POST['password']
    cursor = connection.cursor()
    query1 = "select * from users where email='"+email+"'"
    cursor.execute(query1)
    data = cursor.fetchall()
    if len(data) > 0:
        data = {'email': "Already User", 'password': " "}
        return render(request, "first.html", data)
    else:
        otp = random.randint(100000, 900000)
        strotp = str(otp)
        query2 = "insert into users (email, password, otp) values(%s, %s, %s)"
        values2 = (email, psw, strotp)
        cursor.execute(query2, values2)
        body = 'your otp is '+strotp+''
        send_mail("OTP Verification", body,"yamanpaeek818@gmail.com", [email])
        data = {'email': email}
        return render(request, "signupsucces.html", data)

def signin(request):
    return render(request,"login.html")

def login(request):
    email = request.POST['email']
    psw = request.POST['password']
    cursor = connection.cursor()
    query1 = "select * from users where email='" + email + "'"
    cursor.execute(query1)
    data = cursor.fetchone()
    if data is None:
        data = {'email': "Not signedUp", 'password': " "}
        return render(request, "first.html", data)
    else:
        if data[1] == psw:
            data = {'email': "login complete", 'password': " "}
            return render(request, "first.html", data)
        else:
            data = {'email': "password is wrong", 'password': " "}
            return render(request, "first.html", data)

def otpVarify(request):
    email = request.POST['email']
    otp = request.POST['otp']
    cursor = connection.cursor()
    query1 = "select * from users where email='" + email + "'"
    cursor.execute(query1)
    data = cursor.fetchone()
    if data is not None:
        if data[3] == otp:
            query2 = "update users set is_verify =1 where email='" + email + "'"
            cursor.execute(query2)
            if cursor.rowcount == 1:
                print("OTP Verified")
                data = {'email': "OTP Verified"}
                return render(request, "first.html", data)
        else:
            data = {'email': "OTP Not Verified"}
            return render(request, "first.html", data)
def generateShortURL(request):
    letters = string.ascii_letters + string.digits
    shortUrl = ' '
    for i in range(5):
        shortUrl = shortUrl + ''.join(random.choice(letters))
    return shortUrl

def urlshortner(request):
    longLink = request.GET['link']
    customUrl = request.GET["customurl"]
    if customUrl is None or customUrl == '':
        shortUrl = generateShortURL(request)
    else:
        cursor = connection.cursor()
        query1 = "select * from links where short_link ='" + customUrl + "'"
        cursor.execute(query1)
        data = cursor.fetchone()
        if data is not None:
            data = {'email': "This URL already used try another."}
            return render(request, "first.html", data)
        else:
            query2 = "insert into links (long_link, short_link) values(%s, %s)"
            value = (longLink, customUrl)
            cursor.execute(query2, value)
            data = {'email': "Your url is shortne with nano.co/"+customUrl}
            return render(request, "first.html", data)
    if shortUrl is not None or shortUrl != '':
        cursor = connection.cursor()
        query1 = "select * from links where short_link ='" + shortUrl + "'"
        cursor.execute(query1)
        data = cursor.fetchone()
        if data is not None:
            data = {'email': "This URL already used try another."}
            return render(request, "first.html", data)
        else:
            query2 = "insert into links (long_link, short_link) values(%s, %s)"
            values2 = (longLink, shortUrl)
            cursor.execute(query2, values2)
            data = {'email': "Your url is shortne with nano.co/'"+shortUrl+"'"}
            return render(request, "first.html", data)


