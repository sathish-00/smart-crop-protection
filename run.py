# smart-crop-protection/run.py
from backend import create_app
from backend.config import DevelopmentConfig

# 1. Calls the application factory function defined in backend/__init__.py
app = create_app(config_object=DevelopmentConfig)

if __name__ == '__main__':
    # 2. Runs the application. Since debug=True is set in config, 
    #    Flask will start the development server.
    app.run(debug=True)