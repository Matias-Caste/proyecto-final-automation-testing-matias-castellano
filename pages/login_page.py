from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config import BASE_URL


class LoginPage(BasePage):
    # Locators de la pagina de login
    CAMPO_USUARIO = (By.ID, "user-name")
    CAMPO_PASSWORD = (By.ID, "password")
    BOTON_LOGIN = (By.ID, "login-button")
    MENSAJE_ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def abrir_pagina(self):
        self.abrir(BASE_URL)

    def hacer_login(self, usuario, password):
        self.log.info(f"Intentando login con el usuario '{usuario}'")
        self.escribir(self.CAMPO_USUARIO, usuario)
        self.escribir(self.CAMPO_PASSWORD, password)
        self.hacer_click(self.BOTON_LOGIN)

    def obtener_error(self):
        return self.obtener_texto(self.MENSAJE_ERROR)
