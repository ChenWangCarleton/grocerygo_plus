import socket
import threading
import time
import logging
import traceback
import os
import queue

from grocerygo_plus.grocerygo import database
from grocerygo_plus.grocerygo.web_crawler import utils_walmart

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class server_walmart:
    def __init__(self, max_thread = 10, daily_id='XXXX0001'):
        self.max_thread = max_thread
        self.daily_id = daily_id
        self.current_thread

        self.current_server_task = -1 # -1 is no task, 0 is get&write item links, 1 is get&write item prices, 2 is get&write item detail

        self.url_list = []
        self.id_url_tuple_list = []
        self.to_be_written_to_db = [] # list of tuples to be written to db
        self.tablename_attributelist_dict = {'item_url':['url', 'source_brand', 'category'],
                                             'item':['item_id', 'name', 'brand', 'description', 'ingredient', 'img_src'],
                                             'item_price':['item_id', 'daily_id', 'price']}

        self.category_urls = ['https://www.walmart.ca/en/grocery/fruits-vegetables/N-3799',
                              'https://www.walmart.ca/en/grocery/dairy-eggs/N-3798',
                              'https://www.walmart.ca/en/grocery/meat-seafood/N-3793',
                              'https://www.walmart.ca/en/grocery/pantry-food/N-3794',
                              'https://www.walmart.ca/en/grocery/frozen-food/N-3795',
                              'https://www.walmart.ca/en/grocery/deli-ready-made-meals/N-3792',
                              'https://www.walmart.ca/en/grocery/bakery/N-3796',
                              'https://www.walmart.ca/en/grocery/drinks/N-3791',
                              'https://www.walmart.ca/en/grocery/natural-organic-food/N-3992']

        self.data = database.DatabaseObj("localhost", "readwrite", "readwrite", databasename='grocerygo', write_access=True)


    def write_to_db(self, table_name, attribute_tuple_list):
        """
        This function write attribute tuple list to the table with predifined columns
        :param table_name:
        :param attribute_tuple_list:
        :return: True if succeed, False otherwise
        """
        if table_name not in self.tablename_attributelist_dict:
            logger.error('talbe name does not exist in table dictionary. table name: {}\ndictionary:{}\n{}'.format(table_name, self.tablename_attributelist_dict, traceback.format_exc()))
            return False
        respond = self.data.execute_insert(table_name,
                                           columnnames=self.tablename_attributelist_dict[table_name],
                                           attributes=attribute_tuple_list)
        if not respond:
            logger.error('error when writting into database, terminating the writing process now, '
                         'please try again once the database issue is fixed\n{}'.format(traceback.format_exc()))
            return False

        return True

    def thread_get_item_link(self):
