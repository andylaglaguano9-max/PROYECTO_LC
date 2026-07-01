import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse

app = FastAPI(title="Mistral Proxy API", description="Proxy compatible con middleware", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    html_content = """
    <html>
        <head>
            <title>Mistral Proxy</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; text-align: center; padding-top: 10vh; }
                h1 { color: #38bdf8; font-size: 3rem; margin-bottom: 10px; }
                p { font-size: 1.2rem; color: #94a3b8; }
                .status { background-color: #1e293b; padding: 40px; border-radius: 15px; display: inline-block; box-shadow: 0 10px 25px rgba(0,0,0,0.5); border: 1px solid #334155; }
                .badge { background-color: #10b981; color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 0.9rem; }
            </style>
        </head>
        <body>
            <div class="status">
                <h1>🚀 AI Proxy Server</h1>
                <p>Tu servidor de Inteligencia Artificial está en línea.</p>
                <div style="margin: 20px 0;"><span class="badge">ONLINE (ZeroTier Ready)</span></div>
                <p style="font-size: 0.9rem; color: #64748b;">Endpoint activo: <code>POST /chat</code></p>
                <p style="font-size: 0.9rem; color: #64748b;">Modelo en uso: <code>qwen2.5-coder:1.5b</code></p>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/metrics")
def get_metrics():
    # Retornamos métricas simuladas (mock) para el frontend de Scada IA
    return {
        "accuracy": 0.92,
        "precision": 0.89,
        "recall": 0.94,
        "f1_score": 0.91
    }

# Agregamos GET para que no dé error cuando abran el enlace en el navegador
@app.get("/chat")
def chat_browser_test():
    return {"response": "Mistral Proxy funcionando perfectamente. Usa un método POST para enviar tus prompts."}

@app.post("/chat")
async def chat_endpoint(request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
        
    prompt = data.get("prompt", "")
    
    # Adaptador para la API /api/generate de Ollama
    # Usaremos el modelo 'mistral' base (Q4) que pesa ~4GB para evitar el error de Memoria RAM
    payload = {
        "model": "qwen2.5-coder:1.5b",
        "prompt": prompt,
        "stream": False,
        "keep_alive": -1
    }
        
    async with httpx.AsyncClient() as client:
        try:
            # Quitamos el timeout de 5.0 y le damos hasta 10 minutos (600.0)
            response = await client.post("http://127.0.0.1:11434/api/generate", json=payload, timeout=600.0)
            
            if response.status_code == 200:
                return JSONResponse(status_code=200, content=response.json())
            else:
                return JSONResponse(status_code=response.status_code, content={"message": "Error from Ollama"})
        except httpx.ReadTimeout:
            return JSONResponse(status_code=200, content={"response": "Mistral está pensando, pero tardó más de 10 minutos. Intenta un prompt más corto."})
        except httpx.RequestError as e:
            return JSONResponse(status_code=500, content={"message": f"Error conectando con Ollama: {str(e)}"})
