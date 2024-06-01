import uvicorn
from main import app

uvicorn.run(app, port=5000, host="0.0.0.0")
