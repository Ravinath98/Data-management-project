import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import csv

df=pd.read_csv('data.csv')
asins = df['asin'].tolist()

# asins=['B01AUI4VVA','B0102TRQYG','B00K328KV6','B000ILG1J0','B005KMDV9A','B006QZ7J8O','B01BVXEN3O','B01DJKOS96','B01E6RJ6WK','B01EV6LJ7G']

product_data=[]
for i in asins:
    ASIN=i
    try:
        url = 'https://www.amazon.com/dp/' + ASIN

        HEADERS = {
            'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
                           'AppleWebKit/537.36 (KHTML, like Gecko)'
                           'Chrome/44.0.2403.157 Safari/537.36'),
            'Accept-Language': 'en-US, en;q=0.5'
        }

        # Send a GET request to the URL
        response = requests.get(url, headers=HEADERS)
        # print(response)
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the title of the product
        title = soup.find('span', {'id': 'productTitle'}).text.strip()
        # print(title)
        # Find the URL of the first image of the product
        img_url = soup.find('img', {'class': 'a-dynamic-image'})['data-a-dynamic-image']
        url_pattern = re.compile(r'https:\/\/.*?\.jpg')

        # Find all URLs in the text string that match the pattern
        urls = re.findall(url_pattern, img_url)
        # Print the title and image URL

        # Define the file name to save the image as
        file_name = 'images' + '/' + ASIN + '.jpg'

        with open(file_name, 'wb') as handle:
            response = requests.get(urls[0], stream=True)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)

    except:
        continue
    product_data.append([i,title])

# Save the product data to a CSV file
with open('product_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['asin', 'title'])
    for data in product_data:
        writer.writerow(data)

print('done.......')