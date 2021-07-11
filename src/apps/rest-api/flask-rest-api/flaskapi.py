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

@app.route('/PIDConfig', methods=['GET'])
def PIDConfig():
    try:
        path = "/home/pi/sample2/src/apps/static/config/caring-service/config.json"
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
                
        output = config["pid"]
    except Exception as exception:
        output = "ERROR: " + str(exception)
    finally:
        return jsonify({'PIDConfig': output})
    

@app.route('/heaterConfig', methods=['GET'])
def heaterConfig():
    try:
        path = "/home/pi/sample2/src/apps/static/config/caring-service/config.json"
        with open(path) as f:
            config = json.load(f)
            
        args = request.args
        if args:
            args = jsonify(args)
            for key in args.json:
                if key in config ["heater"]:
                    config ["heater"][key] = float(args.json[key])

            config = json.dumps(config, indent=4)
            
            with open(path, "w") as f:
                f.write(config)
                config = json.loads(config)
                
        output = config["heater"]
    except Exception as exception:
        output = "ERROR: " + str(exception)
    finally:
        return jsonify({'heaterConfig': output})
    
@app.route('/lampsConfig', methods=['GET'])
def lampsConfig():
    try:
        path = "/home/pi/sample2/src/apps/static/config/caring-service/config.json"
        with open(path) as f:
            config = json.load(f)
            
        args = request.args
        if args:
            args = jsonify(args)
            for key in args.json:
                if key in config ["lamps"]:
                    config ["lamps"][key] = float(args.json[key])

            config = json.dumps(config, indent=4)
            
            with open(path, "w") as f:
                f.write(config)
                config = json.loads(config)
                
        output = config["lamps"]
    except Exception as exception:
        output = "ERROR: " + str(exception)
    finally:
        return jsonify({'lampsConfig': output})

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)

