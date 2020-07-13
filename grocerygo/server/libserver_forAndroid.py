import sys
import selectors
import json
import io
import struct

from server_loblaws import *
from database_app_server import *

request_search = {
    "morpheus": "Follow the white rabbit. \U0001f430",
    "ring": "In the caves beneath the Misty Mountains. \U0001f48d",
    "\U0001f436": "\U0001f43e Playing ball! \U0001f3d0",
}

source_brand_dict = {"Loblaws":0, "Walmart":1,"Metro":2}
category_dict = {}
category_dict.update(dict.fromkeys(['Fruits & Vegetables','FRUITS & VEGETABLES',],0))
category_dict.update(dict.fromkeys(['Drinks','BEVERAGES',],1))
category_dict.update(dict.fromkeys(['Ready Made Meals','Deli','Deli & Ready Made Meals','DELI & PREPARED MEALS',],2))
category_dict.update(dict.fromkeys(['Bakery','BREAD & BAKERY PRODUCTS',],3))
category_dict.update(dict.fromkeys(['Dairy and Eggs','Dairy & Eggs','DAIRY & EGGS',],4))
category_dict.update(dict.fromkeys(['Pantry','Pantry Food','PANTRY', ],5))
category_dict.update(dict.fromkeys(['Meat & Seafood','MEAT & POULTRY','FISH & SEAFOOD',],6))
category_dict.update(dict.fromkeys(['Frozen','Frozen Food','FROZEN',],7))
data = DatabaseObj("localhost", "readwrite", "readwrite", databasename='grocerygo',
                                         write_access=True)

sql_statement = "select item_url.item_id, item.name, item_url.category, item.brand, item_url.source_brand, item.img_src from item_url inner join item on item_url.item_id = item.item_id inner join item_price on item_url.item_id = item_price.item_id"
result = data.execute_select(sql_statement)
print(len(result))
sql_statement = "select distinct category, source_brand from item_url"
print(data.execute_select(sql_statement))
sample_data = [[[] for j in range(8)] for i in range(3)]
hard_code = [[[] for j in range(8)] for i in range(3)]
print(len(sample_data))
print(len(sample_data[0]))

#max_data = 2

for record in result:
    if record[2] in category_dict:
        source_brand_index = source_brand_dict[record[4]]
        category_index = category_dict[record[2]]
        #if len(sample_data[source_brand_index][category_index]) < max_data:
        hard_code[source_brand_index][category_index].append([str(record[0]),record[1],str(category_index),str(record[3]), str(source_brand_index),record[5]])
        sample_data[source_brand_index][category_index].append({'item_id':str(record[0]),'item_name':record[1],'category':str(category_index),'item_brand':str(record[3]),'source_brand':str(source_brand_index),'img_src':record[5]})
mixed = []
for i in sample_data:
    for j in i:
        for k in j:
            mixed.append(k)
