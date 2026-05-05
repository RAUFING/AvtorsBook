from django.shortcuts import render, redirect
from django.http import *
from .forms import LoginForm, RegisterForm, CreateBook, Filter, CreateComment
from .models import Users_Book, Book, Commnet
from django import forms


import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import string
import random

import smtplib

# Create your views here.
#if request.session['Auth_Name'] != 'None':
#    auth = True

def send_email(to_addr, subject, text):
    msg = MIMEMultipart()
    msg['From'] = "avtorsbooks@mail.ru"
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(text, 'plain'))
    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    server.ehlo("avtorsbooks@mail.ru")
    server.login("avtorsbooks@mail.ru", 'ILoveKolobok12!')
    server.auth_plain()
    server.send_message(msg)
    server.quit()
def index(request):
    
    try:
        if request.session['Auth_Name'] == 'True':
            pass
        if request.session['Auth_Name'] != 'None':
            auth = "True"
        else:
            auth = 'False'
    except:
        request.session['Auth_Name'] = 'None'
        request.session['Auth_Password'] = 'None'
        auth = "False"
    if request.method == 'POST' :
        if request.POST.get('search') != None:
            site = request.POST.get('search')
            return redirect(f'/book_filter/{site}')
    
        
    try:
        if request.session['FirstName'] != 'None' and request.session['LastName'] != None:
            data = {'creators': request.session['FirstName'] + ' ' + request.session['LastName']}
        else:
            data = {'creators': "Войдите в систему"}
    except:
        data = {'creators': "Войдите в систему"}
    data['filter'] = Filter()
    data['auth'] = auth
    spisok = []
    books = Book.objects.all()
    for i in books:
        spisok.append(i.title)
    data['books'] = spisok

    return render(request, "index.html", context=data)

def login(request):
    try:
        if request.session['Auth_Name'] != 'None':
            auth = "True"
        else:
            auth = 'False'
    except:
        request.session['Auth_Name'] = 'None'
        request.session['Auth_Password'] = 'None'
        auth = "False"
    if request.method == 'POST' :
        if request.POST.get('search') != None:
            site = request.POST.get('search')
            return redirect(f'/book_filter/{site}')
    
    # try:users = Users_Book.objects.all(username = request.session['Auth_Name'], password=request.session['Auth_Password'])
    # except:
    #     request.session['Auth_Name'] = 'None'
    #     request.session['Auth_Password'] = 'None'
    
        
    if request.session['Auth_Name'] == 'None':
        if request.method == "POST":
            name = request.POST.get('username')
            password = request.POST.get('password')
            try:
                users = Users_Book.objects.get(username = name)
                if users.password == password:
                    request.session['Auth_Name'] = users.username
                    request.session['Auth_Password'] = users.password
                    request.session['FirstName'] = users.firstname
                    request.session['LastName'] = users.lastname
                    mata = {'message':'Вы вошли в систему', 'auth':auth}
                    return render(request, 'mesage.html', context=mata)
            except Users_Book.DoesNotExist:
                mata = {'message':'Такого пользователя не существует!', 'auth':auth}
                return render(request, 'mesage.html', context=mata)
            mata = {'message':'Пароль не верный', 'auth':auth}
            return render(request, 'mesage.html', context=mata)
        login_form = LoginForm()
        data = {'form':login_form, 'auth':auth}
        return render(request, 'login.html', context=data)
    mata = {'message':'Вы уже авторизованны! Сначало нужно выйти из аккаунта', 'auth':auth}
    return render(request, 'mesage.html', context=mata)

