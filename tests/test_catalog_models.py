import pytest

from catalog.models import Category, Product


@pytest.mark.django_db
def test_product_str_and_slug():
    """Проверяет генерацию slug и __str__."""
    cat = Category.objects.create(name="Телефоны")
    p = Product.objects.create(title="iPhone X", category=cat, price=99999)
    assert str(p) == "iPhone X"
    assert p.slug is not None
