import json
from django.shortcuts import render
from .models import Room

def my_simple_view(request,room_name):
    context = {'room': room_name }
    return render(request,'simple_home.html')

def my_text_view(request,room_name,user_name):
    context = {'room':room_name,'user':request.user}
    return render(request,'text_home.html',context)    

def my_temp_view(request,room_name,user_name):
    context = {'room':room_name}
    return render(request,'temp_home.html',context)

def my_db_text_view(request,room_name,user_name):
    room, created = Room.objects.get_or_create(name=room_name)
    context = {'room':room, 'user':request.user}
    return render(request,'db_text_home.html',context) 

def my_db_temp_view(request,room_name,user_name):
    room, created = Room.objects.get_or_create(name=room_name)
    context = {'room':room, 'user':request.user}
    return render(request,'db_temp_home.html',context) 

def passing_msg_view(request,room_name):
    message = request.GET.get('msg') 
    sender = request.GET.get('sndr')
    user = request.user.username
    print(request.user)
    template = 'msg_in.html' 
    if user == sender:
        template = 'msg_out.html'
    context = {'message' : message} 

    return render(request,template,context)