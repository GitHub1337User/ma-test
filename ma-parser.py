import requests
import json
import sys 
from sign import generate_sign


# URL эндпоинтов
PRODUCTS_URL = 'https://4lapy.ru/api/v2/catalog/product/list/'  # Замените на ваш URL товаров
OFFER_URL = 'https://4lapy.ru/api/product_variant_info/'



headers = {
    'Authorization': 'Basic NGxhcHltb2JpbGU6eEo5dzFRMyhy',
    'Content-Type': 'application/json; charset=utf-8',  
    'Accept': 'application/json; charset=utf-8',  
    'user-agent':'v4.5.6(Android 9, Honor BVL-AN16)',
    'Version-Build': '228',
    'X-Apps-Build': '4.5.6(228)',
    'X-Apps-Os': '9',
    'X-Apps-Screen': '1280x720',
    'X-Apps-Device': 'Honor BVL-AN16',
    'X-Apps-Location': 'lat:null,lon:null',
    'X-Apps-Additionally': '404',
    'Accept-Encoding': 'gzip, deflate, br'
        
}

# city spb 0000103664 / city msk 0000073738
cookies = {
    'selected_city_code':'',
}
params_products = {
    'sort': 'popular',
    'category_id': '1',
    'page': '1',
    'count': '100',
    'token': 'd6aa1a4bd50797c7d69ed3dfc8668b0a',
    'sign': '16e77e2ad9a0aec0d1803423cd2205b2',
}

params_offer = {
    'offerId':'',
    'token': 'd6aa1a4bd50797c7d69ed3dfc8668b0a',
    'sign':'',
}


def fetch_products(city_code):
    try:
        cookies['selected_city_code'] = city_code
    
        response = requests.get(PRODUCTS_URL, params=params_products,headers=headers,cookies=cookies)

        response.raise_for_status()  
        response.encoding = 'utf-8'
        return response.json()  
    
    except requests.exceptions.RequestException as e:

        print(f"Ошибка при получении товаров: {e}")

        sys.exit(1)  


def write_file(city,output):
    with open(f'4lapy-{city}.json', 'w') as json_file:
            json.dump(output, json_file, indent=4)


def output(result,city):
    output = []
    if result:
        for item in result['data']['goods']:
            if item['isAvailable']:
                current_data = {
                        "id":item['id'],
                        "title":item['title'],
                        'url':item['webpage'],
                        'brand':item['brand_name'],
                        'price_per_kg':item['price_per_kg'],
                        'price':item['price']
                }
                output.append(current_data)
                print('Product: '+str(current_data['id'])+' Success')
                for additional in item['packingVariants']:
                    current_data = {
                        "id":additional['id'],
                        "title":additional['title'],
                        'url':additional['webpage'],
                        'brand':item['brand_name'],
                        'price_per_kg':additional['price_per_kg'],
                        'price':additional['price']
                }
                    output.append(current_data)
    print('Count of products:', len(output))
        
    write_file(city,output)
    return output


def get_prices(input,city_code,city):
    output=[]
    try:
        cookies['selected_city_code'] = city_code
        for item in input:
            try:
                params_offer['offerId'] = str(item['id']) 
                params_offer['sign'] = generate_sign(params_offer, params_offer['token'])
                response = requests.get(OFFER_URL, params=params_offer,headers=headers,cookies=cookies)
                response.raise_for_status()  # Проверка на успешный ответ
                # response.encoding = 'utf-8'
                response = response.json()
                for product in response['data']['packingVariants']:
                    if product['id'] == item['id']:
                        item['price'] = product['price']
                        output.append(item)
                        print(f'Succes {product["id"]}')
           
                print(f'Final products with prices: {len(output)}')
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при получении цен товаров: {e} = пропуск записи")
                write_file(city,output)
    except Exception as e:
        print(f"Общая ошибка: {e}")
        # sys.exit(1)  



# msk
get_prices(output(fetch_products('0000073738'),'msk'),'0000073738','msk')
# spb
get_prices(output(fetch_products('0000103664'),'spb'),'0000103664','spb')


