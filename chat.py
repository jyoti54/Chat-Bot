import torch
from model import NeuralNet
from preprocessor import tokenize,bag_of_words
import json
import random


with open("intents.json",'r') as f:
    intents_data = json.load(f)
    intents = intents_data['intents']

File = "model_data.pth"

model_data=torch.load(File)

print(model_data)


model_state = model_data['model_state']
input_size = model_data['input_size']
hidden_size = model_data['hidden_size']
output_size = model_data['output_size']
all_words = model_data['all_words']
tags = model_data['tags']

device =torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = NeuralNet(input_size,hidden_size,output_size).to(device)
model.load_state_dict(model_state)
model.eval()

def response(user_input):
    sentence=tokenize(user_input)
    x=bag_of_words(sentence, all_words)
    x=x.reshape(1, x.shape[0])
    x=torch.from_numpy(x).to(device)
    out=model(x)
    _, predicted=torch.max(out,dim=1)
    tag = tags[predicted.item()]
    probs = torch.softmax(out, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item()>0.75:
        for intent in intents:
            if tag == intent['tag']:
                return random.choice(intent['responses'])
    
    return "I do not understand, kindly rephrase"
        
        

if __name__=="__main__":
    print("Lets start chatting! type(quit) to exit te chat")
    while True:
        user_input = input("User :")
        if user_input =="quit":
            break
        
        print(response(user_input))