from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from apps.models import Feedback
from newspaper import Article

def fetch_article_summary(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        try:
            # Initialize article object
            article = Article(url)
            # Download and parse the article
            article.download()
            article.parse()
            # Fetch the article summary
            article.nlp()
            summary = article.summary
            return render(request, 'fetch_summary.html', {'summary': summary})
        except Exception as e:
            error_message = str(e)
            return render(request, 'error.html', {'error_message': error_message})
    return render(request, 'fetch_summary.html')



@login_required
def HomePage(request):
    return render(request, 'home.html', {})


def Register(request):
    if request.method == 'POST':
        name = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('pass')

        new_user = User.objects.create_user(name, email, password)
        new_user.save()
        return redirect('login')

    return render(request, 'register.html', {})


def Login(request):
    if request.method == 'POST':
        name = request.POST.get('uname')
        password = request.POST.get('pass')

        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Error, user does not exist')

    return render(request, 'login.html', {})


def logoutuser(request):
    logout(request)
    return redirect('login')


def feedback(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phonenumber = request.POST['phonenumber']
        feedback = request.POST['feedback']
        ins = Feedback(name=name, email=email, phonenumber=phonenumber, feedback=feedback)
        ins.save()
        print("ok")
    return render(request, 'feedback.html', {})


def contact(request):
    return render(request, 'contact.html',{})


def precautions(request):
    return render(request, 'p.html',{})