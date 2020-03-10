import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from .models import Search
# Create your views here.


def home(request):
    return render(request, 'new_search.html')


def new_search(request):
    base_url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw={}'
    search = request.POST.get('search')
    Search.objects.create(search=search)
    final_url = base_url.format(quote_plus(search))

    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')

    final_post = []

    post_listings = soup.find_all('div', {'class': 's-item__wrapper clearfix'})
    for item in post_listings:
        d = dict()

        d['post_title'] = item.find('a', {'class': 's-item__link'}).text
        d['post_url'] = item.find('a').get('href')
        d['post_image'] = item.find('img').get('src')

        if item.find('span',{'class': 's-item__price'}):
            d['post_price'] = item.find('span',{'class':'s-item__price'}).text
        else:
            d['post_price'] = 'Item does not have a price'

        final_post.append(d)

    return render(request, 'new_search.html', {'search': search, 'final_post':final_post})
