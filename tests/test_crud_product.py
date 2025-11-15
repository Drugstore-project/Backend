from decimal import Decimal
from app.schemas.product import ProductCreate
from app.crud.product import create_product, list_products


def test_create(db):
    payload = ProductCreate(
        name="Aspirin",
        description="Pain reliever",
        price=9.99,
        stock_quantity=10,
        requires_prescription=False,
    )
    p = create_product(db, payload)
    assert p.id is not None
    assert p.name == "Aspirin"
    assert p.stock_quantity == 10
    assert p.price == Decimal("9.99")


def test_list(db):
    payload = ProductCreate(
        name="Aspirin",
        description="Pain reliever",
        price=9.99,
        stock_quantity=10,
        requires_prescription=False,
    )

    # cria um produto (reaproveita o create)
    p = create_product(db, payload)

    # lista e confirma que o produto criado está presente
    products = list_products(db)
    assert isinstance(products,list)
    assert len(products) == 1
    product = products[0]
    assert product.name == payload.name
   

