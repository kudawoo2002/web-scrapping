import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from .models import Search
# Create your views here.


def home(request):
    return render(request, 'new_search.html')


def new_search(request):
    base_url = 'https://losangeles.craigslist.org/search/sss?query={}'
    search = request.POST.get('search')
    Search.objects.create(search=search)
    final_url = base_url.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_titles = soup.find_all('a', {'class':'result-title'}).text
    print(post_titles.text)
    return render(request, 'new_search.html', {'search':search})



