from this import d
from yaml import parse
from common import config
import delivery_sites_object as deliverys
from urllib3.exceptions import MaxRetryError
from requests.exceptions import HTTPError
import requests
from bs4 import BeautifulSoup
import re
import argparse
import logging
import os
import pandas as pd
import datetime
import json
from os import write
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
is_well_formed_link = re.compile(r'^https?://.+/.+$')
other = re.compile(r'^https?://.+$')
is_root_path = re.compile(r'^/.+$')


def delivery_scraper(delivery_sites_uid, idx):
    host = config()['delivery_sites']['store']['city']
    logging.info('Beginning scraper for {}'.format(host))
    store_page = deliverys.StorePage(delivery_sites_uid, idx)
    stores = []
    store_info = []
    for info in store_page.store_info:
        link = info[1]
        store = _fetch_store(delivery_sites_uid, _builder_link(link, host))
        if store != None:
            logging.info('Store {} found and fetched'.format(info[1]))
            stores.append(store)
            store_info.append(info[0])
        else:
            logging.info('Store {} not available'.format(link))
    _save_store(stores, store_info ,delivery_sites_uid, idx)

def _save_store(stores, store_info, delivery_sites_uid, idx):

    objStore = {
        'name': [],
        'details': [],
        'categories': [],
        'price': [],
        'store_name': [],
        }
    for aux in range(len(stores)):
        menu_aux = stores[aux]
        categories = [x['name'] for x in menu_aux ]
        for i in range(len(categories)):
            number_products = len(menu_aux[i]['itens'])
            for j in range(number_products):
                objStore['categories'].append(menu_aux[i]['name'])
                objStore['name'].append( menu_aux[i]['itens'][j]['description'])
                try:
                    objStore['details'].append(menu_aux[i]['itens'][j]['details'])
                except KeyError:
                    objStore['details'].append('whitout info')
                objStore['price'].append(menu_aux[i]['items'][j]['price'])
                objStore['store_name'].append(store_info[aux]['sotre_name'])

    df_store = pd.DataFrame(objStore)

    df_store.to_csv('{}{}_'.format(delivery_sites_uid,idx), sep=',', index=False , encoding='utf-8')

def _fetch_store(homepage_url , link):
    logging.info('Beginning fetching store {}'.format(link))
    try:
        response = requests.get(link)
        response.raise_for_status()
        restaurant = BeautifulSoup(response.text, 'lxml').find('script', attrs={'id': '__NEXT_DATA__'}).get_text()
        res_data = json.loads(restaurant)
        data_store = res_data['props']['initialState']['store']['']
        data_store.update()
        if data_store == []:
            return None
        else:
            return data_store
    except (HTTPError, MaxRetryError) as e:
        logging.error('Error while trying to fetch store: {}'.format(e))
        return None

def _builder_link(link, host):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return '{}{}'.format(host, link)
    elif other.match(link):
        return '{}/{}'.format(host, link)
    else:
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    delivery_sites_choices = list(config()['delivery_sites'].keys())
    index_choices = [str(x) for x in range(0,1)]
    parser.add_argument('delivery_site', help='The delivery site uid, must be one of: {}'.format(delivery_sites_choices), type=str, choices=delivery_sites_choices)
    parser.add_argument('index', help='index of file: data.json', type=str, choices=index_choices)
    args = parser.parse_args()
    delivery_scraper(args.delivery_site , args.index)
