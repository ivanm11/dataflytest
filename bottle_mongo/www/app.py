from bottle import Bottle

app = Bottle()

@app.get('/')
def index():
    return 'Bottle & Mongo project'

if __name__ == "__main__":
    app.run(host='localhost', port=8080, debug=True, reloader=True)