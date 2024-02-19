
from bs4 import BeautifulSoup
import requests
import django
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ecommerce.settings')
django.setup()


productList = []
currentPage = 1
maxPage = 10

while currentPage <= maxPage:
    url = f"https://www.jumia.com.ng/mlp-official-stores/?page={currentPage}#catalog-listing"
    res = requests.get(url)

    if res.status_code == 200:
        HTML_content = res.text
        pot = BeautifulSoup(HTML_content, "lxml")
        articles = pot.css.select(".prd")

        for article in articles:
            productList.append({'id': len(productList) + 1,
                                'name': article.css.select(".name")[0],
                                'image': article.css.select(".img")[0]['data-src'],
                                'brand': article.css.select(".prd > a")[0]['data-brand'],
                                'category': article.css.select(".prd > a")[0]['data-category'].split("/")[0],
                                'price': article.css.select(".prd > a")[0]['data-price'],
                                'rating': {'rate': article.css.select(".prd > a")[0]['data-dimension27'],
                                           'count': article.css.select(".prd > a")[0]['data-dimension26']}
                                })

        currentPage += 1
    else:
        print(f"Failed to get requests {currentPage}!!!")

categories = []
catRes = requests.get("https://www.jumia.com.ng/mlp-official-stores/")
smallPot = BeautifulSoup(catRes.text, 'lxml')

meat = smallPot.css.select("article .-db")
for link in meat:
    if link['data-eventaction'] == "category":
        categories.append(link.text)

from product.models import Product, Category
def populate():
    # product = Product()
    for category in categories:
        catg = Category.objects.get_or_create(title=category)[0]
        catg.save()

        for prod in productList:
            if prod['category'] == category:
                prd = Product.objects.get_or_create(
                    # slug=prod['id'],
                    name=prod['name'],
                    image=prod['image'],
                    brand=prod['brand'],
                    price=prod['price'],
                    category=catg)[0]
                prd.save()


if __name__ == '__main__':
    print('populating')
    populate()
    print("completed")
else:
    print("failed to run script")
