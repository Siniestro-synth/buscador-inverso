import json
from pathlib import Path

# Datos simulados de departamentos a refaccionar
departamentos = [
    {
        "ciudad": "Buenos Aires",
        "direccion": "Av. Corrientes 2345",
        "estado": "A refaccionar",
        "precio": "USD 45.000",
        "m2": 40,
        "imagen": "https://via.placeholder.com/300x200?text=Depto+Corrientes",
        "url": "https://www.zonaprop.com.ar/departamento-av-corrientes-2345.html"
    },
    {
        "ciudad": "Buenos Aires",
        "direccion": "Callao 1200",
        "estado": "A reciclar",
        "precio": "USD 50.000",
        "m2": 55,
        "imagen": "https://via.placeholder.com/300x200?text=Depto+Callao",
        "url": "https://www.argenprop.com/departamento-callao-1200.html"
    },
    {
        "ciudad": "La Plata",
        "direccion": "Diagonal 80 y 47",
        "estado": "A refaccionar",
        "precio": "USD 38.500",
        "m2": 45,
        "imagen": "https://via.placeholder.com/300x200?text=Depto+La+Plata",
        "url": "https://www.mercadolibre.com.ar/departamento-la-plata-diag-80"
    }
]

# Guardar archivo JSON
json_path = Path("/mnt/data/departamentos.json")
json_path.write_text(json.dumps(departamentos, indent=2), encoding="utf-8")

json_path.name
