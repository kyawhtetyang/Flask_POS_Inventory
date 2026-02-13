from models.inventory import Inventory


def test_add_product_and_find_product(tmp_path):
    db_path = tmp_path / "test_shop.db"
    inventory = Inventory(str(db_path))

    inventory.add_product("Apple", 1.5, 10, "Fruit")
    product = inventory.find_product("Apple")

    assert product is not None
    assert product.name == "Apple"
    assert product.quantity == 10
