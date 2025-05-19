# iteso-bdnr-mongodb

A place to share mongodb app code

### Setup a python virtual env with python mongodb installed
```

# If pip is not present in you system
sudo apt update
sudo apt install python3-pip

# Install and activate virtual env (Linux/MacOS)
python3 -m pip install virtualenv
python3 -m venv ./venv
source ./venv/bin/activate

# Install and activate virtual env (Windows)
python3 -m pip install virtualenv
python3 -m venv ./venv
.\venv\Scripts\Activate.ps1

# Install project python requirements
pip install -r requirements.txt
```

### To run the API service
```
cd ./mongo
python -m uvicorn main:app --port 9100 --reload
```

### To load data
Ensure you have a running mongodb instance
i.e.:
```
docker run --name mongodb -d -p 27017:27017 mongo
```
## App.py

Con los contenedores de cada base de datos corriendo, y el ambiente virtual comunitario, podemos ejecutar app.py
