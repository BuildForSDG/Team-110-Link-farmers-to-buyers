''' Run app module'''

from routes import *

if __name__ == "__main__":
    app.run(debug=True, port=1234)
