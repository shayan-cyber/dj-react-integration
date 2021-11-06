from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from . models import Tweet
import random
from . forms import TweetForm
from django.conf import settings
from django.utils.http import is_safe_url

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request):
    # return HttpResponse("hello")
    return render(request,'pages/home.html', context={}, status=200)

def tweet_create_view(request):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form  = TweetForm(request.POST or None)

    next_url = request.POST.get('next') or None
    print(request.is_ajax())
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user =user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
        
        if next_url != None and is_safe_url(next_url,ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request,'components/form.html', context={"form": form}, status=200)

def tweet_list_view(request):
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs ]

    data ={
        "isUser":False,
        "response":tweets_list,
    }

    return JsonResponse(data)


def tweet_detail_view(request, tweet_id):
    data ={
        "id":tweet_id,
        
        
    }
    status =200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data["content"] = obj.content
    except:
        data["message"]= "Not found"
        status =404
    
    # return HttpResponse(f"{tweet_id}-{obj.content}")
    return JsonResponse(data, status=status)