import requests
from bs4 import BeautifulSoup
from product_classify import classifyProducts

#to import upper folder `cvs_server`
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
#django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cvs_server.settings")
import django
django.setup()

from cvs_rest.models import Product
from django.core.exceptions import ObjectDoesNotExist
#PB Product PBG
#CU Product CUG

pbList = []
productList = []

def parsePBList(x):
    if x.find(class_='prodName'):
        name = x.find(class_='prodName').find('a').get_text()
        category = classifyProducts(name)
        return {
            'large_category': category['large_category'],
            'small_category': category['small_category'], 
            'name': x.find(class_='prodName').find('a').get_text(), 
            'price': int(x.find(class_='prodPrice').find('span').get_text().replace('\n','').replace(',','')), 
            'img': x.find('img')['src'], 
        }

def parseProductList(x):
    if x.find(class_='prodName'):
        name = x.find(class_='prodName').find('span').get_text()
        category = classifyProducts(name)
        return {
            'large_category': category['large_category'],
            'small_category': category['small_category'],
            'name': name, 
            'price': int(x.find(class_='prodPrice').find('span').get_text().replace('\n','').replace(',','')), 
            'img': x.find('img')['src']
        }
    

def pbCrawler(productType):
    url = 'http://cu.bgfretail.com/product/pbAjax.do'
    pageIndex = 1
    while True:
        req = requests.post(url, data={'pageIndex': pageIndex, 'gdIdx': 0, 'searchgubun': productType})
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        htmlList = soup.find_all('li')
        for productHTML in htmlList:
            pbList.append(parsePBList(productHTML))
        if soup.find(id='nonelayer'):
            break
        pageIndex = pageIndex + 1

def productCrawler(productCode):
    url = 'http://cu.bgfretail.com/product/productAjax.do'
    pageIndex = 1
    while True:
        req = requests.post(url, data={'pageIndex': pageIndex, 'gdIdx': 0, 'searchMainCategory': productCode, 'codeParent': productCode, 'searchCondition': 'setA'})
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        htmlList = soup.find_all('li')
        for productHTML in htmlList:
            productList.append(parseProductList(productHTML))
        if soup.find(class_='prodListWrap').find('div'):
            if soup.find(class_='prodListWrap').find('div').get_text() == '조회된 상품이 없습니다.':
                break
        pageIndex = pageIndex + 1

        
productCrawler(10) #간편식사      
productCrawler(20) #즉석조리
productCrawler(30) #과자류
productCrawler(40) #아이스크림
productCrawler(50) #식품
productCrawler(60) #음료
productCrawler(70) #샏활용품
productList = [x for x in productList if x is not None]

pbCrawler('PBG')
pbCrawler('CUG')
pbList = [x for x in pbList if x is not None]

#print(pbList)

# code for registering product to DB
if __name__ == '__main__':
    print('CU crawler START')
    product_data_dict = pbList
    for p in product_data_dict:
        try:
            Product.objects.get(name=p['name'])
        except ObjectDoesNotExist:
            print('\t{} is registed in DB'.format(p['name']))
            Product(
                name=p['name'], 
                price=p['price'], 
                image=p['img'], 
                manufacturer='CU',
                large_category=p['large_category'],
                small_category=p['small_category'],
                PB=True,
            ).save()
    
    print('not PB crawler START')
    product_data_dict = productList
    for p in product_data_dict:
        try:
            Product.objects.get(name=p['name'])
        except ObjectDoesNotExist:
            print('\t{} is registed in DB'.format(p['name']))
            Product(
                name=p['name'], 
                price=p['price'], 
                image=p['img'], 
                manufacturer='Other',
                large_category=p['large_category'],
                small_category=p['small_category'],
                PB=False,
            ).save()        
