import pytest
import requests

from utils.config import API_URL
from utils.logger import crear_logger

pytestmark = pytest.mark.api

log = crear_logger("api")
TIMEOUT = 10  # segundos


def test_get_post_existente():
    log.info("GET /posts/1")
    respuesta = requests.get(f"{API_URL}/posts/1", timeout=TIMEOUT)

    assert respuesta.status_code == 200
    datos = respuesta.json()
    # Valido la estructura y el contenido
    for campo in ["userId", "id", "title", "body"]:
        assert campo in datos
    assert datos["id"] == 1


def test_get_lista_de_posts():
    log.info("GET /posts")
    respuesta = requests.get(f"{API_URL}/posts", timeout=TIMEOUT)

    assert respuesta.status_code == 200
    posts = respuesta.json()
    assert isinstance(posts, list)
    assert len(posts) == 100


@pytest.mark.negativo
def test_get_post_inexistente():
    log.info("GET /posts/9999 (no existe)")
    respuesta = requests.get(f"{API_URL}/posts/9999", timeout=TIMEOUT)

    assert respuesta.status_code == 404
    assert respuesta.json() == {}


def test_crear_post():
    log.info("POST /posts")
    nuevo_post = {"title": "Mi post de prueba", "body": "Contenido", "userId": 1}
    respuesta = requests.post(f"{API_URL}/posts", json=nuevo_post, timeout=TIMEOUT)

    assert respuesta.status_code == 201
    datos = respuesta.json()
    assert datos["title"] == nuevo_post["title"]
    assert datos["userId"] == 1
    assert "id" in datos


def test_eliminar_post():
    log.info("DELETE /posts/1")
    respuesta = requests.delete(f"{API_URL}/posts/1", timeout=TIMEOUT)

    assert respuesta.status_code == 200


def test_encadenado_usuario_y_sus_posts():
    # Paso 1: obtengo un usuario
    log.info("GET /users/1")
    respuesta_usuario = requests.get(f"{API_URL}/users/1", timeout=TIMEOUT)
    assert respuesta_usuario.status_code == 200
    id_usuario = respuesta_usuario.json()["id"]

    # Paso 2: uso el id del usuario para pedir sus posts
    log.info(f"GET /posts?userId={id_usuario}")
    respuesta_posts = requests.get(
        f"{API_URL}/posts", params={"userId": id_usuario}, timeout=TIMEOUT
    )
    assert respuesta_posts.status_code == 200
    posts = respuesta_posts.json()
    assert len(posts) > 0
    for post in posts:
        assert post["userId"] == id_usuario

    # Paso 3: creo un post nuevo para ese mismo usuario
    nuevo = {"title": "Post encadenado", "body": "Texto", "userId": id_usuario}
    respuesta_nuevo = requests.post(f"{API_URL}/posts", json=nuevo, timeout=TIMEOUT)
    assert respuesta_nuevo.status_code == 201
    assert respuesta_nuevo.json()["userId"] == id_usuario
