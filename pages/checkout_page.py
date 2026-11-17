from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    # Locators del checkout
    CAMPO_NOMBRE = (By.ID, "first-name")
    CAMPO_APELLIDO = (By.ID, "last-name")
    CAMPO_CODIGO_POSTAL = (By.ID, "postal-code")
    BOTON_CONTINUAR = (By.ID, "continue")
    BOTON_FINALIZAR = (By.ID, "finish")
    MENSAJE_EXITO = (By.CLASS_NAME, "complete-header")
    MENSAJE_ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def completar_datos(self, nombre, apellido, codigo_postal):
        self.log.info(f"Completando datos de envio para {nombre} {apellido}")
        self.escribir(self.CAMPO_NOMBRE, nombre)
        self.escribir(self.CAMPO_APELLIDO, apellido)
        self.escribir(self.CAMPO_CODIGO_POSTAL, codigo_postal)
        self.hacer_click(self.BOTON_CONTINUAR)

    def finalizar_compra(self):
        self.hacer_click(self.BOTON_FINALIZAR)

    def obtener_mensaje_exito(self):
        return self.obtener_texto(self.MENSAJE_EXITO)

    def obtener_error(self):
        return self.obtener_texto(self.MENSAJE_ERROR)
