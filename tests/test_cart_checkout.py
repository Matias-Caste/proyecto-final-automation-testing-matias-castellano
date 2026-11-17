import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.datos import leer_json

pytestmark = pytest.mark.ui

PRODUCTO = "Sauce Labs Backpack"
datos_checkout = leer_json("datos/checkout.json")


def test_agregar_producto_al_carrito(inventario, driver):
    inventario.agregar_producto(PRODUCTO)
    assert inventario.cantidad_en_carrito() == 1

    inventario.ir_al_carrito()
    carrito = CartPage(driver)
    assert PRODUCTO in carrito.obtener_nombres()


def test_quitar_producto_del_carrito(inventario, driver):
    inventario.agregar_producto(PRODUCTO)
    inventario.ir_al_carrito()

    carrito = CartPage(driver)
    assert carrito.cantidad_items() == 1
    carrito.quitar_primer_producto()
    assert carrito.cantidad_items() == 0


@pytest.mark.parametrize(
    "datos", datos_checkout, ids=lambda d: d["nombre"]
)
def test_checkout_completo(inventario, driver, datos):
    # Flujo completo: producto -> carrito -> datos -> finalizar compra
    inventario.agregar_producto(PRODUCTO)
    inventario.ir_al_carrito()

    carrito = CartPage(driver)
    carrito.ir_a_checkout()

    checkout = CheckoutPage(driver)
    checkout.completar_datos(
        datos["nombre"], datos["apellido"], datos["codigo_postal"]
    )
    checkout.finalizar_compra()

    assert "Thank you for your order" in checkout.obtener_mensaje_exito()


@pytest.mark.negativo
def test_checkout_sin_completar_datos(inventario, driver):
    inventario.agregar_producto(PRODUCTO)
    inventario.ir_al_carrito()
    CartPage(driver).ir_a_checkout()

    checkout = CheckoutPage(driver)
    checkout.completar_datos("", "", "")

    assert "First Name is required" in checkout.obtener_error()
