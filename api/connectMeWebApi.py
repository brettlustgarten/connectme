from flask_api import FlaskAPI
from flask import request

app = FlaskAPI(__name__)

@app.route('/api/connectme/new_user', methods=["GET", "POST"])
def get_new_user_data():
    return {'request data': request.data}
	
@app.route('/api/connectme/parsed_user_data', methods=["GET", "POST"])
def parse_user():
    return {'request data': request.data}
	
if __name__ == "__main__":
    app.run(debug=True)
