#Check it out online
http://cs2102.ymichael.com/

#Read our report
https://docs.google.com/document/d/1S7favUB12Mqybnwc5R3nzxfr3QFllD7kojeCnjVlL3s/edit?usp=sharing

# Install Dependencies
- `$ pip install -r requirements.txt`

# Running application
## In production
- `$ FLASK_ENV=prod python app.py`
- Go to `http://localhost:5000`

## In development
- `$ FLASK_ENV=dev python app.py` or `python app.py`
- Go to `http://localhost:5000`

# Running Tests
- `$ nosetests`

# Writing Tests
- See `tests/__init__.py` for base class or function decorator to use for preparing tests
