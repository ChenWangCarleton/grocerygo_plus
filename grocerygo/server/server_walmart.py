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
    def __init__(self, max_thread=10, daily_id='XXXX0001',max_db_input_record=30):
        self.max_thread = max_thread
        self.daily_id = daily_id
        self.current_thread = 0

        self.current_server_task = -1  # -1 is no task, 0 is get&write item links, 1 is get&write item prices, 2 is get&write item detail
        self.supported_tasks = {0:"get&write item links", 1:"get&write item prices", 2:"get&write item detail"}
        self.retry_statue = 0 # 0 for not selected, -1/<0 for not retry/ discard what's in retry list and log the failed list, 1/>0 for retry the failed list
        self.max_db_input_record = max_db_input_record
        self.quit_signal = False
        self.url_list = []
        self.failed_list = [] # failed url list or id_url_tuple list depends on the current task
        self.id_url_tuple_list = []
        self.to_be_written_to_db = []  # list of tuples to be written to db
        self.tablename_attributelist_dict = {'item_url': ['url', 'source_brand', 'category'],
                                             'item': ['item_id', 'name', 'brand', 'description', 'ingredient',
                                                      'img_src'],
                                             'item_price': ['item_id', 'daily_id', 'price']}

        self.category_urls = ['https://www.walmart.ca/en/grocery/fruits-vegetables/N-3799',
                              'https://www.walmart.ca/en/grocery/dairy-eggs/N-3798',
                              'https://www.walmart.ca/en/grocery/meat-seafood/N-3793',
                              'https://www.walmart.ca/en/grocery/pantry-food/N-3794',
                              'https://www.walmart.ca/en/grocery/frozen-food/N-3795',
                              'https://www.walmart.ca/en/grocery/deli-ready-made-meals/N-3792',
                              'https://www.walmart.ca/en/grocery/bakery/N-3796',
                              'https://www.walmart.ca/en/grocery/drinks/N-3791',
                              ]
        #self.category_urls = ['https://www.walmart.ca/en/grocery/natural-organic-food/N-3992']
        #self.category_urls = ['https://www.walmart.ca/en/grocery/fruits-vegetables/N-3799'] # for testing

        self.data = database.DatabaseObj("localhost", "readwrite", "readwrite", databasename='grocerygo',
                                         write_access=True)

        self.thread_lock = threading.Lock()
        threading.Thread(target=self.main_thread).start()
        logger.debug('server walmart started')
    def get_failed_list(self):
        return self.failed_list
    def set_quit_signal(self, status=True):
        self.quit_signal = status
    def set_retry(self, status):
        self.retry_statue = status

    def set_task(self, task_num):
        if self.current_server_task != -1:
            logger.error('server is handling task {}:{}, please try again later'.format(self.current_server_task, self.supported_tasks[self.current_server_task]))
            return False
        if task_num not in self.supported_tasks:
            logger.error('server does not support task number:{}, all supported tasks:\n{}'.format(task_num, self.supported_tasks))
            return False
        self.current_server_task = task_num

        logger.debug('clearing list before server start')
        self.url_list = []
        self.failed_list = [] # failed url list or id_url_tuple list depends on the current task
        self.id_url_tuple_list = []
        self.to_be_written_to_db = []  # list of tuples to be written to db

        #initializations
        if task_num == 0:
            self.url_list.extend(self.category_urls)
        elif task_num == 1:
            self.url_list.extend(self.category_urls)
        elif task_num == 2:
            if not self.get_id_url():
                logger.error(
                    'something wrong when trying to get id and url from database, please check again, ending task now')
                self.current_server_task = -1
        self.current_server_task = task_num
        logger.debug('server task sets to {}:{}'.format(task_num, self.supported_tasks[task_num]))
        return True

    #{0:"get&write item links", 1:"get&write item prices", 2:"get&write item detail"}
    def main_thread(self):
        while True:
            if self.quit_signal:
                break
            if self.current_server_task == 0:
                while self.current_thread < self.max_thread and len(self.url_list) > 0:
                    threading.Thread(target=self.thread_get_item_link, args=(self.url_list.pop(0),)).start()
                if self.current_thread == 0 and len(self.url_list) == 0:
                    while len(self.to_be_written_to_db) > 0:
                        index = min(self.max_db_input_record, len(self.to_be_written_to_db))
                        temp_records = self.to_be_written_to_db[:index]
                        self.to_be_written_to_db = self.to_be_written_to_db[index:]

                        respond = self.write_to_db('item_url', temp_records)
                        if not respond:
                            logger.debug('error when writing to db, put the temp records back to the list\n{}'.format(self.get_status()))
                            self.to_be_written_to_db.extend(temp_records)
                    if self.retry_statue > 0:
                        logger.debug('retrying {} records in failed list\n{}'.format(len(self.failed_list), self.failed_list))
                        self.url_list.extend(self.failed_list)
                        self.failed_list = []
                        self.retry_statue = 0
                    elif self.retry_statue < 0:
                        logger.debug('task {}:{} finished successfully'.format(self.current_server_task, self.supported_tasks[self.current_server_task]))
                        self.current_server_task = -1
            if self.current_server_task == 1:
                while self.current_thread < self.max_thread and len(self.url_list) > 0:
                    threading.Thread(target=self.thread_get_item_price, args=(self.url_list.pop(0),)).start()
                if self.current_thread == 0 and len(self.url_list) == 0:
                    while len(self.to_be_written_to_db) > 0:
                        index = min(self.max_db_input_record, len(self.to_be_written_to_db))
                        temp_records = self.to_be_written_to_db[:index]
                        self.to_be_written_to_db = self.to_be_written_to_db[index:]

                        respond = self.write_to_db('item_price', temp_records)
                        if not respond:
                            logger.debug('error when writing to db, put the temp records back to the list\n{}'.format(self.get_status()))
                            self.to_be_written_to_db.extend(temp_records)
                    if self.retry_statue > 0:
                        logger.debug('retrying {} records in failed list\n{}'.format(len(self.failed_list), self.failed_list))
                        self.url_list.extend(self.failed_list)
                        self.failed_list = []
                        self.retry_statue = 0
                    elif self.retry_statue < 0:
                        logger.debug('task {}:{} finished successfully'.format(self.current_server_task, self.supported_tasks[self.current_server_task]))
                        self.current_server_task = -1
            if self.current_server_task == 2:
                while self.current_thread < self.max_thread and len(self.id_url_tuple_list) > 0:
                    threading.Thread(target=self.thread_get_item_detail, args=(self.id_url_tuple_list.pop(0),)).start()

                if len(self.to_be_written_to_db) > self.max_db_input_record:
                    with self.thread_lock:
                        temp_records = self.to_be_written_to_db[:self.max_db_input_record]
                        self.to_be_written_to_db = self.to_be_written_to_db[self.max_db_input_record:]
                    respond = self.write_to_db('item',temp_records)
                    if not respond:
                        logger.debug('error when writing to db, put the temp records back to the list\n{}'.format(self.get_status()))
                        self.to_be_written_to_db.extend(temp_records)

                if self.current_thread == 0 and len(self.id_url_tuple_list) == 0:
                    while len(self.to_be_written_to_db) > 0:
                        index = min(self.max_db_input_record, len(self.to_be_written_to_db))
                        temp_records = self.to_be_written_to_db[:index]
                        self.to_be_written_to_db = self.to_be_written_to_db[index:]

                        respond = self.write_to_db('item', temp_records)
                        if not respond:
                            logger.debug('error when writing to db, put the temp records back to the list\n{}'.format(self.get_status()))
                            self.to_be_written_to_db.extend(temp_records)
                    if self.retry_statue > 0:
                        logger.debug('retrying {} records in failed list\n{}'.format(len(self.failed_list), self.failed_list))
                        self.id_url_tuple_list.extend(self.failed_list)
                        self.failed_list = []
                        self.retry_statue = 0
                    elif self.retry_statue < 0:
                        logger.debug('task {}:{} finished successfully'.format(self.current_server_task, self.supported_tasks[self.current_server_task]))
                        self.current_server_task = -1

    def get_status(self):
        to_return = 'current_thread: {}, current_server_task: {}, ' \
                    'len of url_list: {}, len of failed_list: {}, ' \
                    'len of id_url_tuple_list: {}, len of to_be_written_to_db: {}'.format(self.current_thread, self.current_server_task, len(self.url_list),
                                                                                          len(self.failed_list), len(self.id_url_tuple_list), len(self.to_be_written_to_db))
        return to_return
    def write_to_db(self, table_name, attribute_tuple_list):
        """
        This function write attribute tuple list to the table with predifined columns
        :param table_name:
        :param attribute_tuple_list:
        :return: True if succeed, False otherwise
        """
        if table_name not in self.tablename_attributelist_dict:
            logger.error(
                'talbe name does not exist in table dictionary. table name: {}\ndictionary:{}\n{}'.format(
                    table_name, self.tablename_attributelist_dict, traceback.format_exc()))
            return False
        respond = self.data.execute_insert(table_name,
                                           columnnames=self.tablename_attributelist_dict[table_name],
                                           attributes=attribute_tuple_list)
        if not respond:
            logger.error('error when writting into database, terminating the writing process now, '
                         'please try again once the database issue is fixed\n{}'.format(traceback.format_exc()))
            return False

        return True


    def thread_get_item_link(self, url, brand='Walmart'):
        """
        a function used in thread to get the item links in a category url
        If there are more sub categories from the url, get urls of sub categories and store them into url list
        If there no more sub categories from the url, add all the item links and categories from all pages in this category to add to db list
        :param url: a url of one of the category in walmart, it either has more sub categories under it or not
        :return:
        True when everything works fine
        False when error happens
        """
        with self.thread_lock:
            self.current_thread +=1
        try:
            result = utils_walmart.has_subcategory(url, disableimage=True)
            if result is None:
                logger.error('unexpectd error happened when checking if url:{} has more subcategory'.format(url))
                self.failed_list.append(url)
                return False
            if result:
                for url in result:
                    self.url_list.append(url)
                logger.debug('sub categories link found and added to url list for url:{}'.format(url))
                return True

            result = utils_walmart.get_all_category_link(url, disableimage=True)
            if result is None:
                logger.error('unexpectd error happened when getting item links from url:{} '.format(url))
                self.failed_list.append(url)
                return False

            for record in result:
                url = record[0]
                category_list = record[1]
                attribute_tuple_list = (url, brand, category_list[1])
                self.to_be_written_to_db.append(attribute_tuple_list)
            logger.debug('total {} items link added to to_be_written_to_db list from url {}')
            return True
        finally:
            with self.thread_lock:
                self.current_thread -= 1


    def thread_get_item_price(self, url, brand='Walmart'):
        """
        a function used in thread to get the item prices in a category url
        If there are more sub categories from the url, get urls of sub categories and store them into url list
        If there no more sub categories from the url, add all the item links and categories from all pages in this category to add to db list
        :param url: a url of one of the category in walmart, it either has more sub categories under it or not
        :return:
        True when everything works fine
        False when error happens
        """
        with self.thread_lock:
            self.current_thread +=1
        try:
            result = utils_walmart.has_subcategory(url, disableimage=True)
            if result is None:
                logger.error('unexpectd error happened when checking if url:{} has more subcategory'.format(url))
                self.failed_list.append(url)
                return False
            if result:
                for url in result:
                    self.url_list.append(url)
                logger.debug('sub categories link found and added to url list for url:{}'.format(url))
                return True

            result = utils_walmart.get_all_category_price(url, disableimage=True)
            if result is None:
                logger.error('unexpectd error happened when getting item links from url:{} '.format(url))
                self.failed_list.append(url)
                return False

            for record in result:
                item_url = record[0]
                category_list = record[1]
                price = record[2]

                # get item id
                item_id = self.data.select_from_table('item_url', "url='{}'".format(item_url), 'item_id')
                if len(item_id) == 0:
                    # insert it into item_url table first if the url doesn't exist in it

                    attribute_tuple_list = [(item_url, brand, category_list[1])]
                    respond = self.data.execute_insert('item_url',
                                                       columnnames=self.tablename_attributelist_dict['item_url'],
                                                       attributes=attribute_tuple_list)
                    if not respond:
                        logger.error('error happened when inserting item into item_url table url:{} '.format(item_url))
                        self.failed_list.append(url)
                        return False
                    item_id = self.data.select_from_table('item_url', "url='{}'".format(item_url), 'item_id')
                if len(item_id) != 1:
                    logger.error('error when getting id for item {}, terminating the writing process now, '
                                 'please try again once the database issue is fixed'.format(item_url))
                    self.failed_list.append(url)
                    return False
                item_id = item_id[0][0]

                attribute_tuple_list = (item_id, self.daily_id, price)
                self.to_be_written_to_db.append(attribute_tuple_list)
            logger.debug('total {} items link added to to_be_written_to_db list from url {}')
            return True
        finally:
            with self.thread_lock:
                self.current_thread -= 1

    def get_id_url(self, category='', brand='Walmart'):
        # get list of (item_id, url) tuple from database into
        try:
            if category:
                result = self.data.select_from_table('item_url',
                                                     "source_brand='{}' and category='{}'".format(brand, category),
                                                     'item_id', 'url')
            else:
                result = self.data.select_from_table('item_url',
                                                     "source_brand='{}'".format(brand, category),
                                                     'item_id', 'url')
            self.id_url_tuple_list.extend(result)
            return True
        except:
            logger.error('unexpected error when start_getting_item_detail')
            return False


    def thread_get_item_detail(self, id_url_tuple):

        with self.thread_lock:
            self.current_thread +=1
        try:
            result = utils_walmart.get_item_detail(id_url_tuple, disableimage=True)
            if result is None:
                logger.error('error when getting item detail with value: {}'.format(id_url_tuple))
                self.failed_list.append(id_url_tuple)
                return False

            self.to_be_written_to_db.append(result)
            return True
        finally:
            with self.thread_lock:
                self.current_thread -= 1