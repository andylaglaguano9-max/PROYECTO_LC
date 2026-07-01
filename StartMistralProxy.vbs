Set WshShell = CreateObject("WScript.Shell")
' Ejecutar el proxy FastAPI de forma completamente invisible usando pythonw
WshShell.Run "cmd.exe /c cd C:\Users\PC-MASTER\fastapi-users-crud & .\.venv\Scripts\pythonw.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8002", 0, False

' Esperar 10 segundos para darle tiempo a Ollama y al proxy de iniciar
WScript.Sleep 10000

' Enviar el ping de despertar para cargar el modelo en RAM permanentemente
WshShell.Run "cmd.exe /c C:\Users\PC-MASTER\fastapi-users-crud\.venv\Scripts\pythonw.exe -c ""import httpx; httpx.post('http://127.0.0.1:11434/api/generate', json={'model': 'qwen2.5-coder:1.5b', 'prompt': 'Despierta', 'keep_alive': -1, 'stream': False}, timeout=60.0)""", 0, False
