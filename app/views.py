from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
# Create your views here.
def xyz(request):
    return render(request,"index.html")

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
        query2 = "insert into users (email, password) values(%s,%s)"
        values2 = (email, psw)
        cursor.execute(query2, values2)
        data = {'email': email, 'password': psw}
        return render(request, "first.html", data)

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
