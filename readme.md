# Integración de etcd con FastAPI para Configuración Distribuida en Sistemas Modernos

## Introducción

En el desarrollo de software moderno, sobre todo en entornos de microservicios, la gestión centralizada de configuraciones y la coordinación de servicios son claves para garantizar la escalabilidad y resiliencia de las aplicaciones. **etcd** es una base de datos clave-valor distribuida, altamente disponible, ideal para almacenar configuraciones, realizar descubrimiento de servicios y sincronizar datos en entornos productivos. En este artículo, exploraremos cómo integrar **etcd** con **FastAPI** para lograr una gestión eficiente y centralizada de configuraciones.

## ¿Qué es etcd?

**etcd** es un almacén de claves y valores distribuido, desarrollado originalmente por CoreOS y actualmente bajo la tutela de CNCF (Cloud Native Computing Foundation). Es ampliamente utilizado para:

- Almacenamiento de configuraciones distribuidas.
- Descubrimiento y coordinación de servicios en sistemas distribuidos.
- Gestión de clústeres en Kubernetes.
- Implementación de bloqueos distribuidos y semáforos para sincronización concurrente.

## Instalación de etcd

Antes de integrar **etcd** con **FastAPI**, es necesario instalar y ejecutar **etcd**. Para quienes trabajen con **Docker**, pueden lanzar el servicio con el siguiente comando:

```sh
docker run -p 2379:2379 --name etcd \
    quay.io/coreos/etcd \
    etcd --advertise-client-urls http://0.0.0.0:2379 \
         --listen-client-urls http://0.0.0.0:2379
```

Esto inicia **etcd** en el puerto `2379`, que será el punto de entrada para nuestras operaciones.

## Integración de etcd con FastAPI

### Instalación de la librería etcd3

Para interactuar con **etcd** desde Python, utilizaremos la librería `etcd3`. Su instalación se realiza con:

```sh
pip install etcd3
```

### Conectando FastAPI con etcd

A continuación, implementamos un servicio **FastAPI** que permite obtener y registrar configuraciones en **etcd**.

```python
from fastapi import FastAPI
import etcd3

app = FastAPI()
etcd = etcd3.client(host='localhost', port=2379)

@app.get("/config/{key}")
def get_config(key: str):
    value, _ = etcd.get(key)
    if value:
        return {"key": key, "value": value.decode("utf-8")}
    return {"error": "Clave no encontrada"}

@app.post("/config/{key}")
def set_config(key: str, value: str):
    etcd.put(key, value)
    return {"mensaje": f"Configuración {key} registrada correctamente"}
```

### Prueba de la Aplicación

Ejecutamos el servidor FastAPI con:

```sh
uvicorn main:app --reload
```

Ahora, podemos probar los endpoints utilizando **curl** o herramientas como **Postman**:

1. **Registrar una configuración:**
   ```sh
   curl -X POST "http://127.0.0.1:8000/config/database_url" -H "Content-Type: application/json" -d '"postgres://usuario:password@localhost:5432/basededatos"'
   ```

2. **Obtener la configuración registrada:**
   ```sh
   curl -X GET "http://127.0.0.1:8000/config/database_url"
   ```

Esto devolverá la URL de la base de datos almacenada en etcd, permitiendo su acceso centralizado por los servicios que la requieran.

## Casos de Uso en Sistemas Productivos

- **Gestión centralizada de configuraciones:** Los servicios pueden recuperar sus configuraciones dinámicamente desde **etcd**, eliminando la necesidad de archivos locales o variables de entorno fijas.
- **Descubrimiento de servicios dinámico:** Los microservicios pueden registrarse y ser descubiertos en tiempo de ejecución sin necesidad de reiniciar instancias.
- **Coordinación de límites de concurrencia y accesos:** Se pueden definir reglas distribuidas para la gestión de accesos, control de rate limiting y sincronización de procesos en múltiples instancias.

## Conclusión

La integración de **etcd** con **FastAPI** permite crear sistemas escalables y resilientes, con una configuración centralizada y adaptable a cambios en tiempo real sin reinicios innecesarios. Este enfoque es clave en arquitecturas de microservicios y entornos cloud-native, donde la flexibilidad y la alta disponibilidad son esenciales para un correcto funcionamiento.

