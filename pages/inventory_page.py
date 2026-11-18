from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InventoryPage(BasePage):
    # Locators de la pagina de productos
    TITULO = (By.CLASS_NAME, "title")
    PRODUCTOS = (By.CLASS_NAME, "inventory_item")
    NOMBRES = (By.CLASS_NAME, "inventory_item_name")
    PRECIOS = (By.CLASS_NAME, "inventory_item_price")
    SELECTOR_ORDEN = (By.CLASS_NAME, "product_sort_container")
    BADGE_CARRITO = (By.CLASS_NAME, "shopping_cart_badge")
    ICONO_CARRITO = (By.CLASS_NAME, "shopping_cart_link")
    BOTON_MENU = (By.ID, "react-burger-menu-btn")
    LINK_LOGOUT = (By.ID, "logout_sidebar_link")

    def obtener_titulo(self):
        return self.obtener_texto(self.TITULO)

    def cantidad_productos(self):
        return len(self.obtener_elementos(self.PRODUCTOS))

    def obtener_nombres(self):
        return [p.text for p in self.obtener_elementos(self.NOMBRES)]

    def obtener_precios(self):
        # Los precios vienen como "$29.99", les saco el $ y los paso a numero
        precios = self.obtener_elementos(self.PRECIOS)
        return [float(p.text.replace("$", "")) for p in precios]

    def ordenar_por(self, valor):
        # Valores posibles: az, za, lohi, hilo
        self.log.info(f"Ordenando productos por '{valor}'")
        Select(self.driver.find_element(*self.SELECTOR_ORDEN)).select_by_value(valor)

    def _boton_del_producto(self, nombre):
        # Busca el boton (Add to cart / Remove) que esta dentro del producto
        xpath = (
            f"//div[text()='{nombre}']"
            "/ancestor::div[@class='inventory_item']//button"
        )
        return (By.XPATH, xpath)

    def agregar_producto(self, nombre):
        self.log.info(f"Agregando al carrito: {nombre}")
        self.hacer_click(self._boton_del_producto(nombre))
        # espero a que aparezca el numerito del carrito antes de seguir
        self.wait.until(EC.visibility_of_element_located(self.BADGE_CARRITO))

    def quitar_producto(self, nombre):
        self.log.info(f"Quitando del carrito: {nombre}")
        self.hacer_click(self._boton_del_producto(nombre))

    def cantidad_en_carrito(self):
        # Si no hay productos el numerito (badge) no aparece
        badges = self.obtener_elementos(self.BADGE_CARRITO)
        if len(badges) == 0:
            return 0
        return int(badges[0].text)

    def ir_al_carrito(self):
        self.hacer_click(self.ICONO_CARRITO)
        # Espero a que cargue el carrito (con la URL sola no alcanzaba)
        self.wait.until(EC.text_to_be_present_in_element(self.TITULO, "Your Cart"))

    def cerrar_sesion(self):
        self.hacer_click(self.BOTON_MENU)
        self.hacer_click(self.LINK_LOGOUT)
