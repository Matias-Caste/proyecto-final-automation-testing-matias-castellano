# Proyecto Final - Automation Testing

Autor: Matias Castellano

## De qué trata

Este es mi proyecto final del curso de Automation Testing. Armé un framework de pruebas con Python y Pytest que prueba dos cosas:

- La página [saucedemo.com](https://www.saucedemo.com/) con Selenium (login, productos, carrito y checkout).
- La API [JSONPlaceholder](https://jsonplaceholder.typicode.com/) con Requests (GET, POST y DELETE).

Cuando termina de correr genera un reporte en HTML. Si falla algún test de la web, saca una captura de pantalla y la agrega al reporte.

## Tecnologías

- Python
- Pytest y pytest-html
- Selenium WebDriver (con Chrome)
- Requests
- Git y GitHub
- GitHub Actions

## Estructura

- `pages/`: las clases del Page Object Model (una por cada página: login, productos, carrito y checkout, más una clase base).
- `tests/`: los tests de UI (`test_login`, `test_inventory`, `test_cart_checkout`) y los de API (`test_api`).
- `utils/`: configuración de URLs, lectura de CSV/JSON y el logger.
- `datos/`: archivos CSV y JSON con los datos de prueba.
- `reports/`: el reporte HTML y los logs (se crean solos al correr).
- `screenshots/`: capturas de los tests que fallan.
- `conftest.py`: el fixture del navegador y la captura de pantalla cuando falla un test.
- `.github/workflows/tests.yml`: para correr los tests en GitHub Actions.

## Cómo instalar

Hace falta tener Python y Chrome instalados.

```
git clone https://github.com/Matias-Caste/proyecto-final-automation-testing-matias-castellano.git
cd proyecto-final-automation-testing-matias-castellano
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Cómo correr los tests

```
pytest
```

Otras formas:

```
pytest --headless
pytest -m ui
pytest -m api
pytest -m negativo
```

- `--headless`: corre sin abrir el navegador.
- `-m ui`: solo los tests de la web.
- `-m api`: solo los tests de la API.
- `-m negativo`: solo los casos negativos.

## Cómo leer los reportes

- Al terminar se crea `reports/reporte.html`. Se abre con cualquier navegador y muestra qué tests pasaron y cuáles fallaron, con lo que tardó cada uno. En los que fallan se puede ver el error y la captura.
- En `reports/` también queda un archivo `.log` con los pasos que fue haciendo cada test, que sirve para ver dónde se rompió.
- Las capturas también se guardan en `screenshots/`, con la fecha, la hora y el nombre del test en el nombre del archivo.

## GitHub Actions

Cada vez que hago push se ejecutan los tests solos y el reporte queda guardado como artefacto de la ejecución.
- En 'reports/' también queda un archivo '.log' con los pasos que fue haciendo cada test, que sirve para ver dónde se rompió.
- Las capturas también se guardan en 'screenshots/', con la fecha, la hora y el nombre del test en el nombre del archivo.

## GitHub Actions

Cada vez que hago push se ejecutan los tests solos y el reporte queda guardado como artefacto de la ejecución.
