from django.shortcuts import render,redirect
from django.http import JsonResponse
import openai
from django.contrib import auth
from django.contrib.auth.models import User #user  model
from .models import Chat
from django.utils import timezone

# Create your views here.
openapi_key='insert you api key here'
openai.api_key=openapi_key

def ask_openai(message):
    response=openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Updated to a more recent model
        messages=[
            {"role":"system","content":"You are helpful"},
            {"role": "user", "content": message},
        ],
        # model="text-davinci-003",
        # prompt=message,
        # max_token=150,
        # n=1,
        # stop=None,
        # temperature=0.7 #parameters needed for api
    )
    answer=response.choices[0].message.content.strip() #returns a dictionary in which chioces is first hence [0],in that the actual repsonse is stored in text 
    return answer
def chatbot(request):
    chats=Chat.objects.filter(user=request.user) #return the previous chats of the user when he/she logs in
    
    if request.method=='POST':
        message=request.POST.get('message') #users message
        response=ask_openai(message)
        chat=Chat(user=request.user,message=message,response=response,created_at=timezone.now)#saving user name,message and ai repsonse wit the time
        chat.save()
        return JsonResponse({'message':message,'response':response})
    return render(request,'chatbot.html',{'chats':chats})
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        Password=request.POST['password']
        user=auth.authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('chatbot')#if user is valid redirect to chatbot
        else:
            error_message='Invaldi Username or Password'
            return render(request,'login.html',{'error_message':error_message})
    else:
        return render (request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if password1==password2:
            try:
                user=User.objects.create_user(username,email,password1)
                user.save()
                auth.login(request,user) #login automatically
                return redirect('chatbot')

            except:
                error_message='Error'
                return render (request,'register.html',{'error_message':error_message})
        else:
            error_message='Password do not match'
            return render (request,'register.html',{'error_message':error_message})
    return render (request,'register.html')
