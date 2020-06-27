from grocerygo_plus.grocerygo.web_crawler.utils_metro import get_item_detail,get_item_price,get_item_link
def test_get_item_link():
    beer = 'https://www.metro.ca/en/online-grocery/aisles/beer-wine'
    result = get_item_link(beer,headless=True,disableimage=True)
    assert len(result) > 24
    assert len(result[0]) == 2


def test_get_item_price():
    beer = 'https://www.metro.ca/en/online-grocery/aisles/beer-wine'
    result = get_item_price(beer,headless=True,disableimage=True)
    assert len(result) > 24
    assert len(result[0]) == 3

def test_get_item_detail():
    beer = 'https://www.metro.ca/en/online-grocery/aisles/beer-wine'
    result = get_item_detail(beer,headless=True,disableimage=True)
    assert len(result) > 24
    assert len(result[0]) == 5
