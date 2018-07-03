from flask import Flask, request
import os
import sys
import json
import socket
import numpy
app = Flask(__name__)
coun=0

@app.route('/ping')
def ping():
    return 'pinged'

@app.route('/initialize/<config_file_name>&<config_file_path>')
def initialize(config_file_name, config_file_path):
    print("===The configuration file={!s}".format(config_file_path))
    return 'Server initialize...'

@app.route('/dostep/<time>&<inputnames>&<inputvalues>&<outputnames>')
def step(time, inputnames, inputvalues, outputnames):
    #data = _parse_url(time, inputnames, inputvalues, outputnames)
    global coun
    #outputs = [data['u'] * coun
    #           for i in range(0, len(data['outputnames']))]
    coun+=1
    return str('1.0')


def _parse_url(time, inputnames, inputvalues, outputnames):
    """
    Ensure that inputs has the right type
    """

    data = {str(key):eval(str(value))
            for key, value in
            zip(inputnames.split(','), inputvalues.split(','))}
    data['time'] = float(time)
    data['outputnames'] = outputnames.split(',')
    return data

@app.errorhandler(Exception)
def handle_error(e):
    """
    Handle error message back to the FMU
    """
    return 'ERROR: ' + str(e)


@app.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

if __name__ == '__main__':
    # Open the right port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 0))  # Get a free port at random with '0'
    address, port = sock.getsockname()  # Retrieve the port and address
    sock.close()  # Close the socket and use the port with Flask

    # Write a file with port and address
    path_to_server = sys.argv[1]

    str_ser = """def main():
    import urllib2
    try:
        response = urllib2.urlopen("http://localhost:""" + str(port) + """/ping").read()
        response = response.decode('utf-8')
    except:
        response = 'bad request'
    if response in 'pinged':
        print('The Server is up')
        return 0
    else:
        print('The server is not up yet')
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(main())

"""
#     str_ser='''def main():
#     import socket
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     result = sock.connect_ex(('localhost', '''+str(port)+'''))
#     if result == 0:
#         return 0
#     else:
#         return 1
#
#     # etc.
# if __name__ == '__main__':
#     import sys
#     sys.exit(main())
#     '''
    # Write a file which allows checking if the server is up
    with open(path_to_server + "check_server.py", "w") as config1:
        config1.write(str_ser)
    # Write te configuration file for connecting to the server
    with open(path_to_server + "server_config.txt", "w") as config2:
        config2.write('address' + ':' + 'localhost' + ':' + 'port' + ':' + str(port) + ':')
    # Start the server
    app.run(port=port, debug=True, use_reloader=False, threaded=True)
