# Proxy API LLM - Proyecto SCADA

Este repositorio contiene la Capa de Procesamiento (Middleware) del sistema de detección semántica para SCADA. Funciona como un Proxy API construido en FastAPI que sirve de puente entre el Frontend del usuario y los modelos de Inteligencia Artificial (Qwen 2.5 Coder vía Ollama).

## Arquitectura del Sistema

El proyecto forma parte de una arquitectura de 3 capas conectada a través de ZeroTier:
1. Frontend (Puerto 8000): Interfaz visual (Node.js/React).
2. Clasificador SCADA (Puerto 8001): Modelo SVM + TF-IDF para filtrado y análisis semántico.
3. Proxy API (Este repositorio - Puerto 8002): Orquestador de solicitudes y generador de respuestas mediante LLM.

## Requisitos

- Python 3.10+
- Ollama ejecutándose localmente con el modelo qwen2.5-coder:1.5b.

## Instalación y Ejecución

1. Crear y activar el entorno virtual:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

2. Instalar dependencias:
   ```powershell
   pip install fastapi uvicorn httpx
   ```

3. Ejecutar el servidor (Obligatorio en 0.0.0.0 para acceso por ZeroTier):
   ```powershell
   uvicorn app.main:app --host 0.0.0.0 --port 8002
   ```

## Endpoints Principales

- POST /chat: Recibe un payload JSON con {"prompt": "..."} y genera la respuesta mediante Ollama.
- GET /dashboard: Interfaz web nativa del servidor para monitoreo y pruebas del proxy.
- GET /health: Endpoint de estado. Devuelve "Ollama is running" para compatibilidad con paneles de control.

## Configuración CORS
El middleware está configurado de forma abierta (allow_origins=["*"]) para permitir la comunicación sin bloqueos desde el servidor Frontend o clientes ZeroTier.
