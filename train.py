import json
from preprocessor import tokenize,stem,bag_of_words
import numpy as np
from torch.utils.data import Dataset,DataLoader
from model import NeuralNet
import torch
import torch.nn as nn

with open('intents.json','r') as f:
    data = json.load(f)
    intents = data['intents']
    
# print(intents)

tags=[]
all_words=[]
xy=[]

for intent in intents:
    # print(intent)
    tag = intent['tag']
    tags.append(tag)
    
    for pattern in intent['patterns']:
        words = tokenize(pattern)
        all_words.extend(words)
        
        xy.append((words, tag))
        
# print("tags: ",tags)
# print("all_words", all_words)
# print("xy:", xy)


ignore_words = ['?','!','.']

#alll words stemmed and puntuation is also removed
all_words = [stem(word) for word in all_words if word not in ignore_words]

all_words = sorted(set(all_words))

tags = sorted(set(tags))


x_train = []
y_train = []
for words, tag in xy:
    bag = bag_of_words(words,all_words)
    x_train.append(bag)
    
    # label = tags.index[tag]
    label = tags.index(tag)
    
    y_train.append(label)
    
x_train = np.array(x_train)
y_train = np.array(y_train)
    
class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train
    def __getitem__(self, index):
            return self.x_data[index],self.y_data[index]
        
    def __len__(self):
        return self.n_samples
    
# Hyper parameters
epochs = 1000       
batch_size=8
input_size=len(x_train[0])
hidden_size =8
output_size =len(tags)
dataset = ChatDataset()
learning_rate = 0.001

dataset[0]

train_loader = DataLoader(dataset=dataset, batch_size=batch_size,num_workers=0)  

device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')


model = NeuralNet(input_size, hidden_size,output_size).to(device)

criteria = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)


for epoch in range(epochs):
    for bagofwords,label in train_loader:
        bagofwords=bagofwords.to(device)
        label = label.to(dtype=torch.long).to(device)
        
        output = model(bagofwords)
    
        loss = criteria(output,label)
        
        optimizer.zero_grad()
        
        loss.backward()
        optimizer.step()
            
    if (epoch+1)%100==0:    
        print(f'epoch: {epoch+1}/{epochs}, loss:{loss.item():4f}')   

print(f'final loss: {loss.item():4f}')   



data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "hidden_size": hidden_size,
    "output_size": output_size,
    "all_words":all_words,
    "tags": tags
}

File = "model_data.pth"
torch.save(data,File)
print(f'Model data saved into {File}')

