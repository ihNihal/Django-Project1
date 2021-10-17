from typing import Text
import requests
from django.shortcuts import render
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import models


BASE_CRAIGLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'results-row'})
    post_title = post_listings[0].find(class_='results-title').text
    post_url = post_listings[0].find('a').get('href')
    post_price = post_listings[0].find(class_='result-price').text

    print(post_title)
    print(post_url)
    print(post_price)

    stuff_for_frontend = {
        'search': search,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)

# Create your views here.
