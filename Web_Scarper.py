import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin


base_url = "https://www.amazon.in"


start_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}


products = []


for page in range(1, 21):
    
    response = requests.get(start_url + "&page=" + str(page), headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")


    items = soup.find_all("div", class_="s-result-item")

    
    for item in items:
        
        product_url = item.find("a", class_="a-link-normal")
        product_url = product_url["href"] if product_url else "N/A"
        product_url = urljoin(base_url, product_url)

       
        product_name = item.find("span", class_="a-size-medium a-color-base a-text-normal")
        product_name = product_name.text if product_name else "N/A"

       
        product_price = item.find("span", class_="a-price-whole")
        product_price = product_price.text if product_price else "N/A"

        product_rating = item.find("span", class_="a-icon-alt")
        product_rating = product_rating.text if product_rating else "N/A"

     
        product_reviews = item.find("span", class_="a-size-base")
        product_reviews = product_reviews.text if product_reviews else "N/A"
        

   
        product_response = requests.get(product_url, headers=headers)
        product_soup = BeautifulSoup(product_response.content, "html.parser")

        description = soup.find("div", id="productDescription")
        if description is not None:
            description = description.text.strip()
        else:
            description = ""


        
        asin_element = product_soup.find("div", id="cerberus-data-metrics")
        if asin_element is not None:
            asin = asin_element["data-asin"]
        else:
            asin = ""

        
        product_description_element = product_soup.find("div", id="feature-bullets")
        if product_description_element is not None:
            product_description = product_description_element.text.strip()
        else:
            product_description = ""
        
        manufacturer_element = product_soup.find("div", id="bylineInfo")
        if manufacturer_element is not None:
            manufacturer = manufacturer_element.text.strip()
        else:
            manufacturer = ""

            
with open("data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["product_url", "product_name", "product_price", "product_rating", "product_reviews", "description", "asin_element", "product_description", "manufacturer"])
    writer.writerows(products)

