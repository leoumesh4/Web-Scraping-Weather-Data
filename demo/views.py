from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup


def get_html_content(location):
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    location = location.replace(" ", "+")
    html_content = session.get(f'https://www.bing.com/search?q=weather+in+{location}').text
    return html_content


def home(request):
    context = None
    if 'location' in request.GET:
        location = request.GET.get('location')
        html_data = get_html_content(location)
        soup = BeautifulSoup(html_data, "html.parser")
        region = soup.find('span', attrs={'class': 'wtr_foreGround'}).text
        print(region)
        daytime = soup.find('div', attrs={'class': 'wtr_dayTime'}).text
        status = soup.find('div', attrs={'class': 'wtr_caption'}).text
        temperature = soup.find('div', attrs={'class': 'wtr_currTemp'}).text
        context = {'region': region, 'daytime': daytime, 'status': status, 'temperature': temperature}

    return render(request, 'demo/index.html', context)
