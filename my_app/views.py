import requests
from django.shortcuts import render
from requests.compat import urljoin, quote_plus
from bs4 import BeautifulSoup
from . import models
# Create your views here.

BASE_CRAGELIST_URL='https://hyderabad.craigslist.org/search/?query={}'
BASE_IMAGE_URL="https://images.craigslist.org/{}_300x300.jpg"
def home(request):
    return render(request, "base.html")

def new_search(request):
    search=request.POST.get('search')
    models.Search.objects.create(search=search)
    print(search)
    final_url = BASE_CRAGELIST_URL.format(quote_plus(search))
    # final_url=BASE_CRAGELIST_URL.format(quote_plus(search))
    print(final_url)
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_listing = soup.find_all('li', {'class': 'result-row'})
    final_posting = []

    for post in post_listing:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price')
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_url=post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url=BASE_IMAGE_URL.format(post_image_url)
            final_posting.append((post_title, post_url, post_price, post_image_url))

        else:
            post_image_url="https://craigslist.org/images/peace.jpg"


            print(post_image_url)
    stuff_for_frontend = {
        'search': search,
        'final_posting': final_posting,
    }
   # print(stuff_for_frontend)
    return render(request,"my_app/new_search.html",stuff_for_frontend)
