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
        """ a queue contains 2-element tuple to be used for getting itempages' link
         example of an element in the queue: (url, [categoryA, categoryB])"""
        self.current_running_thread = 0
        self.current_running_thread_lock = threading.Lock()
        # https://stackoverflow.com/questions/35088139/how-to-make-a-thread-safe-global-counter-in-python
        self.loblaws_initial_page = 'https://www.loblaws.ca/Food/Ready-Made-Meals/c/LSL001002000000'#'https://www.loblaws.ca/Food/c/LSL001000000000?navid=flyout-L2-Food'

        self.data = DatabaseObj("localhost", "readwrite", "readwrite", databasename='grocerygo', write_access=True)

        self.getting_links = False
        self.quit_server = False
        self.get_link_result_list = []
        self.get_link_failed_list = []

        self.monitor = threading.Thread(target=self.monitor_thread)
        self.monitor.start()


    def force_reset(self):
        logger.info('force reseting Server_Loblaws instance')
        if self.getting_links:
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
                     'current {} elements in get_link_failed_list.'.format(self.getting_links,
                                                                           self.get_link_loblaws_tuple_queue.qsize(),
                                                                           self.current_running_thread,
                                                                           len(self.get_link_result_list),
                                                                           total_item_link,
                                                                           len(self.get_link_failed_list))
        return result_str

    def initial_get_loblaws_item_links(self):
        if not self.get_link_loblaws_tuple_queue.empty() or self.current_running_thread !=0:
            logger.error('trying to execute get_loblaws_item_links when queue get_link_loblaws_tuple_queue is not '
                         'empty, currently {} tasks in queue, currently {} running thread'.format(
                self.get_link_loblaws_tuple_queue.qsize(), self.current_running_thread))
            return False
        result = has_more_subcategories((self.loblaws_initial_page,[]), headless=True, disableimage=True)
        if isinstance(result, list):
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
                    threading.Thread(target=self.get_loblaws_item_links,
                                     args=(url_category_tuple,)).start()
                    logger.debug('started a new thread for get_loblaws_item_links, current {} running thread'
                                 .format(self.current_running_thread))
                    self.getting_links = True
            if self.get_link_loblaws_tuple_queue.empty() and self.current_running_thread == 0 and self.getting_links:
                self.getting_links = False

            if self.quit_server:
                logger.info('ending server_loblaws monitor thread')
                break



    def get_loblaws_item_links(self, url_category_tuple):
        try:
            result = has_more_subcategories(url_category_tuple, headless=True, disableimage=True)
            if isinstance(result, list):
                for element in result:
                    self.get_link_loblaws_tuple_queue.put(element)
            else:
                category_list = url_category_tuple[1]
                category_list.append(result)
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
