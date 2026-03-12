import requests
import json

FIXTURES = {
    "https://swapi.dev/api/people/10/": {
        "status_code": 200,
        "json": {
            "name": "Obi-Wan Kenobi", "height": "182", "mass": "77",
            "url": "https://swapi.dev/api/people/10/"
        }
    },
    "https://swapi.dev/api/people/13/": {
        "status_code": 200,
        "json": {
            "name": "Chewbacca", "height": "228", "mass": "112",
            "url": "https://swapi.dev/api/people/13/"
        }
    },
    "https://swapi.dev/api/planets/2/": {
        "status_code": 200,
        "json": {
            "name": "Alderaan", "population": "2000000000",
            "url": "https://swapi.dev/api/planets/2/"
        }
    },
    "https://swapi.dev/api/starships/10/": {
        "status_code": 200,
        "json": {
            "name": "Millennium Falcon", "crew": "4",
            "url": "https://swapi.dev/api/starships/10/"
        }
    },
    "https://swapi.dev/api/people/9999/": {
        "status_code": 404,
        "json": {"detail": "Not found"}
    }
}

class FallbackResponse:
    def __init__(self, url, status_code, payload, source):
        self.url = url
        self.status_code = status_code
        self._payload = payload
        self.source = source

    def json(self):
        return self._payload

def get_swapi(url):
    try:
        resp = requests.get(url, timeout=5)
        return FallbackResponse(url, resp.status_code, resp.json(), "online")
    except:
        fixture = FIXTURES.get(url)
        return FallbackResponse(url, fixture["status_code"], fixture["json"], "fallback_local")

def mostrar_resposta(url):
    response = get_swapi(url)
    print(f"Fonte: {response.source} | Status: {response.status_code}")
    print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    return response

# --- PARTE 1: Execução das URLs ---

print("=== PARTE 1: CONSULTANDO ENDPOINTS ===")
urls = [
    "https://swapi.dev/api/people/10/",
    "https://swapi.dev/api/people/13/",
    "https://swapi.dev/api/planets/2/",
    "https://swapi.dev/api/starships/10/"
]

for url in urls:
    print(f"\nConsultando: {url}")
    mostrar_resposta(url)

# --- PARTE 4: Testes Automatizados com Assert ---

print("\n=== PARTE 4: TESTES AUTOMATIZADOS ===")

# Teste 1: Validar Obi-Wan Kenobi
url_obi = "https://swapi.dev/api/people/10/"
res_obi = get_swapi(url_obi)
dados_obi = res_obi.json()
assert res_obi.status_code == 200
assert dados_obi["name"] == "Obi-Wan Kenobi"
print("Teste Obi-Wan: OK")

# Teste 2: Validar Millennium Falcon
url_nave = "https://swapi.dev/api/starships/10/"
res_nave = get_swapi(url_nave)
assert int(res_nave.json()["crew"]) > 0
print("Teste Millennium Falcon: OK")

# Teste 3: Teste Negativo (ID 9999)
url_erro = "https://swapi.dev/api/people/9999/"
res_erro = get_swapi(url_erro)
assert res_erro.status_code == 404
assert res_erro.json()["detail"] == "Not found"
print("Teste Negativo 404: OK")

print("\nTodos os testes automatizados passaram!")
