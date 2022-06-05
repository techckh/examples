from .config import create_app

# uvicorn main:app  --reload --host 0.0.0.0 --port 8000
app = create_app()
