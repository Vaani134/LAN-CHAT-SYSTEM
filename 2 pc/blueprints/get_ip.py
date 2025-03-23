from flask import Flask, request

app = Flask(__name__)

@app.route('/get_ip')
def get_ip():
    # Try to get the real IP address if behind a proxy
    if request.headers.get('X-Forwarded-For'):
        ip_address = request.headers.get('X-Forwarded-For').split(',')[0]
    else:
        ip_address = request.remote_addr  # Direct IP address

    return f'Your IP address is: {ip_address}'

if __name__ == '__main__':
    app.run(debug=True, host='10.112.67.84')
