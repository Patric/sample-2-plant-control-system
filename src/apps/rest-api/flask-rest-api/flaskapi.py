from flask import Flask
from flask import jsonify
from flask import request
import json

from sensors import Sensors


app = Flask(__name__)

@app.route("/")
def index():
    return "<html><body><h1>Sample2 REST API</h1></body></html>"

@app.route('/getSensorsValues', methods=['GET'])
def getSensorsValues():
    try:
        output = Sensors().getValues()
    except Exception as exception:
        output = "ERROR: " + str(exception)
    finally:
        return jsonify({'sensorValues': output})


@app.route('/lamps', methods=['GET'])
def turnOnLamps():
    try:
        on = request.args.get('on', type = str)
        if on == None: on = "false"
        output = bool(on)
    except Exception as exception:
        output = "ERROR: " + str(exception)
    finally:
        return jsonify({'lampsOn': output})

@app.route('/controlConfig', methods=['GET'])
def controlConfig():
    try:
        path = "/home/pi/sample2/src/apps/www-data/config/caring-service/config.json"
        with open(path) as f:
            config = json.load(f)
            
        args = request.args
        if args:
            args = jsonify(args)
            for key in args.json:
                if key in config ["pid"]:
                    config ["pid"][key] = float(args.json[key])

            config = json.dumps(config, indent=4)
          
            with open(path, "w") as f:
                f.write(config)
                config = json.loads(config)
                
        output = config
    except Exception as exception:
        output = "ERROR: " + str(exception)
    finally:
        return jsonify({'controlConfig': output})

@app.route('/getSample2ServiceLogs', methods=['GET'])
def getSample2ServiceLogs():
    try:
        max_length_in_chars = 100000
        max_length_arg = request.args.get('max_length', type = int)
        if max_length_arg:
            max_length_in_chars = max_length_arg

        path = "/home/pi/sample2/src/apps/www-data/logs/caring_system.log"
        with open(path) as f:
            content = f.read(max_length_in_chars).splitlines()
                
        output = content
    except Exception as exception:
        output = "ERROR: " + str(exception)
    finally:
        return output

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)

