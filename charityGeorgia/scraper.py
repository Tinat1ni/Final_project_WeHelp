import requests
from bs4 import BeautifulSoup
from .models import Charity
from django.core.cache import cache


def scrape_and_cache_data():
    cached_data=cache.get('charity_data')
    if cached_data:
        return cached_data

    url = 'https://catharsis.ge/index.php?m=52'
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    name_element = soup.select_one('.logo-title span')
    name = name_element.text.strip() if name_element else 'unknown'

    paragraphs = soup.find_all('p', class_='paragraph')
    scraped_text = ' '.join([p.text for p in paragraphs])

    charity = Charity.objects.create(
        name=name,
        scraped_text = scraped_text,
        website=url
    )

    cache.set('charity_data',{
        'name': name,
        'scraped_text': scraped_text,
        'website': url
    }, timeout=60 * 60 * 24 * 90)

    return {
        'name': name,
        'scraped_text': scraped_text,
        'website': url
    }
