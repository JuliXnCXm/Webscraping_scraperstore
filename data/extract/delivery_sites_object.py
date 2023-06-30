from logging import debug
from common import config
import json


class DeliverySite:
    def __init__(self, delivery_sites_uid,idx):
        self.__config = config()['delivery_sites']['']
        self._data = None
        self._index = int(idx)
        self._delivery_sites_uid = delivery_sites_uid
        self.url_store_res = self.__config['']
        self._readingData()

    def _readingData(self):
        try:
            jsonFile = open('../../backend_scraper/src/data/data{}.json'.format(self._index), 'r')
            self._data = json.load(jsonFile)
            return self._data
        except Exception as e:
            debug(e)

class StorePage(DeliverySite):
    def __init__(self, delivery_sites_uid, idx):
        super().__init__(delivery_sites_uid,idx )
        for i in range(len(self._data)):
            if self._data[i]['cardType'] == '':
                self._index = i

    @property
    def store_info(self):
        info_stores = []
        for info in self._data[self._index]['data']['contents']:
            slug = info['action'].split('%2F')[-1]
            info_stores.append(
                [info, self.url_store_res + slug + '/' + info['id']])

        return info_stores
