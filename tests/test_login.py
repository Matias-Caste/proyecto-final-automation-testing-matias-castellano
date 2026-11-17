import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.datos import leer_csv

pytestmark = pytest.mark.ui

usuarios_validos = leer_csv("datos/login_validos.csv")
usuarios_invalidos = leer_csv("datos/login_invalidos.csv")


@pytest.mark.parametrize("fila", usuarios_validos, ids=lambda f: f["usuario"])
def test_login_exitoso(driver, fila):
    login = LoginPage(driver)
    login.abrir_pagina()
    login.hacer_login(fila["usuario"], fila["password"])

    inventario = InventoryPage(driver)
    assert inventario.obtener_titulo() == "Products"
    assert "inventory.html" in driver.current_url


@pytest.mark.negativo
@pytest.mark.parametrize(
    "fila", usuarios_invalidos, ids=lambda f: f["usuario"] or "usuario_vacio"
)
def test_login_con_datos_invalidos(driver, fila):
    login = LoginPage(driver)
    login.abrir_pagina()
    login.hacer_login(fila["usuario"], fila["password"])

    mensaje = login.obtener_error()
    assert fila["mensaje_esperado"] in mensaje
    # Si el login fallo, tiene que seguir en la pagina de login
    assert "inventory.html" not in driver.current_url


def test_logout(inventario, driver):
    inventario.cerrar_sesion()

    login = LoginPage(driver)
    assert driver.current_url == "https://www.saucedemo.com/"
    assert driver.find_element(*login.BOTON_LOGIN).is_displayed()
