import http.server
import socketserver
from database_http_server import *
class Item:
    def __init__(self, id, url, name, brand, src, price):
        self.item_id = id
        self.item_url = url
        self.item_name = name
        if brand is None:
            brand = ''
        self.item_brand = brand
        self.img_src = src
        self.item_price = price

        self.searchable_str = self.item_brand + self.item_name
    def toString(self):
        if self.item_brand:
            return '{} {} : {}'.format(self.item_brand,self.item_name,self.item_price)
        else:
            return '{} : {}'.format(self.item_name,self.item_price)

def initialization(item_list):
    sql_statement = "select item_url.item_id, item_url.url, item.name, item.brand, item.img_src, item_price.price from item_url inner join item on item_url.item_id = item.item_id inner join item_price on item_url.item_id = item_price.item_id"
    data = DatabaseObj("localhost", "readwrite", "readwrite", databasename='grocerygo',
                       write_access=True)
    result = data.execute_select(sql_statement)
    for element in result:
        item_list.append(Item(element[0],element[1],element[2],element[3],element[4],element[5]))

def search_result(query, template):
    global item_list
    result = ''
    for item in item_list:
        if query.lower() in item.searchable_str.lower():
            result+=template.format(item.item_url,item.img_src, item.toString())
    return result

def generate_response(query):
    result_first_half = '<html><body><h2>GroceryGo</h2><form class="search_bar"><input type="text" placeholder="Search.." name="search"><button type="submit">Submit</button></form><div id="myList">'
    result_second_half = '</div></body></html>'
    result_middle = ''
    element_template ='<div style="background-color:#ddd;"><a href="{}"><img src="{}" width="200" height="200"><pre>{}</pre></a></div>'
    result_middle = search_result(query, element_template)
    """for i in range(10):
        #template = element_template.
        result_middle += element_template.format("https://www.google.ca/","https://www.google.ca/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",query)"""
    return result_first_half + result_middle + '<p>' + query + '</p>'+ result_second_half
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/' and not self.path.startswith('/?search='):
            return http.server.SimpleHTTPRequestHandler.send_error(self, 403)
        if self.path.startswith('/?search='):
            query_msg = self.path[9:]
            print('search:',query_msg)

            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            output = generate_response(query_msg)
            self.wfile.write(output.encode())
            print(output)
            return

        else:
            self.path = 'test.html'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Create an object of the above class
item_list = []
initialization(item_list)
print('initializaton done, total elements in item_list:',len(item_list))
handler_object = MyHttpRequestHandler

PORT = 8000
my_server = socketserver.TCPServer(("", PORT), handler_object)

# Star the server
my_server.serve_forever()