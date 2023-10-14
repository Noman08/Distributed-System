from bottle import Bottle, run, template, error, get, post, request, static_file

app = Bottle()

@app.route("/")
def root():
	return static_file("links.html","./")

@app.route("/hello")
@app.route("/hello/<name>")
def hello(name="unknown"):
	return "<b>Faiz Ahmed</b>"


@app.get("/input")
def input_get():
	return static_file("input.html","./")

@app.post("/input")
def show_data():
	first_name = request.forms.get("first_name")
	last_name = request.forms.get("last_name")
	return template("<p>First Name:{{first_name}} <br/> Last name: {{last_name}}",first_name = first_name, last_name = last_name)


@error(404)
def error404(error):
    return 'Nothing here, sorry'

run(app,host='localhost', port=8080, debug=True,reloader=True)