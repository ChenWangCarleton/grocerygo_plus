from grocerygo_plus.grocerygo.web_crawler import has_more_subcategories
def test_has_more_subcategories():
    food = 'https://www.loblaws.ca/Food/c/LSL001000000000?navid=flyout-L2-Food'
    apple = 'https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Fruit/Apples/plp/LSL001001001001?navid=CLP-L5-Apples'
    assert has_more_subcategories((apple,[]),headless=True) == 'Apples'
    assert len(has_more_subcategories((food,[]),headless=True)) == 15