def logout(request):
    try:
        if request.session['Auth_Name'] != 'None':
            auth = "True"
        else:
            auth = 'False'
    except:
        request.session['Auth_Name'] = 'None'
        request.session['Auth_Password'] = 'None'
        auth = "False"
    if request.method == 'POST' :
        if request.POST.get('search') != None:
            site = request.POST.get('search')
            return redirect(f'/book_filter/{site}')
    
    if request.session['Auth_Name'] == 'None':
        mata = {'message':'Что бы выйти нужно сначало авторизоваться', 'auth':auth}
        return render(request, 'mesage.html', context=mata)
    if request.method == 'POST':
        request.session['Auth_Name'] = 'None'
        request.session['Auth_Password'] = 'None'
        request.session['FirstName'] = 'None'
        request.session['LastName'] = 'None'
        mata = {'message':'Вы вышли из системы!', "auth":auth}

        return render(request, 'mesage.html', context=mata)
    
    
    return render(request, 'logout.html', context={'auth':auth})

def register(request):
    try:
        if request.session['Auth_Name'] != 'None':
            auth = "True"
        else:
            auth = 'False'
    except:
        request.session['Auth_Name'] = 'None'
        request.session['Auth_Password'] = 'None'
        auth = "False"
    if request.method == 'POST' :
        if request.POST.get('search') != None:
            site = request.POST.get('search')
            return redirect(f'/book_filter/{site}')
    
    
    if request.session['Auth_Name'] == 'None':
        if request.method == 'POST':
            
            request.session['potv'] = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters)
            to = request.session['potv']
            request.session['potvi'] = 'True'
            send_email(request.POST.get('mail'), 'Потвердите свой адрес!', f'Здравствуйте, вас тревожит администрация сайта AvtorBook\n ваш код потверждения: {to}\nС уважением администрация сайта AvtorBook')
            
            request.session['usernamereg'] = request.POST.get('username')
            request.session['passwordreg'] = request.POST.get('password')
            request.session['mailreg'] = request.POST.get('mail')
            request.session['firstnamereg'] = request.POST.get('firstname')
            request.session['lastnamereg'] = request.POST.get('username')
            return redirect('/potv/')
            '''
            client = Users_Book()
            client.username = request.POST.get('username')
            client.password = request.POST.get('password')
            
            client.mail = request.POST.get('mail')
            client.firstname = request.POST.get('firstname')
            client.lastname = request.POST.get('lastname')
            
            client.count_public_book = 0
            client.save()
            request.session['Auth_Name'] = client.username
            request.session['Auth_Password'] = client.password
            request.session['FirstName'] = client.firstname
            request.session['LastName'] = client.lastname
            mata = {'message':'Ваш аккаунт зарегестрирован!', 'auth':auth}
            return render(request, 'mesage.html', context=mata)
            '''
        reg_form = RegisterForm()
        data = {'form': reg_form}
        return render(request, 'register.html', context=data)
    mata = {'message':'Вы уже авторизованны!', 'auth':auth}
    return render(request, 'mesage.html', context=mata)

def view_book(request, id):
    # try:users = Users_Book.objects.all(username = request.session['Auth_Name'], password=request.session['Auth_Password'])
    # except:
    #     request.session['Auth_Name'] = 'None'
    #     request.session['Auth_Password'] = 'None'
    try:
        if request.session['Auth_Name'] != 'None':
            auth = "True"
        else:
            auth = 'False'
    except:
        request.session['Auth_Name'] = 'None'
        request.session['Auth_Password'] = 'None'
        auth = "False"
    if request.method == 'POST' :
        if request.POST.get('search') != None:
            site = request.POST.get('search')
            return redirect(f'/book_filter/{site}')
    try:
        book = Book.objects.get(title=id)
        if request.method == 'POST':
            txt = request.POST.get('text')
            comment = Commnet()
            comment.author = request.session['Auth_Name']
            comment.book = book.title
            comment.comment = txt
            comment.save()
        
        try:
            if request.session[book.title] != True:
                book.see += 1
                book.save()
                request.session[book.title] = True
        except:
            request.session[book.title] = False
        author = ''
        author_id = book.author
        user = Users_Book.objects.get(username=author_id)
        
        author = author + f"{user.firstname} {user.lastname}"
        com = Commnet.objects.all()
        spisokcom = []
        for i in reversed(com): 
            if i.book == book.title:
                spisokcom.append(f'''
_________________
Автор коментария: {i.author}

        -{i.comment}
_________________''')
    
        data = {'titlebook':book.title, 'textbook':book.text, 'predbook':book.pred, 'author':author, 'date':book.date, "author_id":author_id, 'see':book.see, 'auth':auth}
        if request.session['Auth_Name'] != "None":
            
            data['form'] = CreateComment()
        else:
            data['form'] = "Auth"
        data['comments'] = spisokcom
        return render(request, 'bookview.html', context=data)
    except Book.DoesNotExist:
        mata = {'message':'Такой книги нет!', 'auth':auth}
        return render(request, 'mesage.html', context=mata)
    

