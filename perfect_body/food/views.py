from django.http import HttpResponse
from django.shortcuts import render
from .helper import crawl_food


def food(request):
    crawl_food('1 apple')
    return HttpResponse(200)
