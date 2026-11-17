import pytest

from utils.datos import leer_json

pytestmark = pytest.mark.ui

productos_esperados = leer_json("datos/productos.json")


def test_catalogo_muestra_seis_productos(inventario):
    assert inventario.cantidad_productos() == 6


@pytest.mark.parametrize("producto", productos_esperados)
def test_producto_esta_en_el_catalogo(inventario, producto):
    assert producto in inventario.obtener_nombres()


def test_ordenar_por_precio_de_menor_a_mayor(inventario):
    inventario.ordenar_por("lohi")

    precios = inventario.obtener_precios()
    assert precios == sorted(precios)
