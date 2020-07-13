import json

import database_obj
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
data = database_obj.DatabaseObj("localhost", "readwrite", "readwrite", databasename='grocerygo',
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

max_data = 2

for record in result:
    if record[2] in category_dict:
        source_brand_index = source_brand_dict[record[4]]
        category_index = category_dict[record[2]]
        if len(sample_data[source_brand_index][category_index]) < max_data:
            hard_code[source_brand_index][category_index].append([str(record[0]),record[1],str(category_index),str(record[3]), str(source_brand_index),record[5]])
            sample_data[source_brand_index][category_index].append({'item_id':str(record[0]),'item_name':record[1],'category':str(category_index),'item_brand':str(record[3]),'source_brand':str(source_brand_index),'img_src':record[5]})
mixed = []
for i in sample_data:
    for j in i:
        for k in j:
            mixed.append(k)
print(len(mixed))
x=json.dumps(mixed)
print(x)
y = json.loads(x)
print(y)
#products.add(new Product(id.get(x),titles.get(x),body.get(x),vendor.get(x),types.get(x),created.get(x),handle.get(x),updated.get(x),at.get(x),suffix.get(x),scope.get(x),tags.get(x),imgURL.get(x)));
"""print("ArrayList<Item>  items=new ArrayList<>();")
for i in hard_code:
    for j in i:
        for k in j:
            print('items.add(new Item("{}"));'.format('","'.join(k)))

#Item(String item_id, String item_name, String item_category, String item_brand, String source_brand, String img_src)
for key, value in source_brand_dict.items():
    print('source_brand_map.put("{}","{}")'.format(value, key))
for key, value in category_dict.items():
    print('category_map.put("{}","{}")'.format( value, key))"""