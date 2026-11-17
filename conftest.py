import os
import re
from datetime import datetime

import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.logger import crear_logger

log = crear_logger("conftest")


def pytest_addoption(parser):
    # Permite correr con: pytest --headless (sin abrir la ventana del navegador)
    parser.addoption(
        "--headless", action="store_true", default=False,
        help="Ejecuta Chrome sin interfaz grafica"
    )


@pytest.fixture
def driver(request):
    opciones = Options()
    if request.config.getoption("--headless"):
        opciones.add_argument("--headless=new")
        opciones.add_argument("--no-sandbox")
    opciones.add_argument("--window-size=1920,1080")

    # Desactivo los popups de Chrome que pregunta si quiero guardar contraseñas
    opciones.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })

    log.info(f"Iniciando navegador para el test: {request.node.name}")
    driver = webdriver.Chrome(options=opciones)
    yield driver

    log.info("Cerrando navegador")
    driver.quit()


@pytest.fixture
def inventario(driver):
    # Hace login con standard_user y devuelve la pagina de productos
    login = LoginPage(driver)
    login.abrir_pagina()
    login.hacer_login("standard_user", "secret_sauce")
    pagina = InventoryPage(driver)
    assert pagina.obtener_titulo() == "Products"
    return pagina


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    #Si un test de UI falla: saco screenshot, lo guardo y lo agrego al reporte
    outcome = yield
    reporte = outcome.get_result()

    if reporte.when == "call" and reporte.failed:
        driver = item.funcargs.get("driver")  # los tests de API no tienen driver
        if driver is not None:
            fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_test = re.sub(r"[^\w\-]", "_", item.name)
            ruta = os.path.join("screenshots", f"{fecha_hora}_{nombre_test}.png")

            os.makedirs("screenshots", exist_ok=True)
            driver.save_screenshot(ruta)
            log.error(f"Test fallido: {item.name}. Screenshot guardado en {ruta}")

            # Tambien lo incluyo dentro del reporte HTML
            extras = getattr(reporte, "extras", [])
            extras.append(pytest_html.extras.png(driver.get_screenshot_as_base64()))
            reporte.extras = extras
