import uvicorn
from nursaryapp.main import app

uvicorn.run(app, port=5000, host="localhost")