print(len(mixed))
x=json.dumps(mixed)
loblaws_server = Server_Loblaws()
loblaws_server_dict = {
    "status": loblaws_server.get_server_status,
    'reset': loblaws_server.force_reset,
    "quit": loblaws_server.send_quit,
    "initial_link": loblaws_server.initial_get_loblaws_item_links,
    "result_link": loblaws_server.return_get_link_result_list,
    "failed_link": loblaws_server.return_get_link_failed_list,
    'write_link': loblaws_server.start_writting_links,
    'retry_link': loblaws_server.retry_first_max_failed_get_link_list,
    "initial_price": loblaws_server.initial_get_loblaws_item_price,
    "result_price": loblaws_server.return_get_price_result_list,
    "failed_price": loblaws_server.return_get_price_failed_list,
    'write_price': loblaws_server.start_writting_price,
    'retry_price': loblaws_server.retry_first_max_failed_get_price_list,
    'initial_detail': loblaws_server.start_getting_item_detail,
    'detail_list': loblaws_server.get_id_url_tuple_list,
    'detail_failed': loblaws_server.get_failed_item_detail_tuple_list,
    'retry_detail': loblaws_server.retry_failed_get_item_detail,
    'give_up_thread': loblaws_server.give_up_thread

}
respond = x
#respond = """[{"item_id": "527", "item_name": "Organic Honeydew Melon", "category": "0", "item_brand": "None", "source_brand": "0", "img_src": "https://assets.shop.loblaws.ca/products_jpeg/20289708001/en/20289708001_lrg_1_@1x.jpg"}, {"item_id": "1430", "item_name": "Caf\u00e9 blanc 3-en-1", "category": "1", "item_brand": "None", "source_brand": "0", "img_src": "https://assets.shop.loblaws.ca/products_jpeg/21094512/en/21094512_lrg_1_@1x.jpg"}, {"item_id": "6774", "item_name": "1/4 Rotisserie Chicken Dark Meat", "category": "2", "item_brand": "None", "source_brand": "0", "img_src": "https://assets.shop.loblaws.ca/products_jpeg/20116090/en/20116090_lrg_1_@1x.jpg"}, {"item_id": "4365", "item_name": "Ace Cheddar Onion Demi Baguette", "category": "3", "item_brand": "ACE", "source_brand": "0", "img_src": "https://assets.shop.loblaws.ca/products_jpeg/21018897/en/21018897_lrg_1_@1x.jpg"}, {"item_id": "249", "item_name": "Organic Yogurt, Mango Apricot", "category": "4", "item_brand": "LIBERTE", "source_brand": "0", "img_src": "https://assets.shop.loblaws.ca/products_jpeg/20790591001/en/20790591001_lrg_1_@1x.jpg"}, {"item_id": "7412", "item_name": "Ready Crust, Chocolate Pie Crust", "category": "5", "item_brand": "KEEBLER", "source_brand": "0", "img_src": "https://assets.shop.loblaws.ca/products_jpeg/20117311002/en/20117311002_lrg_1_@1x.jpg"}, {"item_id": "907", "item_name": "Plant Based Beefless Burgers, Plant-Based, Vegan", "category": "6", "item_brand": "PRESIDENT'S CHOICE", "source_brand": "0", "img_src": "https://assets.shop.loblaws.ca/products_jpeg/21179192/en/21179192_lrg_1_@1x.jpg"}, {"item_id": "5545", "item_name": "Premium Ice", "category": "7", "item_brand": "None", "source_brand": "0", "img_src": "https://assets.shop.loblaws.ca/products_jpeg/20158645/en/20158645_lrg_1_@1x.jpg"}, {"item_id": "31561", "item_name": "Cilantro", "category": "0", "item_brand": "None", "source_brand": "1", "img_src": "https://i5.walmartimages.ca/images/Large/094/548/6000200094548.jpg"}, {"item_id": "31961", "item_name": "Beck's Non-Alcoholic Beer", "category": "1", "item_brand": "None", "source_brand": "1", "img_src": "https://i5.walmartimages.ca/images/Large/243/783/243783.jpg"}, {"item_id": "31981", "item_name": "Molinaro's Pizza Dough", "category": "2", "item_brand": "Molinaro's", "source_brand": "1", "img_src": "https://i5.walmartimages.ca/images/Large/424/734/6000198424734.jpg"}, {"item_id": "32633", "item_name": "The Bakery White Crusty Loaf", "category": "3", "item_brand": "The Bakery", "source_brand": "1", "img_src": "https://i5.walmartimages.ca/images/Large/261/254/6000200261254.jpg"}, {"item_id": "31582", "item_name": "Pillsbury\u2122 Original Crescents", "category": "4", "item_brand": "Pillsbury", "source_brand": "1", "img_src": "https://i5.walmartimages.ca/images/Large/625/347/6000201625347.jpg"}, {"item_id": "34959", "item_name": "Uncle Ben's Southern Chili Style Beans", "category": "5", "item_brand": "None", "source_brand": "1", "img_src": "https://i5.walmartimages.ca/images/Large/141/464/6000201141464.jpg"}, {"item_id": "32520", "item_name": "Maple Leaf Naturally Smoked Bacon", "category": "6", "item_brand": "Maple Leaf", "source_brand": "1", "img_src": "https://i5.walmartimages.ca/images/Large/219/406/999999-63100219406.jpg"}, {"item_id": "33031", "item_name": "Kinnikinnick Gluten Free Pie Crust 9 Inch", "category": "7", "item_brand": "None", "source_brand": "1", "img_src": "https://i5.walmartimages.ca/images/Large/124/421/6000200124421.jpg"}, {"item_id": "48970", "item_name": "Banana", "category": "0", "item_brand": "None", "source_brand": "2", "img_src": "https://product-images.metro.ca/images/hee/h5c/8872794652702.jpg"}, {"item_id": "54431", "item_name": "Natural Spring Water", "category": "1", "item_brand": "ESKA", "source_brand": "2", "img_src": "https://product-images.metro.ca/images/h41/hf4/9351392133150.jpg"}, {"item_id": "66443", "item_name": "Old-fashioned smoked ham", "category": "2", "item_brand": "THE DELI-SHOP", "source_brand": "2", "img_src": "https://product-images.metro.ca/images/h1f/h62/8820483719198.jpg"}, {"item_id": "59502", "item_name": "Baguette", "category": "3", "item_brand": "PREMI\u00c8RE MOISSON", "source_brand": "2", "img_src": "https://product-images.metro.ca/images/h03/ha4/9252545560606.jpg"}, {"item_id": "49552", "item_name": "Large Eggs", "category": "4", "item_brand": "SELECTION", "source_brand": "2", "img_src": "https://product-images.metro.ca/images/h3e/h65/9398467985438.jpg"}, {"item_id": "50740", "item_name": "White vinegar", "category": "5", "item_brand": "SELECTION", "source_brand": "2", "img_src": "https://product-images.metro.ca/images/he6/h09/8854725820446.jpg"}, {"item_id": "56200", "item_name": "Medium Ground Beef, Value Pack", "category": "6", "item_brand": "None", "source_brand": "2", "img_src": "https://product-images.metro.ca/images/h61/h5b/9188501585950.jpg"}, {"item_id": "58181", "item_name": "Frozen chicken pot pie", "category": "7", "item_brand": "ST-HUBERT", "source_brand": "2", "img_src": "https://product-images.metro.ca/images/h3a/h0f/8821239021598.jpg"}]"""
#respond = """[{"item_id": "527", "item_name": "Organic Honeydew Melon", "category": "0", "item_brand": "None", "source_brand": "0", "img_src": "https://assets.shop.loblaws.ca/products_jpeg/20289708001/en/20289708001_lrg_1_@1x.jpg"}, {"item_id": "528", "item_name": "Pink Lady Apples", "category": "0", "item_brand": "PC ORGANICS", "source_brand": "0", "img_src": "https://assets.shop.loblaws.ca/products_jpeg/20793536001/en/20793536001_lrg_1_@1x.jpg"}, {"item_id": "1430", "item_name": "Caf\u00e9 blanc 3-en-1", "category": "1", "item_brand": "None", "source_brand": "0", "img_src": "https://assets.shop.loblaws.ca/products_jpeg/21094512/en/21094512_lrg_1_@1x.jpg"}, {"item_id": "1431", "item_name": "Brand Dulce De Leche Sweetened Condensed Milk", "category": "1", "item_brand": "EAGLE BRAND", "source_brand": "0", "img_src": "https://assets.shop.loblaws.ca/products_jpeg/21012627/en/21012627_lrg_1_@1x.jpg"}, {"item_id": "6774", "item_name": "1/4 Rotisserie Chicken Dark Meat", "category": "2", "item_brand": "None", "source_brand": "0", "img_src": "https://assets.shop.loblaws.ca/products_jpeg/20116090/en/20116090_lrg_1_@1x.jpg"}, {"item_id": "6775", "item_name": "Cripsy Chicken Sandwich", "category": "2", "item_brand": "FROM OUR CHEFS", "source_brand": "0", "img_src": "https://assets.shop.loblaws.ca/products_jpeg/21086084/en/21086084_lrg_1_@1x.jpg"}, {"item_id": "4365", "item_name": "Ace Cheddar Onion Demi Baguette", "category": "3", "item_brand": "ACE", "source_brand": "0", "img_src": "https://assets.shop.loblaws.ca/products_jpeg/21018897/en/21018897_lrg_1_@1x.jpg"}, {"item_id": "4366", "item_name": "Petit Pain, Sundried Tomato", "category": "3", "item_brand": "ACE", "source_brand": "0", "img_src": "https://assets.shop.loblaws.ca/products_jpeg/20639494/en/20639494_lrg_1_@1x.jpg"}, {"item_id": "249", "item_name": "Organic Yogurt, Mango Apricot", "category": "4", "item_brand": "LIBERTE", "source_brand": "0", "img_src": "https://assets.shop.loblaws.ca/products_jpeg/20790591001/en/20790591001_lrg_1_@1x.jpg"}, {"item_id": "250", "item_name": "Organic Almond Milk, Original", "category": "4", "item_brand": "SO NICE", "source_brand": "0", "img_src": "https://assets.shop.loblaws.ca/products_jpeg/20794550001/en/20794550001_lrg_1_@1x.jpg"}, {"item_id": "7412", "item_name": "Ready Crust, Chocolate Pie Crust", "category": "5", "item_brand": "KEEBLER", "source_brand": "0", "img_src": "https://assets.shop.loblaws.ca/products_jpeg/20117311002/en/20117311002_lrg_1_@1x.jpg"}, {"item_id": "7413", "item_name": "Graham Crumbs", "category": "5", "item_brand": "HONEYMAID", "source_brand": "0", "img_src": "https://assets.shop.loblaws.ca/products_jpeg/20302704002/en/20302704002_lrg_1_@1x.jpg"}, {"item_id": "907", "item_name": "Plant Based Beefless Burgers, Plant-Based, Vegan", "category": "6", "item_brand": "PRESIDENT'S CHOICE", "source_brand": "0", "img_src": "https://assets.shop.loblaws.ca/products_jpeg/21179192/en/21179192_lrg_1_@1x.jpg"}, {"item_id": "908", "item_name": "Portobello Swiss Burger", "category": "6", "item_brand": "PRESIDENT'S CHOICE", "source_brand": "0", "img_src": "https://assets.shop.loblaws.ca/products_jpeg/20941351/en/20941351_lrg_1_@1x.jpg"}, {"item_id": "5545", "item_name": "Premium Ice", "category": "7", "item_brand": "None", "source_brand": "0", "img_src": "https://assets.shop.loblaws.ca/products_jpeg/20158645/en/20158645_lrg_1_@1x.jpg"}, {"item_id": "5546", "item_name": "Citrus", "category": "7", "item_brand": "FIVE ALIVE", "source_brand": "0", "img_src": "https://assets.shop.loblaws.ca/products_jpeg/20418326001/en/20418326001_lrg_1_@1x.jpg"}, {"item_id": "31561", "item_name": "Cilantro", "category": "0", "item_brand": "None", "source_brand": "1", "img_src": "https://i5.walmartimages.ca/images/Large/094/548/6000200094548.jpg"}, {"item_id": "31562", "item_name": "Mint, Fresh", "category": "0", "item_brand": "None", "source_brand": "1", "img_src": "https://i5.walmartimages.ca/images/Large/801/072/999999-625647801072.jpg"}, {"item_id": "31961", "item_name": "Beck's Non-Alcoholic Beer", "category": "1", "item_brand": "None", "source_brand": "1", "img_src": "https://i5.walmartimages.ca/images/Large/243/783/243783.jpg"}, {"item_id": "31962", "item_name": "Gioia Red Bitter Non Alcoholic Aperitif", "category": "1", "item_brand": "None", "source_brand": "1", "img_src": "https://i5.walmartimages.ca/images/Large/921/106/999999-779921921106.jpg"}, {"item_id": "31981", "item_name": "Molinaro's Pizza Dough", "category": "2", "item_brand": "Molinaro's", "source_brand": "1", "img_src": "https://i5.walmartimages.ca/images/Large/424/734/6000198424734.jpg"}, {"item_id": "31983", "item_name": "Your Fresh Market Pizza Kit", "category": "2", "item_brand": "Your Fresh Market", "source_brand": "1", "img_src": "https://i5.walmartimages.ca/images/Large/084/580/628915084580.jpg"}, {"item_id": "32633", "item_name": "The Bakery White Crusty Loaf", "category": "3", "item_brand": "The Bakery", "source_brand": "1", "img_src": "https://i5.walmartimages.ca/images/Large/261/254/6000200261254.jpg"}, {"item_id": "32634", "item_name": "Your Fresh Market French-Style Baguette", "category": "3", "item_brand": "Your Fresh Market", "source_brand": "1", "img_src": "https://i5.walmartimages.ca/images/Large/783/307/6000201783307.jpg"}, {"item_id": "31582", "item_name": "Pillsbury\u2122 Original Crescents", "category": "4", "item_brand": "Pillsbury", "source_brand": "1", "img_src": "https://i5.walmartimages.ca/images/Large/625/347/6000201625347.jpg"}, {"item_id": "31583", "item_name": "Pillsbury Grands Cinnamon Rolls Flaky Supreme with Icing", "category": "4", "item_brand": "Pillsbury", "source_brand": "1", "img_src": "https://i5.walmartimages.ca/images/Large/625/485/6000201625485.jpg"}, {"item_id": "34959", "item_name": "Uncle Ben's Southern Chili Style Beans", "category": "5", "item_brand": "None", "source_brand": "1", "img_src": "https://i5.walmartimages.ca/images/Large/141/464/6000201141464.jpg"}, {"item_id": "34962", "item_name": "Uncle Ben's Zesty Mexican Style Beans", "category": "5", "item_brand": "None", "source_brand": "1", "img_src": "https://i5.walmartimages.ca/images/Large/141/362/6000201141362.jpg"}, {"item_id": "32520", "item_name": "Maple Leaf Naturally Smoked Bacon", "category": "6", "item_brand": "Maple Leaf", "source_brand": "1", "img_src": "https://i5.walmartimages.ca/images/Large/219/406/999999-63100219406.jpg"}, {"item_id": "32521", "item_name": "Schneiders Naturally Smoked Regular Bacon", "category": "6", "item_brand": "Schneiders", "source_brand": "1", "img_src": "https://i5.walmartimages.ca/images/Large/110/389/6000198110389.jpg"}, {"item_id": "33031", "item_name": "Kinnikinnick Gluten Free Pie Crust 9 Inch", "category": "7", "item_brand": "None", "source_brand": "1", "img_src": "https://i5.walmartimages.ca/images/Large/124/421/6000200124421.jpg"}, {"item_id": "33032", "item_name": "Daiya Key Lime Cheezecake", "category": "7", "item_brand": "Daiya", "source_brand": "1", "img_src": "https://i5.walmartimages.ca/images/Large/461/482/6000198461482.jpg"}, {"item_id": "48970", "item_name": "Banana", "category": "0", "item_brand": "None", "source_brand": "2", "img_src": "https://product-images.metro.ca/images/hee/h5c/8872794652702.jpg"}, {"item_id": "48971", "item_name": "English cucumber", "category": "0", "item_brand": "None", "source_brand": "2", "img_src": "https://product-images.metro.ca/images/hc5/h7d/8874246078494.jpg"}, {"item_id": "54431", "item_name": "Natural Spring Water", "category": "1", "item_brand": "ESKA", "source_brand": "2", "img_src": "https://product-images.metro.ca/images/h41/hf4/9351392133150.jpg"}, {"item_id": "54432", "item_name": "Orange Juice Without Pulp, Premium", "category": "1", "item_brand": "OASIS", "source_brand": "2", "img_src": "https://product-images.metro.ca/images/h78/he7/9383675101214.jpg"}, {"item_id": "66443", "item_name": "Old-fashioned smoked ham", "category": "2", "item_brand": "THE DELI-SHOP", "source_brand": "2", "img_src": "https://product-images.metro.ca/images/h1f/h62/8820483719198.jpg"}, {"item_id": "59502", "item_name": "Baguette", "category": "3", "item_brand": "PREMI\u00c8RE MOISSON", "source_brand": "2", "img_src": "https://product-images.metro.ca/images/h03/ha4/9252545560606.jpg"}, {"item_id": "59503", "item_name": "100% Whole wheat sliced bread", "category": "3", "item_brand": "DEMPSTER'S", "source_brand": "2", "img_src": "https://product-images.metro.ca/images/h3e/h59/9398164193310.jpg"}, {"item_id": "49552", "item_name": "Large Eggs", "category": "4", "item_brand": "SELECTION", "source_brand": "2", "img_src": "https://product-images.metro.ca/images/h3e/h65/9398467985438.jpg"}, {"item_id": "49553", "item_name": "Salted Butter", "category": "4", "item_brand": "SELECTION", "source_brand": "2", "img_src": "https://product-images.metro.ca/images/h92/hea/8834785083422.jpg"}, {"item_id": "50740", "item_name": "White vinegar", "category": "5", "item_brand": "SELECTION", "source_brand": "2", "img_src": "https://product-images.metro.ca/images/he6/h09/8854725820446.jpg"}, {"item_id": "50741", "item_name": "Low sodium tomato paste", "category": "5", "item_brand": "SELECTION", "source_brand": "2", "img_src": "https://product-images.metro.ca/images/hf0/h0b/8856193859614.jpg"}, {"item_id": "56200", "item_name": "Medium Ground Beef, Value Pack", "category": "6", "item_brand": "None", "source_brand": "2", "img_src": "https://product-images.metro.ca/images/h61/h5b/9188501585950.jpg"}, {"item_id": "56201", "item_name": "Pork Tenderloins, Value Pack", "category": "6", "item_brand": "None", "source_brand": "2", "img_src": "https://product-images.metro.ca/images/h76/hf0/9233895325726.jpg"}, {"item_id": "58181", "item_name": "Frozen chicken pot pie", "category": "7", "item_brand": "ST-HUBERT", "source_brand": "2", "img_src": "https://product-images.metro.ca/images/h3a/h0f/8821239021598.jpg"}, {"item_id": "58182", "item_name": "Frozen chicken for Chinese fondue", "category": "7", "item_brand": "SELECTION", "source_brand": "2", "img_src": "https://product-images.metro.ca/images/h09/h59/9185743667230.jpg"}]"""
class Message:
    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self._recv_buffer = b""
        self._send_buffer = b""
        self._jsonheader_len = None
        self.jsonheader = None
        self.request = None
        self.response_created = False

    def _set_selector_events_mask(self, mode):
        """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError(f"Invalid events mask mode {repr(mode)}.")
        self.selector.modify(self.sock, events, data=self)

    def _read(self):
        try:
            # Should be ready to read
            data = self.sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        else:
            if data:
                self._recv_buffer += data
                print("current data:",data)
            else:
                raise RuntimeError("Peer closed.")

    def _write(self):
        if self._send_buffer:
            print("sending", repr(self._send_buffer), "to", self.addr)
            try:
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]
                # Close when the buffer is drained. The response has been sent.
                if sent and not self._send_buffer:
                    self.close()

    def _json_encode(self, obj, encoding):
        return json.dumps(obj, ensure_ascii=False).encode(encoding)

    def _json_decode(self, json_bytes, encoding):
        tiow = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=""
        )
        obj = json.load(tiow)
        tiow.close()
        return obj

    def _create_message(
        self, *, content_bytes, content_type, content_encoding
    ):
        jsonheader = {
            "byteorder": sys.byteorder,
            "content-type": content_type,
            "content-encoding": content_encoding,
            "content-length": len(content_bytes),
        }
        jsonheader_bytes = self._json_encode(jsonheader, "utf-8")
        print(len(jsonheader_bytes))
        print(jsonheader_bytes)
        message_hdr = (len(jsonheader_bytes)).to_bytes(1,byteorder='big',signed=True)
        message = message_hdr + jsonheader_bytes + content_bytes
        return message

    def _create_response_json_content(self):
        action = self.request.get("action")
        print('action:',action)
        if action == "search":
            query = self.request.get("value")
            answer = request_search.get(query) or f'No match for "{query}".'
            content = {"result": answer}
        elif action == "server":
            query = self.request.get("value")
            answer = loblaws_server_dict.get(query)() or f'No match for "{query}".'
            content = {"result": respond}
        else:
            content = {"result": f'Error: invalid action "{action}".'}
        content_encoding = "utf-8"
        response = {
            "content_bytes": str.encode(respond),#self._json_encode(content, content_encoding),
            "content_type": "text/json",
            "content_encoding": content_encoding,
        }
        return response

    def _create_response_binary_content(self):
        response = {
            "content_bytes": b"First 10 bytes of request: "
            + self.request[:10],
            "content_type": "binary/custom-server-binary-type",
            "content_encoding": "binary",
        }
        return response

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()

    def read(self):
        self._read()

        if self._jsonheader_len is None:
            self.process_protoheader()

        if self._jsonheader_len is not None:
            if self.jsonheader is None:
                self.process_jsonheader()

        if self.jsonheader:
            if self.request is None:
                self.process_request()

    def write(self):
        if self.request:
            if not self.response_created:
                self.create_response()

        self._write()

    def close(self):
        print("closing connection to", self.addr)
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            print(
                "error: selector.unregister() exception for",
                f"{self.addr}: {repr(e)}",
            )

        try:
            self.sock.close()
        except OSError as e:
            print(
                "error: socket.close() exception for",
                f"{self.addr}: {repr(e)}",
            )
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None

    def process_protoheader(self):
        hdrlen = 1
        if len(self._recv_buffer) >= hdrlen:
            self._jsonheader_len = int.from_bytes(self._recv_buffer[:hdrlen], byteorder='big', signed=True)
            self._recv_buffer = self._recv_buffer[hdrlen:]

    def process_jsonheader(self):
        hdrlen = self._jsonheader_len
        if len(self._recv_buffer) >= hdrlen:
            self.jsonheader = self._json_decode(
                self._recv_buffer[:hdrlen], "utf-8"
            )
            self._recv_buffer = self._recv_buffer[hdrlen:]
            for reqhdr in (
                "byteorder",
                "content-length",
                "content-type",
                "content-encoding",
            ):
                if reqhdr not in self.jsonheader:
                    raise ValueError(f'Missing required header "{reqhdr}".')

    def process_request(self):
        content_len = self.jsonheader["content-length"]
        if not len(self._recv_buffer) >= content_len:
            return
        data = self._recv_buffer[:content_len]
        self._recv_buffer = self._recv_buffer[content_len:]
        if self.jsonheader["content-type"] == "text/json":
            encoding = self.jsonheader["content-encoding"]
            self.request = self._json_decode(data, encoding)
            print("received request", repr(self.request), "from", self.addr)
        else:
            # Binary or unknown content-type
            self.request = data
            print(
                f'received {self.jsonheader["content-type"]} request from',
                self.addr,
            )
        # Set selector to listen for write events, we're done reading.
        self._set_selector_events_mask("w")

    def create_response(self):
        if self.jsonheader["content-type"] == "text/json":
            response = self._create_response_json_content()
        else:
            # Binary or unknown content-type
            response = self._create_response_binary_content()
        message = self._create_message(**response)
        self.response_created = True
        self._send_buffer += message