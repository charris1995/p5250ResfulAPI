from cgitb import reset
from flask import Flask, request, session
import AS400API

app = Flask(__name__)
ibm = AS400API.p5250WebAPI()

sessions = {}

@app.route('/Connect')
def TestConnection():
    result = None
    sessionName = request.args.get("SessionName")
    sessionName = str(hash(sessionName))
    if sessionName in sessions.keys():
        return "Session Exists"
    else:
        sessions[sessionName] = AS400API.p5250WebAPI()
    
    ibm = sessions[sessionName]
    isConnected = ibm.my_client.connect()
    if(isConnected):
        return sessionName
    return "Connection Failed"


@app.route("/Disconnect")
def disconnect():
    sessionName = request.args.get("SessionName")
    ibm = sessions[sessionName]
    ibm.my_client.endSession()
    ibm.my_client.disconnect()
    sessions[sessionName] = None
    del sessions[sessionName]
    return "Disconnected"

@app.route('/GoToLine')
def goToLine():
    sessionName = request.args.get("SessionName")
    ibm = sessions[sessionName]
    x = int(request.args.get('X'))
    y = int(request.args.get('Y'))
    
    ibm.my_client.moveTo(x,y)
    result = ibm.my_client.getScreen()
    return result


@app.route('/SendText')
def SendText():
    sessionName = request.args.get("SessionName")
    ibm = sessions[sessionName]
    text = request.args.get("Text")
    ibm.my_client.sendText(text)
    return ibm.my_client.getScreen()

@app.route('/SendEnter')
def SendEnter():
    sessionName = request.args.get("SessionName")
    ibm = sessions[sessionName]
    ibm.my_client.sendEnter()
    return ibm.my_client.getScreen()

@app.route('/SendFunction')
def SendFunction():
    sessionName = request.args.get("SessionName")
    fn = request.args.get("function")
    ibm = sessions[sessionName]
    ibm.my_client.sendF(int(fn))
    return ibm.my_client.getScreen()


@app.route('/GetRow')
def GetRow():
    sessionName = request.args.get("SessionName")
    x = int(request.args.get('X'))
    y = int(request.args.get('Y'))
    length = int(request.args.get('length'))
    ibm = sessions[sessionName]
    result = ibm.my_client.readTextAtPosition(x, y, length)
    return result

@app.route('/NextPage')
def NextPage():
    sessionName = request.args.get("SessionName")
    ibm = sessions[sessionName]
    result = ibm.my_client.rollUp()
    return ibm.my_client.getScreen()


if __name__ =='__main__':
    app.run()