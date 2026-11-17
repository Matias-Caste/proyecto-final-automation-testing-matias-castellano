from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.logger import crear_logger


class BasePage:
    """Clase base con las acciones comunes que usan todas las paginas."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.log = crear_logger(self.__class__.__name__)

    def abrir(self, url):
        self.log.info(f"Abriendo la URL: {url}")
        self.driver.get(url)

    def escribir(self, locator, texto):
        self.log.info(f"Escribiendo '{texto}' en {locator}")
        campo = self.wait.until(EC.visibility_of_element_located(locator))
        campo.clear()
        campo.send_keys(texto)

    def hacer_click(self, locator):
        self.log.info(f"Click en {locator}")
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def obtener_texto(self, locator):
        elemento = self.wait.until(EC.visibility_of_element_located(locator))
        return elemento.text

    def obtener_elementos(self, locator):
        return self.driver.find_elements(*locator)
