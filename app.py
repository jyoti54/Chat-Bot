from flask import Flask,request,Response,jsonify
from flask_cors import CORS
from chat import response as chatBotResponse


app = Flask("__name__")
CORS(app)

@app.route("/", methods=['GET'])
def checkIfApiWorkingFine():
    return Response("This is the response from your chatbot api")

@app.route("/predict",methods=['POST'])
def getAnswer():
    userInput=request.get_json()

    usermessage = userInput["message"]

    chatbotResp=chatBotResponse(usermessage)

    # return (userInput)
    return jsonify(chatbotResp)


@app.errorhandler(Exception)
def basic_error_handlor(e):
    return jsonify("{Error: Some error as occured" + str(e)+"}")
    


  

if __name__=="__main__":
    app.run(debug=True)