def view_profile(request, username):
    try:
        if request.session['Auth_Name'] != 'None':
            auth = "True"
        else:
            auth = 'False'
    except:
        request.session['Auth_Name'] = 'None'
        request.session['Auth_Password'] = 'None'
        auth = "False"
    if request.method == 'POST' :
        if request.POST.get('search') != None:
            site = request.POST.get('search')
            return redirect(f'/book_filter/{site}')
    
    # try:users = Users_Book.objects.all(username = request.session['Auth_Name'], password=request.session['Auth_Password'])
    # except:
    #     request.session['Auth_Name'] = 'None'
    #     request.session['Auth_Password'] = 'None'
    
    try:
        user = Users_Book.objects.get(username=username)
        username = user.username
        firstname = user.firstname
        lastname = user.lastname
        allname = firstname + ' ' + lastname
        books = user.count_public_book
        desc = user.desc
        data = {'allname': allname, 'firstname':firstname, 'lastname':lastname, "username":username, 'books':books, 'desc':desc, 'auth':auth}
        return render(request, 'userview.html', context=data)
    except Users_Book.DoesNotExist:
        mata = {'message':'Такой пользователь не найден!', 'auth':auth}
        return render(request, 'mesage.html', context=mata)

def filter_book(request, name):
    # try:users = Users_Book.objects.all(username = request.session['Auth_Name'], password=request.session['Auth_Password'])
    # except:
    #     request.session['Auth_Name'] = 'None'
    #     request.session['Auth_Password'] = 'None'
    try:
        if request.session['Auth_Name'] != 'None':
            auth = "True"
        else:
            auth = 'False'
    except:
        request.session['Auth_Name'] = 'None'
        request.session['Auth_Password'] = 'None'
        auth = "False"
    if request.method == 'POST' :
        if request.POST.get('search') != None:
            site = request.POST.get('search')
            return redirect(f'/book_filter/{site}')
    
    if request.method == 'POST':
        site = request.POST.get('search')
        return redirect(f'/book_filter/{site}')
    spisok_filter = []
    name = name.lower()
    books = Book.objects.all()
    for i in books:
        pro = i.title.lower()
        if name in pro:
            spisok_filter.append(i.title)
    data = {'filter':name, 'books':spisok_filter, 'auth':auth}
    data['filterstroka'] = Filter()
    return render(request, 'filter.html', context=data)

def filter_profile(request, name):
    try:
        if request.session['Auth_Name'] != 'None':
            auth = "True"
        else:
            auth = 'False'
    except:
        request.session['Auth_Name'] = 'None'
        request.session['Auth_Password'] = 'None'
        auth = "False"
    if request.method == 'POST' :
        if request.POST.get('search') != None:
            site = request.POST.get('search')
            return redirect(f'/book_filter/{site}')
    
        if request.POST.get('searchpro') != None:
            site = request.POST.get('searchpro')
            return redirect(f"/profile_filter/{site}")
    spisok_filter = []
    name = name.lower()
    profiles = Users_Book.objects.all()
    for i in profiles:
        pro = i.username.lower()
        if name in pro:
            spisok_filter.append(i.username)
    
    data = {'filter':name, 'profiles':spisok_filter, 'auth':auth}
    
    return render(request, 'filterpro.html', context=data)

