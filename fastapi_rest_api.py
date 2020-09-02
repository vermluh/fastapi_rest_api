import uvicorn
from config import Config
from app import create_app

app = create_app()

if __name__ == "__main__":
	uvicorn.run(app, host='0.0.0.0', port=Config.RUN_PORT)
