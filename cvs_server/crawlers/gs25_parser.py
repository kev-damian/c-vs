import requests
import json
from bs4 import BeautifulSoup

#productSrvFoodCK description
#FreshFoodKey - fresh food
#DifferentServiceKey - different product


#searchProduct description
#in Fresh Food Key
#productLunch - search dosirak
#productRice - search gimbab & jumukbab
#productBurger - search burger
#productSnack - search fastfood , in Korean, gan pyeon sik
#in Different Service Key
#productDrink - search coffee & drink
#productMilk - search milk product
#productCookie - search snack
#productRamen - search ramen & processed food
#productGoods - search living items

product_list = []
def getPBProducts():
    #setting url
    pageNum = 1
    pageSize = 16
    searchSrvFoodCK = 'FreshFoodKey'
    searchSort = 'searchALLSort'
    searchProduct = 'productALL'
    url = "http://gs25.gsretail.com/products/youus-freshfoodDetail-search?pageNum={}&pageSize={}&searchSrvFoodCK={}&searchSort={}&searchProduct={}".format(pageNum, pageSize, searchSrvFoodCK, searchSort, searchProduct)
    # send request
    req = requests.get(url)
    header = req.headers
    status = req.status_code
    is_ok = req.ok
    if (is_ok == False) :
        print(status)
        return
    #get json data    
    json_raw = req.text
    json_data = json.loads(json_raw)
    json_data = json.loads(json_data)
    #total of products
    total_count = json_data['SubPageListPagination']['totalNumberOfResults']
    #total of pages
    total_page = json_data['SubPageListPagination']['numberOfPages']
    #append items to product_list
    for page in range(1,total_page): 
        url = "http://gs25.gsretail.com/products/youus-freshfoodDetail-search?pageNum={}&pageSize={}&searchSrvFoodCK={}&searchSort={}&searchProduct={}".format(page, pageSize, searchSrvFoodCK, searchSort, searchProduct)
        req = requests.get(url)
        is_ok = req.ok
        if (is_ok == False) :
            print(req.text)
            return    
        json_raw = req.text
        json_data = json.loads(json_raw)
        json_data = json.loads(json_data) 
        products = json_data["SubPageListData"]
        for product in products:
            product_list.append({
                'name':product['goodsNm'],
                'img':product['attFileNm'],
                'price':product['price']
            })
            
        
getPBProducts()
print(product_list)
