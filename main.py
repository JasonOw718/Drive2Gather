from app import create_app
import sys, os
from flask_debugtoolbar import DebugToolbarExtension 
import create_db

sys.path.append(os.getcwd())
app = create_app()

app.debug = True
toolbar = DebugToolbarExtension(app)

if __name__ == '__main__': 
    app.run(debug=True)
