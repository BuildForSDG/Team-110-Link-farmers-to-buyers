''' Run app module'''

from routes import *

if __name__ == "__main__":
    app.run(port=1234, debug=True)