def addbook(request):
    # try:users = Users_Book.objects.all(username = request.session['Auth_Name'], password=request.session['Auth_Password'])
    # except:
    #     request.session['Auth_Name'] = 'None'
    #     request.session['Auth_Password'] = 'None'
    try:
        if request.session['Auth_Name'] != 'None':
            auth = "True"
        else:
            auth = 'False'
    except:
        request.session['Auth_Name'] = 'None'
        request.session['Auth_Password'] = 'None'
        auth = "False"
    if request.method == 'POST' :
        if request.POST.get('search') != None:
            site = request.POST.get('search')
            return redirect(f'/book_filter/{site}')
    
    if request.session['Auth_Name'] == 'None':
        mata = {'message':'Отказано в доступе! Сначало авторизуйтесь!', 'auth':auth}
        return render(request, 'mesage.html', context=mata)
    user = Users_Book.objects.get(username=request.session['Auth_Name'])
    if user.count_public_book >= 10:
        mata = {'message':'Отказанно в доступе! Слишком много книг!', 'auth':auth}
        return render(request, 'mesage.html', context=mata)
    if request.method == 'POST':
        book = Book()
        book.author = user.username
        book.title = request.POST.get('title')
        book.pred = request.POST.get('opis')
        book.text = request.POST.get('text')
        book.see = 0
        
        book.save()
        user.count_public_book += 1
        user.save()
        mata = {'message':'Ваша книга созданна!', 'auth':auth}
        return render(request, 'mesage.html', context=mata)
    form = CreateBook()
    data = {'form':form, 'auth':auth}
    return render(request, 'addbook.html', context=data)

def admin(request):
    try:
        if request.session['Auth_Name'] == 'True':
            pass
    except:
        request.session['Auth_Name'] = 'None'
        request.session['Auth_Password'] = 'None'
    return HttpResponse(str(request.session['Auth_Name']) +' ' + str(request.session['Auth_Password']))

def editbook(request, id):
    try:
        if request.session['Auth_Name'] != 'None':
            auth = "True"
        else:
            auth = 'False'
    except:
        request.session['Auth_Name'] = 'None'
        request.session['Auth_Password'] = 'None'
        auth = "False"
    if request.method == 'POST' :
        if request.POST.get('search') != None:
            site = request.POST.get('search')
            return redirect(f'/book_filter/{site}')
    
    try:
        book = Book.objects.get(title=id)
        try:
            user = Users_Book.objects.get(username=request.session['Auth_Name'])
        except:
            mata = {'message':'Надо авторизоваться!', 'auth':auth}
            return render(request, 'mesage.html', context=mata) 
        if user.username != book.author:
            mata = {'message':'Это не ваша книга!', 'auth':auth}
            return render(request, 'mesage.html', context=mata)
        
        if request.method == 'POST':
            book.pred = request.POST.get('opis')
            book.text = request.POST.get('text')
            book.save()
            mata = {'message':'Книга отредактированна!', 'auth':auth}
            return render(request, 'mesage.html', context=mata)
        else:
            pred = book.pred
            textbook = book.text
            class EditBook(forms.Form):
                opis = forms.CharField(label='Введите описание книги:', widget=forms.Textarea(attrs={'cols': 20, 'rows': 10, 'class':'form-control'}), initial=pred)
                text = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'cols': 70, 'rows': 10}), initial=textbook)
            form = EditBook()
            data = {'form':form, 'auth':auth}
            return render(request, 'editbook.html', context=data)
            
        
    except Book.DoesNotExist:
        mata = {'message':'Книга не найдена', 'auth':auth}
        return render(request, 'mesage.html', context=mata)

