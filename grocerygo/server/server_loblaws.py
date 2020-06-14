import socket
import threading
import time
import logging
import traceback
import os
import queue

from grocerygo_plus.grocerygo.database import *
from grocerygo_plus.grocerygo.web_crawler import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class Server_Loblaws():
    def __init__(self,max_thread=10):
        self.max_running_thread = max_thread

        self.get_link_loblaws_tuple_queue = queue.Queue()
        """ a queue contains 2-element tuple to be used for getting itempages' link & getting item prices
         example of an element in the queue: (url, [categoryA, categoryB])"""
        self.current_running_thread = 0
        self.current_running_thread_lock = threading.Lock()
        # https://stackoverflow.com/questions/35088139/how-to-make-a-thread-safe-global-counter-in-python
        self.loblaws_initial_page = 'https://www.loblaws.ca/Food/Ready-Made-Meals/c/LSL001002000000'#'https://www.loblaws.ca/Food/c/LSL001000000000?navid=flyout-L2-Food'

        self.data = DatabaseObj("localhost", "readwrite", "readwrite", databasename='grocerygo', write_access=True)

        # These two booleans are used to show if the server is getting link or getting price. They are for restricting server from starting new similiar tasks when there are current task running
        self.getting_links = False
        self.getting_price = False


        self.writting_links_to_db = False
        self.writting_prices_to_db = False

        self.quit_server = False
        self.get_link_result_list = []
        self.get_link_failed_list = []

        self.get_price_result_list = []
        self.get_price_failed_list = []
        self.category_list = []

        self.daily_id = 'XXXX0001'

        self.failed_get_item_detail_tuple_list = []
        self.id_url_tuple_list = []
        self.item_detail_result_tuple_list = []
        self.getting_item_detail = False
        self.get_item_detail_thread_count = 0
        self.item_detail_thread_lock = threading.Lock()
        self.item_detail_max_write_length=20

        self.monitor = threading.Thread(target=self.monitor_thread)
        self.monitor.start()

    def get_category_list(self):
        result = self.data.select_from_table('item_url', "source_brand='Loblaws'",'distinct category')
        for element in result:
            self.category_list.append(element[0])
        #print(self.category_set)

    def retry_failed_get_item_detail(self):
        if not self.getting_item_detail and len(self.failed_get_item_detail_tuple_list) > 0:
            self.id_url_tuple_list = self.failed_get_item_detail_tuple_list.copy()
            self.failed_get_item_detail_tuple_list = []
            self.getting_item_detail = True
            logger.debug('retrying getting failed get_item_detail, total {} id_url tuple to retry'.format(len(self.id_url_tuple_list)))
            return True
        else:
            return False

    def start_getting_item_detail(self,category='', brand='Loblaws'):
        # get list of (item_id, url) tuple from database
        try:
            if category:
                result = self.data.select_from_table('item_url', "source_brand='{}' and category='{}'".format(brand, category), 'item_id', 'url')
            else:
                result = self.data.select_from_table('item_url',
                                                     "source_brand='{}'".format(brand, category),
                                                     'item_id', 'url')
            self.id_url_tuple_list.extend(result)
            self.getting_item_detail = True
            return True
        except:
            logger.error('unexpected error when start_getting_item_detail')
            return False
    def get_id_url_tuple_list(self):
        return self.id_url_tuple_list
    def get_failed_item_detail_tuple_list(self):
        return self.failed_get_item_detail_tuple_list
    def get_item_detail_thread(self, id_url_tuple):
        with self.item_detail_thread_lock:
            self.get_item_detail_thread_count +=1
        try:
            result = get_item_detail(id_url_tuple,headless=True, disableimage=True)
            if not result:
                logger.error('error when geting item detail with value:{}'.format(id_url_tuple))
                self.failed_get_item_detail_tuple_list.append(id_url_tuple)
            elif result == 'unavailable':
                logger.error('page unavailable when geting item detail with value:{}'.format(id_url_tuple))
                self.failed_get_item_detail_tuple_list.append(id_url_tuple)
            else:
                self.item_detail_result_tuple_list.append(result)
        except:
            self.failed_get_item_detail_tuple_list.append(id_url_tuple)
            logger.error('unexpected error in get_item_detail_thread')
        finally:
            with self.item_detail_thread_lock:
                self.get_item_detail_thread_count -=1




    def write_item_to_db(self, item_tuple_list):
        """
        :param item_tuple:  a 6-element tuple (item_id, name, brand, description, ingredient, imgsrc)
        :return:
        """
        respond = self.data.execute_insert('item',
                                           columnnames=['item_id', 'name', 'brand', 'description', 'ingredient', 'img_src'],
                                           attributes=item_tuple_list)

        if not respond:
            logger.error('error when write_item_to_db, terminating the writing process now, '
                         'please try again once the database issue is fixed')
            return False
        return True
    def write_link_to_db(self, brand='Loblaws'):
        while len(self.get_link_result_list) > 0:

            current_result = self.get_link_result_list[0]  # will not remove from list untill it is written into db
            category = current_result[1][1]
            urls = current_result[0]

            attribute_tuple_list = []
            for url in urls:
                attribute_tuple_list.append((url, brand, category))

            respond = self.data.execute_insert('item_url',
                                               columnnames=['url', 'source_brand', 'category'],
                                               attributes=attribute_tuple_list)
            if not respond:
                logger.error('error when writting into database, terminating the writing process now, '
                             'please try again once the database issue is fixed')
                self.writting_links_to_db = False
                return False
            self.get_link_result_list.pop(0)
        self.writting_links_to_db = False
        return True

    def force_reset(self):
        logger.info('force reseting Server_Loblaws instance')
        if self.getting_links or self.getting_price:
            self.quit_server = True

            while self.current_running_thread != 0:
                logger.info('waiting for all running thread to finish')
                time.sleep(3)

        logger.info('force reseting Server_Loblaws instance in 3 sec')
        time.sleep(3)
        self.__init__()
        return True


    def __del__(self):
        logger.debug('Deleting Server_Loblaws instance')
        self.get_server_status()

    def start_writting_links(self, iswritting=True):
        if self.getting_links or self.getting_price:
            logger.info('Server is getting itempages links, please check back latter')
            return False
        elif len(self.get_link_result_list) == 0:
            logger.info('No link to be wrote into database')
            return False
        elif self.writting_links_to_db or self.writting_prices_to_db:
            logger.info('Server is writting links into database, please check back latter')
            return False
        self.writting_links_to_db = iswritting
        threading.Thread(target=self.write_link_to_db).start()
        return True
    def start_writting_price(self, iswritting=True):
        if self.getting_links or self.getting_price:
            logger.info('Server is getting itempages links, please check back latter')
            return False
        elif len(self.get_price_result_list) == 0:
            logger.info('No price to be wrote into database')
            return False
        elif self.writting_links_to_db or self.writting_prices_to_db:
            logger.info('Server is writting links into database, please check back latter')
            return False
        self.writting_prices_to_db = iswritting
        threading.Thread(target=self.write_price_to_db).start()
        return True
    def send_quit(self, isquiting=True):
        if isinstance(isquiting, bool):
            self.quit_server = isquiting
            logger.info('setting quit signal to {}'.format(isquiting))
            return True
        else:
            logger.info('server quitting signal is not boolean: {}'.format(isquiting))
            return False


    def return_get_link_result_list(self):
        return self.get_link_result_list


    def return_get_link_failed_list(self):
        return self.get_link_failed_list

    def get_server_status(self):
        total_item_link = 0
        for urls in self.get_link_result_list:
            total_item_link += len(urls[0])
        result_str = 'server is getting itempages url from loblaws: {}\n' \
                     'current get_link_loblaws_tuple_queue size is {}\ncurrent running thread {}\n' \
                     'current {} elements in get_link_result_list, total {} urls\n' \
                     'current {} elements in get_link_failed_list.\n' \
                     'current {} elements in get_price_result_list\n' \
                     'current {} elements in get_price_failed_list.\n' \
                     'getting_links:{}, getting_price:{}, writting_links_to_db:{}, writting_prices_to_db:{}.\n' \
                     'current {} element in id_url_tuple_list, {} element in failed_item_list, ' \
                     'current {} thread for get item detail, getting_item_detail:{}, current {} in item_detail_result_tuple_list'.format(self.getting_links,
                                                                           self.get_link_loblaws_tuple_queue.qsize(),
                                                                           self.current_running_thread,
                                                                           len(self.get_link_result_list),
                                                                           len(self.get_link_failed_list),total_item_link,
                                                                           len(self.get_price_result_list),
                                                                           len(self.get_price_failed_list),
                                                                        self.getting_links, self.getting_price, self.writting_links_to_db, self.writting_prices_to_db,
                                                                                            len(self.id_url_tuple_list), len(self.failed_get_item_detail_tuple_list), self.get_item_detail_thread_count,self.getting_item_detail, len(self.item_detail_result_tuple_list))
        return result_str
    def initial_get_loblaws_item_price(self):
        if self.getting_price:
            logger.error('trying to getting links when the server is running similiar tasks, please try again later')
            return False
        self.getting_price = True
        result = self.initial_get_loblaws_item_links()
        if not result:
            logger.error('trying to getting links when the server is running similiar tasks, please try again later')
            self.getting_price = False
            return False
        else:
            logger.info('task get_loblaws_item_price is initialized with initial page \n{}\ncurrently queue size {}'
                        .format(self.loblaws_initial_page, self.get_link_loblaws_tuple_queue.qsize()))
            return True


    def initial_get_loblaws_item_links(self):
        if self.getting_links:
            logger.error('trying to getting links when the server is running similiar tasks, please try again later')
            return False
        if self.writting_links_to_db or self.writting_prices_to_db:
            logger.error('trying to getting links when the server is writting links or prices into db, please try again later')
            return False
        elif not self.get_link_loblaws_tuple_queue.empty() or self.current_running_thread !=0:
            logger.error('trying to execute get_loblaws_item_links when queue get_link_loblaws_tuple_queue is not '
                         'empty, currently {} tasks in queue, currently {} running thread'.format(
                self.get_link_loblaws_tuple_queue.qsize(), self.current_running_thread))
            return False
        result = has_more_subcategories((self.loblaws_initial_page,[]), headless=True, disableimage=True)
        if isinstance(result, list):
            if not self.getting_price:
                self.getting_links = True
            for element in result:
                self.get_link_loblaws_tuple_queue.put(element)

            logger.info('task get_loblaws_item_links is initialized with initial page \n{}\ncurrently queue size {}'
                        .format(self.loblaws_initial_page, self.get_link_loblaws_tuple_queue.qsize()))
            return True
        else:
            logger.error('expecting non-leaf webpage as loblaws initial page, initial url is \n{}'.format(
                self.loblaws_initial_page))
            return False


    def monitor_thread(self):
        logger.info('server_loblaws monitor thread started')
        while True:

            # starting new get_loblaws_item_links with element in get_link_loblaws_tuple_queue
            if not self.get_link_loblaws_tuple_queue.empty():
                if self.current_running_thread <= self.max_running_thread:
                    with self.current_running_thread_lock:
                        self.current_running_thread += 1
                    url_category_tuple = self.get_link_loblaws_tuple_queue.get()

                    if self.getting_links:
                        threading.Thread(target=self.get_loblaws_item_links,
                                         args=(url_category_tuple,)).start()
                        logger.debug('started a new thread for get_loblaws_item_links, current {} running thread'
                                     .format(self.current_running_thread))
                    elif self.getting_price:
                        threading.Thread(target=self.get_loblaws_item_prices,
                                         args=(url_category_tuple,)).start()
                        logger.debug('started a new thread for get_loblaws_item_prices, current {} running thread'
                                     .format(self.current_running_thread))
            if self.getting_item_detail:
                while len(self.id_url_tuple_list) > 0 and self.get_item_detail_thread_count < self.max_running_thread:
                    id_url_tuple = self.id_url_tuple_list.pop(0)

                    threading.Thread(target=self.get_item_detail_thread,
                                     args=(id_url_tuple,)).start()
                    logger.debug('started a new thread for get_item_detail_thread, current {} running thread'
                                 .format(self.get_item_detail_thread_count))

                if len(self.id_url_tuple_list) == 0 and self.get_item_detail_thread_count == 0:
                    self.getting_item_detail = False

                if len(self.item_detail_result_tuple_list) > self.item_detail_max_write_length:
                    detail_tuple_list = self.item_detail_result_tuple_list[:self.item_detail_max_write_length]
                    respond = self.write_item_to_db(detail_tuple_list)
                    if respond:
                        self.item_detail_result_tuple_list = self.item_detail_result_tuple_list[self.item_detail_max_write_length:]
                    else:
                        logger.error("error when write item detail into db, please check db connection")
            elif len(self.item_detail_result_tuple_list)>0:
                respond = self.write_item_to_db(self.item_detail_result_tuple_list)
                if respond:
                    self.item_detail_result_tuple_list = []
                else:
                    logger.error("error when write item detail into db, please check db connection")
            if self.quit_server:
                logger.info('ending server_loblaws monitor thread')
                break


    def retry_first_max_failed_get_link_list(self):
        if not self.getting_links or self.getting_price:
            self.getting_links = True
            threads_to_start = min(self.max_running_thread, len(self.get_link_failed_list))
            retry_list = self.get_link_failed_list[:threads_to_start]
            self.get_link_failed_list = self.get_link_failed_list[threads_to_start:]
            for url_category_tuple in retry_list:
                with self.current_running_thread_lock:
                    self.current_running_thread += 1
                threading.Thread(target=self.get_loblaws_item_links,
                                 args=(url_category_tuple,)).start()
                logger.debug('started a new thread for get_loblaws_item_links, current {} running thread'
                             .format(self.current_running_thread))
            logger.debug('retrying first {} failed list'.format(threads_to_start))
            return True
        else:
            logger.debug('server is getting links, please try again later')
            return False
    def retry_first_max_failed_get_price_list(self):
        if not self.getting_links or self.getting_price:
            #self.getting_links = True
            self.getting_price = True
            threads_to_start = min(self.max_running_thread, len(self.get_price_failed_list))
            retry_list = self.get_price_failed_list[:threads_to_start]
            self.get_price_failed_list = self.get_price_failed_list[threads_to_start:]
            for url_category_tuple in retry_list:
                with self.current_running_thread_lock:
                    self.current_running_thread += 1
                threading.Thread(target=self.get_loblaws_item_links,
                                 args=(url_category_tuple,)).start()
                logger.debug('started a new thread for get_loblaws_item_links, current {} running thread'
                             .format(self.current_running_thread))
            logger.debug('retrying first {} failed list'.format(threads_to_start))
            return True
        else:
            logger.debug('server is getting links, please try again later')
            return False
    def return_get_price_result_list(self):
        return self.get_price_result_list

    def return_get_price_failed_list(self):
        return self.get_price_failed_list
    def write_price_to_db(self, brand='Loblaws'):
        while len(self.get_price_result_list) > 0:
            current_price_tuple_list = self.get_price_result_list.pop(0)
            for current_price_tuple in current_price_tuple_list:
                category = current_price_tuple[1][1] # currently the root category is included, thus it starts with [1] instead of [0]
                url = current_price_tuple[0]
                url_for_select = url.replace("'", "''") # escaping single quote in mysql
                price = current_price_tuple[2]
                attribute_tuple_list = [(url,brand,category)]
                item_id = self.data.select_from_table('item_url',"url='{}'".format(url_for_select),'item_id')
                if len(item_id) == 0:
                    # insert it into item_url table first if the url doesn't exist in it
                    respond = self.data.execute_insert('item_url',
                                                       columnnames=['url', 'source_brand', 'category'],
                                                       attributes=attribute_tuple_list)
                    if not respond:
                        logger.error('error when writting into database, terminating the writing process now, '
                                     'please try again once the database issue is fixed')
                        self.writting_prices_to_db = False
                        self.get_price_result_list.append(current_price_tuple) # added it back to the list once failed
                        return False
                    item_id = self.data.select_from_table('item_url', "url='{}'".format(url_for_select), 'item_id')
                if len(item_id) != 1:
                    logger.error('error when getting id for item {}, terminating the writing process now, '
                                 'please try again once the database issue is fixed'.format(current_price_tuple))
                item_id = item_id[0][0]
                attribute_tuple_list = [(item_id, self.daily_id, price)]
                respond = self.data.execute_insert('item_price',
                                                   columnnames=['item_id', 'daily_id', 'price'],
                                                   attributes=attribute_tuple_list)
                if not respond:
                    logger.error('error when writting price {} into database, terminating the writing process now, '
                                 'please try again once the database issue is fixed'.format(attribute_tuple_list))
                    self.writting_prices_to_db = False
                    self.get_price_result_list.append(current_price_tuple_list)  # added it back to the list once failed
                    return False

        self.writting_prices_to_db = False
        return True



    def get_loblaws_item_prices(self, url_category_tuple):
        try:
            result = has_more_subcategories(url_category_tuple, headless=True, disableimage=True)
            if isinstance(result, list):
                for element in result:
                    self.get_link_loblaws_tuple_queue.put(element)
            else:
                category_list = url_category_tuple[1]
                category_list.append(result)
                """when the return from has_more_subcategories is not a list, 
                it is the leaf(current) category in string format, 
                it should be added to the category list by the function caller"""
                price_tuple_list = get_link_price((url_category_tuple[0], category_list), headless=True, disableimage=True)
                #self.result_list.append(link_tuples[0]) # only appending the url list
                self.get_price_result_list.append(price_tuple_list)  # only appending the url list

            logger.debug('successfully executed get_loblaws_item_prices with input tuple \n{}\n'
                         'current {} running thread'.format(url_category_tuple, self.current_running_thread))
        except:
            logger.error('error when trying to get loblaws item prices with input tuple\n{}\n'
                         'Now adding it to the failed list'.format(url_category_tuple))
            self.get_price_failed_list.append(url_category_tuple)
        finally:
            with self.current_running_thread_lock:
                self.current_running_thread -= 1
                print('current {} element in get price result list'.format(len(self.get_price_result_list)))
                if self.get_link_loblaws_tuple_queue.empty() and self.current_running_thread == 0 and self.getting_links:
                    self.getting_links = False
                if self.get_link_loblaws_tuple_queue.empty() and self.current_running_thread == 0 and self.getting_price:
                    self.getting_price = False

    def get_loblaws_item_links(self, url_category_tuple):
        try:
            result = has_more_subcategories(url_category_tuple, headless=True, disableimage=True)
            if isinstance(result, list):
                for element in result:
                    self.get_link_loblaws_tuple_queue.put(element)
            else:
                category_list = url_category_tuple[1]
                category_list.append(result)
                """when the return from has_more_subcategories is not a list, 
                it is the leaf(current) category in string format, 
                it should be added to the category list by the function caller"""
                link_tuples = get_link((url_category_tuple[0], category_list), headless=True, disableimage=True)
                #self.result_list.append(link_tuples[0]) # only appending the url list
                self.get_link_result_list.append(link_tuples)  # only appending the url list
                # TODO insert the result urls-categories tuples to database
                # TODO add interactive mode to server (another thread that monitors input)
            logger.debug('successfully executed get_loblaws_item_links with input tuple \n{}\n'
                         'current {} running thread'.format(url_category_tuple, self.current_running_thread))
        except:
            logger.error('error when trying to get loblaws item links with input tuple\n{}\n'
                         'Now adding it to the failed list'.format(url_category_tuple))
            self.get_link_failed_list.append(url_category_tuple)
        finally:
            with self.current_running_thread_lock:
                self.current_running_thread -= 1
                print('current {} element in result list'.format(len(self.get_link_result_list)))
                if self.get_link_loblaws_tuple_queue.empty() and self.current_running_thread == 0 and self.getting_links:
                    self.getting_links = False
                if self.get_link_loblaws_tuple_queue.empty() and self.current_running_thread == 0 and self.getting_price:
                    self.getting_price = False
"""server = Server_Loblaws()
server.get_category_list()
len_list = []
for category in server.category_list:
    len_list.append(server.get_id_url(category))
print(len_list)"""