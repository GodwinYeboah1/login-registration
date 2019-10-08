from django.shortcuts import render, redirect
from .models import User

# Create your views here.
def home(r):
    return render(r,'home.html')

def create_user(r):
    nuser = User.objects.register(first_name=r.POST['first_name'],last_name=r.POST['last_name'], password=r.POST['password'],conf_password=r.POST['pw_confirmation'], email=r.POST['email'])
    print(nuser)

    if nuser['valid']:
        r.session['user_id'] = nuser['user'].id
    return redirect('/')

def login_user(r):
    luser = User.objects.login(email= r.POST['email'], password=r.POST['pw'])

    if luser['valid']:
        r.session['login_user'] = luser['user'].id
        return redirect('/success')

    return redirect('/')

def display_success_page(r):
    # response = {
    #     'user': r.session['login_user_id']
    # }

    print('Login obj:', r.session['login_user'])
    display_user = User.objects.get(pk=r.session['login_user'])
    print(display_user)
    context = {'login_user': display_user}
    return render(r,'success.html',context)

def logout(r):
    r.session.clear()
    return redirect("/")