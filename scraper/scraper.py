import os
import json
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['scrapedData']
collection = db['data']

def scrape_with_requests():
    response = requests.get('https://example.com')
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    for item in soup.select('.item'):
        results.append({
            'title': item.select_one('h2').text,
            'link': item.select_one('a')['href'],
            'description': item.select_one('p').text
        })
    
    return results

def save_to_database(data):
    collection.insert_many(data)
    print('Data saved to the database!')

def main():
    scraped_data = scrape_with_requests()
    save_to_database(scraped_data)
    with open('formatted_data.json', 'w') as f:
        json.dump(scraped_data, f, indent=2)
    print('Data saved!')

if __name__ == '__main__':
    main()
