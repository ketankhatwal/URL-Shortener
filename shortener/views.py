from django.shortcuts import render, redirect
from .models import Short
from django.shortcuts import get_object_or_404
from django.contrib import messages
from requests.exceptions import ConnectionError
import re, requests, secrets

#pattern = re.compile(r"(https?://)?(www\.)?(\w+)(\.\w+/?)/?(.*)")
pattern = re.compile(r"((http|ftp|https)://)?([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?")

def home(request):
    data = None
    if request.method == "POST":
        url = request.POST["actual_url"]
        custom = request.POST["custom"]
        custom = custom.lower()
        match = pattern.findall(url)
        #host_url = request.build_absolute_uri()
        host_url = "https://uvshort.herokuapp.com/"
        print(match)
        if len(match) == 0:
            messages.warning(request,"Enter valid URL")
        else:
            if not match[0][0]:
                old_url = "https://"+match[0][2]+match[0][3]
            else:
                old_url = match[0][0]+match[0][2]+match[0][3]
            print(old_url)
            try:
                r = requests.get(old_url)
                if custom != "":
                    hosts = Short.objects.all()
                    for host in hosts:
                        custom_link = host.shortened_url
                        custom_link = custom_link.split("/")
                        custom_link = custom_link[-1]
                        #print(custom_link)
                        if custom_link == custom:
                            messages.warning(request,"The given custom name is already taken. Please, try again!")
                            return redirect('home')
                        else:
                            rand_bits = custom
                else:
                    rand_bits = secrets.token_urlsafe(8)
                new_url = host_url + rand_bits
                data = new_url
                data = Short(actual_url = old_url, shortened_url = new_url)
                data.save()
            except ConnectionError:
                 messages.warning(request,"The link provided is not for a working website. Please, try again!")
               
    return render(request,'shortener/home.html',{'data':data})

def test(request):
    return render(request,'shortener/test.html')

def about(request):
    return render(request,'shortener/about.html')

def decompress(request,compressed):
    new_url = "https://uvshort.herokuapp.com/" + compressed
    #new_url = "http://127.0.0.1:8000/"+ compressed
    data = get_object_or_404(Short, shortened_url = new_url)
    #data = Short.objects.get(shortened_url = new_url)
    #print(data)
    r = data.actual_url
    return redirect(r)