def deletebook(request, id):
    try:
        if request.session['Auth_Name'] != 'None':
            auth = "True"
        else:
            auth = 'False'
    except:
        request.session['Auth_Name'] = 'None'
        request.session['Auth_Password'] = 'None'
        auth = "False"
    if request.method == 'POST' :
        if request.POST.get('search') != None:
            site = request.POST.get('search')
            return redirect(f'/book_filter/{site}')
    
    try:
        book = Book.objects.get(title=id)
        try:
            user = Users_Book.objects.get(username=request.session['Auth_Name'])
        except:
            mata = {'message':'Надо авторизоваться!', 'auth':auth}
            return render(request, 'mesage.html', context=mata)
        if user.username != book.author:
            mata = {'message':'Это не ваша книга', 'auth':auth}
            return render(request, 'mesage.html', context=mata)
        
        if request.method == 'POST':
            com = Commnet.objects.all()
            for i in com:
                if i.book == book.title:
                    i.delete()
            book.delete()
            user.count_public_book -= 1
            user.save()
            
            
            mata = {'message':'Книга удаленна!', 'auth':auth}
            return render(request, 'mesage.html', context=mata)
        else:
            data = {'name':id, "auth":auth}
            return render(request, 'deletebook.html', context=data)
            
        
    except Book.DoesNotExist:
        mata = {'message':'Книга не найдена!', "auth":auth}
        return render(request, 'mesage.html', context=mata)

def editprofile(request):
    try:
        if request.session['Auth_Name'] != 'None':
            auth = "True"
        else:
            auth = 'False'
    except:
        request.session['Auth_Name'] = 'None'
        request.session['Auth_Password'] = 'None'
        auth = "False"
    if request.method == 'POST' :
        if request.POST.get('search') != None:
            site = request.POST.get('search')
            return redirect(f'/book_filter/{site}')
    
    try:
        user = Users_Book.objects.get(username=request.session['Auth_Name'])
    except:
        mata = {'message':'Надо авторизоваться!', 'auth':auth}
        return render(request, 'mesage.html', context=mata)
    if user.username != request.session['Auth_Name']:
        mata = {'message':'Это не ваш профиль', "auth":auth}
        return render(request, 'mesage.html', context=mata)
        
    if request.method == 'POST':
        user.desc = request.POST.get('desc')
        user.firstname = request.POST.get('firstname')
        user.lastname = request.POST.get('lastname')
        request.session['FirstName'] = user.firstname
        request.session['LastName'] = user.lastname
        user.save()
        
        mata = {'message':'Профиль отредактирован!', "auth":auth}
        return render(request, 'mesage.html', context=mata)
    else:

        class EditProfile(forms.Form):
            firstname = forms.CharField(label='Имя',max_length=30, initial=user.firstname, widget=forms.TextInput(attrs={'class':'form-control'}))
            lastname = forms.CharField(label='Фамилия',max_length=30, initial=user.lastname)
            desc = forms.CharField(label="Описание",widget=forms.Textarea(attrs={'cols': 70, 'rows': 10, 'class':'form-control'}), max_length=10000, initial=user.desc)
        form = EditProfile()
        data = {'form':form, 'auth':auth}
        return render(request, 'editprofile.html', context=data)
            

def str_mess(request, strtext):
    try:
        if request.session['Auth_Name'] != 'None':
            auth = "True"
        else:
            auth = 'False'
    except:
        request.session['Auth_Name'] = 'None'
        request.session['Auth_Password'] = 'None'
        auth = "False"
    if request.method == 'POST' :
        if request.POST.get('search') != None:
            site = request.POST.get('search')
            return redirect(f'/book_filter/{site}')
    if strtext == 'pronas':
        return render(request, 'pronas.html', context={'auth':auth})
    if strtext == 'politica':
        return render(request, 'politica.html', context={'auth':auth})
    return render(request, 'mesage.html', context={'auth':auth, 'message':'Нету такой страницы!'})

