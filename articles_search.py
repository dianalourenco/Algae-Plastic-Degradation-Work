import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import random
import datetime
import re

# Keyword categories
ALGAE_KEYWORDS = [
    'algae', 'microalgae', 'cyanobacteria', 'diatoms']
PLASTIC_KEYWORDS = [
    'plastic', 'microplastic', 'polymeric materials']
DEGRADATION_KEYWORDS = [
    'degradation', 'biodegradation', 'degrade']


queries = []
def generate_queries():
    '''
    Generate search query combinations.
    '''
    queries = []
    for algae in ALGAE_KEYWORDS:
        for plastic in PLASTIC_KEYWORDS:
            for degradation in DEGRADATION_KEYWORDS:
                queries.append(f'{algae} {plastic} {degradation}')
    return queries

def find_articles(keyword):
    '''
    Search for articles on Google Scholar.
    '''

    headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.361681261652"
        }
    url = f"https://scholar.google.com/scholar?q={keyword.replace(' ', '+')}"
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    time.sleep(random.uniform(15,30))

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []

    for result in soup.select('.gs_r'):
        title_elem = result.select('.gs_rt')
        link_elem = result.select('.gs_rt a')

        # Only add articles that have title and link
        if title_elem and link_elem:
            title = title_elem[0].text.strip() 
            link = link_elem[0]['href'].strip() 
                
            articles.append({
                'title': title,
                'url': link
                })

    print(f'\nFound {len(articles)} articles for query: {keyword}')

    return articles


def set_url(filename='articles.txt'):
    '''
    Extract URLs from the existing file
    '''
    try:
        url_pattern = r"Link: (https?:\/\/[^\s]+)"

        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
            urls = set(re.findall(url_pattern, text))
            return urls

    except FileNotFoundError:
        print('File not Found')
        return set()



def save_articles(articles, filename="articles.txt"):
    '''
    Save articles to a text file.
    '''    
    current_time = datetime.datetime.now()

    with open(filename, 'a', encoding='utf-8') as f:
        f.write('\n####################\n')
        f.write(f'Articles searched on: {current_time}\n')
        f.write('####################\n\n')

        # Add articles
        for i, (url,article) in enumerate(articles.items()):
            f.write(f"{i+1}. Title: {article['title']}\n")
            f.write(f"   Link: {article['url']}\n\n")

def main():
    # Retrieve existing URLs
    existing_urls = set_url()

    search_queries = generate_queries()
    all_articles = []
        
    for keyword in tqdm(search_queries, desc="Searching articles"):
        articles = find_articles(keyword)
        all_articles.extend(articles)    

    # Remove duplicates based on URL
    unique_articles = {}
    for article in all_articles:
        if article['url'] not in existing_urls:
            unique_articles[article['url']] = article
    
    if unique_articles:
        save_articles(unique_articles)
        print(f'\n{len(unique_articles)} new articles added to the articles.txt file.')
    else:
        print(f'\nNo new articles found.')

if __name__ == "__main__":
    main()