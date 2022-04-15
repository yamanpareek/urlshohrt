from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
# Create your views here.
def xyz(request):
    return render(request,"index.html")
def signup(request):
    email = request.GET['email']
    psw = request.GET['password']
    data = {'email': email, 'password': psw}
    cursor = connection.cursor()
    query = "insert into users (email, password) values(%s,%s)"
    values = (email, psw)
    cursor.execute(query, values)
    # query = "select * from city where name='"+email+"'"
    # cursor.execute(query)
    # row = cursor.fetchone()
    # print(row)
    return render(request, "first.html", data)
