#!/usr/bin/python3
from app import app

app.debug=True

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8888)
