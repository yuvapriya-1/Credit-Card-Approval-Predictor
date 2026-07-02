from flask import Flask
from pyngrok import ngrok

app = Flask(__name__)

# This defines the "home" page
@app.route('/')
def home():
    return "<h1>Success! The Credit Card Project is connected.</h1><p>If you see this, your tunnel and server are working correctly.</p>"

if __name__ == '__main__':
    PORT = 5000
    # Start tunnel
    public_url = ngrok.connect(PORT)
    print(f" * Public URL: {public_url.public_url}")
    
    # Start app
    app.run(host='0.0.0.0', port=PORT)