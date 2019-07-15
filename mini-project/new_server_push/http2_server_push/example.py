from quart import make_response, Quart, render_template, url_for

app = Quart(__name__)

@app.route('/')
async def index():
    response = 'Hello, world'
    return response

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8080,
        certfile='cert.pem',
        keyfile='key.pem',
    )
