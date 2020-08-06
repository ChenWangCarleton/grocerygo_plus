from database_http_server import *


class Item:
    def __init__(self, id, url, name, brand, src, price, description, ingredient, category, source_brand):
        self.item_id = str(id)
        self.item_url = url
        self.item_name = name
        self.img_src = src
        self.item_price = price
        self.item_category = category
        self.source_brand = source_brand

        if brand is None:
            brand = 'None'
        self.item_brand = brand

        if description is None:
            description = 'None'
        self.item_description = description

        if ingredient is None:
            ingredient = 'None'
        self.item_ingredient = ingredient

        self.searchable_str = self.item_brand + self.item_name

    def asdict(self):
        return {"item_id": self.item_id, "item_name": self.item_name, "img_src": self.img_src,
                "item_price": self.item_price, "item_category": self.item_category,
                "item_description": self.item_brand, "item_brand": self.item_brand,
                "item_ingredient": self.item_ingredient}
    def has_same_id(self, query):
        if self.item_id == query or self.item_id in query:
            return True
        else:
            return False
    def toString(self):
        if self.item_brand:
            return '{} {} : {}'.format(self.item_brand,self.item_name,self.item_price)
        else:
            return '{} : {}'.format(self.item_name,self.item_price)

def initialization(item_list):
    sql_statement = "select item_url.item_id, item_url.url, item.name, item.brand, item.img_src, item_price.price, item.description, item.ingredient, item_url.category, item_url.source_brand from item_url inner join item on item_url.item_id = item.item_id inner join item_price on item_url.item_id = item_price.item_id"
    data = DatabaseObj("localhost", "readwrite", "readwrite", databasename='grocerygo',
                       write_access=True)
    result = data.execute_select(sql_statement)
    for element in result:
        item_list.append(Item(element[0],element[1],element[2],element[3],element[4],element[5],element[6],element[7],element[8],element[9]))
def search_result(query, template):
    global item_list
    result = ''
    for item in item_list:
        if query.lower() in item.searchable_str.lower():
            result+=template.format(item.item_url,item.img_src, item.toString())
    return result

def generate_response_id(query):
    global item_list
    results = []
    ids = query.split(',')

    #print(ids)

    for item in item_list:
        if len(ids) == len(results):
            break
        if item.has_same_id(ids):
            results.append(item.asdict())

    return results


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

item_list = []
initialization(item_list)
print('initializaton done, total elements in item_list:',len(item_list))
"""for i in range(10):
    print(item_list[i*10].item_id)"""
