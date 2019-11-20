from flask_api import FlaskAPI
from flask import request, jsonify
from parse import parse_new_user_data

app = FlaskAPI(__name__)


# @app.route('/api/connectme/new_user', methods=["GET", "POST"])
# def get_new_user_data():
    # if request.method == "POST":
	
	# else:
	
    # return {'request data': request.data}
	
@app.route("/api/connectme/new_user", methods=["GET", "POST"])
def parse_user():
	if request.method == "POST":
		# print(request.data['photo'])
		if 'photo' in request.data:
			photoData = request.data['photo']
			# print(photoData)
			output = parse_new_user_data(photoData)
			# print(output)
			return jsonify({"output":output})
		else:
			return "Error: No photo field provided."
	else:
		return "Hello New User!"
    # return {'request data': request.data}
	
@app.route("/", methods=["GET", "POST"])
def hello():
    return "Hello from Python!"
	
if __name__ == "__main__":
    app.run(debug=True)
