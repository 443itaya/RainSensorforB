from flask import Flask, jsonify, abort, make_response
import csv
import time


api = Flask(__name__)


@api.route('/get', methods=['GET'])
def get():
    file = open('rainInfo.csv', 'r')
    flag = file.read()
    file.close()
    print(flag)
    # time.sleep(1)
    if flag == "1\n":
        result = {'weather': 'rain'}
    elif flag == "0\n":
        result = {'weather': 'norain'}
    
    return make_response(jsonify(result))

@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    api.run(host='192.168.1.31', port=3001)
