from grocerygo_plus.grocerygo.web_crawler.utils_walmart import has_subcategory
def test_has_subcategory():
    leaf_category = 'https://www.walmart.ca/en/grocery/meat-seafood/bacon/N-4526'
    root_category = 'https://www.walmart.ca/en/grocery/frozen-food/ice-cream-treats/N-3828'
    assert has_subcategory(leaf_category, headless=False, disableimage=True) is None
    assert len(has_subcategory(root_category, headless=False, disableimage=True)) == 6
