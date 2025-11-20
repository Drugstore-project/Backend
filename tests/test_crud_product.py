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
        barcode="1234567890123",
        category="Analgesic"
    )
    p = create_product(db, payload)
    assert p.id is not None
    assert p.name == "Aspirin"
    assert p.stock_quantity == 10
    assert p.price == Decimal("9.99")
    assert p.barcode == "1234567890123"
    assert p.category == "Analgesic"


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

def test_update_product(db):
    payload = ProductCreate(
        name="Ibuprofen",
        description="Anti-inflammatory",
        price=14.99,
        stock_quantity=20,
        requires_prescription=False,
    )

    # cria um produto (reaproveita o create)
    p = create_product(db, payload)

    # atualiza o produto
    p.name = "Ibuprofen Updated"
    p.price = Decimal("12.99")
    db.commit()
    db.refresh(p)

    # verifica se as alterações foram aplicadas
    assert p.name == "Ibuprofen Updated"
    assert p.price == Decimal("12.99")
   
def test_delete_product(db):
    payload = ProductCreate(
        name="Paracetamol",
        description="Fever reducer",
        price=7.99,
        stock_quantity=15,

        requires_prescription=False,
    )

    # cria um produto (reaproveita o create)
    p = create_product(db, payload)

    # deleta o produto
    db.delete(p)
    db.commit()

    # verifica se o produto foi deletado
    products = list_products(db)
    assert all(product.id != p.id for product in products)
