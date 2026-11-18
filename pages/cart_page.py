from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CartPage(BasePage):
    # Locators de la pagina del carrito
    # OJO: "inventory_item_name" tambien existe en la pagina de productos,
    # por eso lo busco solo dentro de .cart_item
    NOMBRES = (By.CSS_SELECTOR, ".cart_item .inventory_item_name")
    BOTON_CHECKOUT = (By.ID, "checkout")
    BOTON_QUITAR = (By.CSS_SELECTOR, ".cart_item button")

    def cantidad_items(self):
        return len(self.obtener_elementos(self.NOMBRES))

    def obtener_nombres(self):
        return [n.text for n in self.obtener_elementos(self.NOMBRES)]

    def quitar_primer_producto(self):
        self.log.info("Quitando el primer producto desde el carrito")
        self.hacer_click(self.BOTON_QUITAR)
        # espero a que el producto desaparezca de la lista
        self.wait.until(lambda d: len(d.find_elements(*self.NOMBRES)) == 0)

    def ir_a_checkout(self):
        self.hacer_click(self.BOTON_CHECKOUT)
        self.wait.until(EC.url_contains("checkout-step-one"))