def view_all_book(request, name):
    try:
        if request.session['Auth_Name'] != 'None':
            auth = "True"
        else:
            auth = 'False'
    except:
        request.session['Auth_Name'] = 'None'
        request.session['Auth_Password'] = 'None'
        auth = "False"
    if request.method == 'POST' :
        if request.POST.get('search') != None:
            site = request.POST.get('search')
            return redirect(f'/book_filter/{site}')
    books = Book.objects.all()
    
    if name=='pop':
        spisok = []
        spisok_max = {}
        tochno_spisok = []
        for i in books:
            spisok_max[i.title] = i.see
        for value in spisok_max:
            item = spisok_max[value]
            spisok.append(item)
        nashbook = max(spisok)
        for i in range(nashbook, 1, -1):
            try:
                book = Book.objects.get(see=i)
                tochno_spisok.append(book.title)
            except:
                pass
            
        data = {'auth':auth, 'popbooks':tochno_spisok, 'name':name}
        return render(request,'allbooks.html', context=data)
    elif name=='new':
        spisok = []
        for i in reversed(books):
            spisok.append(i.title)
        data = {'auth':auth, 'newbooks':spisok, 'name':name}
        return render(request,'allbooks.html', context=data)
    elif name=='opros':
        spisok = []
        for i in books:
            if i.see == 0:
                spisok.append(i)
        data = {'auth':auth, 'obooks':spisok, 'name':name}
        return render(request,'allbooks.html', context=data)


    else:
        return render(request, 'mesage.html', context={'auth':auth, 'message':'Нету такой страницы!'})

def delete_page(request):
    try:
        if request.session['Auth_Name'] != 'None':
            auth = "True"
        else:
            auth = 'False'
    except:
        request.session['Auth_Name'] = 'None'
        request.session['Auth_Password'] = 'None'
        auth = "False"
    if request.method == 'POST' :
        if request.POST.get('search') != None:
            site = request.POST.get('search')
            return redirect(f'/book_filter/{site}')
    if auth == 'False':
        return render(request, 'mesage.html', context={'auth':auth, 'message':'Для начало авторизуйтесь!'})
    else:
        spisok = []
        books = Book.objects.all()
        for i in books:
            if i.author == request.session['Auth_Name']:
                spisok.append(i)
        data = {'auth':auth, 'mybooks':spisok}
        return render(request,'delpage.html', context=data)
def potv(request):
    try:
        if request.session['Auth_Name'] != 'None':
            auth = "True"
        else:
            auth = 'False'
        
    except:
        request.session['Auth_Name'] = 'None'
        request.session['Auth_Password'] = 'None'
        auth = "False"
    if request.method == 'POST' :
        if request.POST.get('search') != None:
            site = request.POST.get('search')
            return redirect(f'/book_filter/{site}')
    try:
        if request.session['potvi'] == 'False':
            return redirect('/')
    except:
        return redirect('/')
    if request.method == 'POST':
        txt = request.POST.get('text')
        if txt == request.session['potv']:
            client = Users_Book()
            client.username = request.session['usernamereg']
            client.password = request.session('passwordreg')
            
            client.mail = request.session['mailreg']
            client.firstname = request.session['firstnamereg']
            client.lastname = request.session['lastnamereg']
            
            client.count_public_book = 0
            client.save()
            request.session['Auth_Name'] = client.username
            request.session['Auth_Password'] = client.password
            request.session['FirstName'] = client.firstname
            request.session['LastName'] = client.lastname
            mata = {'message':'Ваш аккаунт зарегестрирован!', 'auth':auth}
            request.session['potvi'] = 'False'
            return render(request, 'mesage.html', context=mata)


    class Potv(forms.Form):
        text = forms.CharField(label='Введите код потверждения:', max_length=6)
    form = Potv()
    data = {'auth':auth, 'form':form}
    return render(request,'allbooks.html', context=data)

def profilespage(request):
    try:
        if request.session['Auth_Name'] != 'None':
            auth = "True"
        else:
            auth = 'False'
        
    except:
        request.session['Auth_Name'] = 'None'
        request.session['Auth_Password'] = 'None'
        auth = "False"
    if request.method == 'POST' :
        if request.POST.get('search') != None:
            site = request.POST.get('search')
            return redirect(f'/book_filter/{site}')
        if request.POST.get('searchpro') != None:
            site = request.POST.get('searchpro')
            return redirect(f"/profile_filter/{site}")
    allpro = Users_Book.objects.all()
    profiles = []
    for i in allpro:
        profiles.append(i.username)
    
    data = {'auth':auth, 'username':request.session['Auth_Name'], 'data':profiles}

    return render(request, 'propage.html', context=data)
