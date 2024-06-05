import torch
from torch import nn, load
from torchvision import transforms

from PIL import Image
from io import BytesIO

import numpy as np

class BrainTumorClassifier(nn.Module):
    def __init__(self):
        super().__init__()

        self.class_names = ["Glioma", "Meningioma", "Normal", "Hipófise"]

        self.transform = transforms.Compose([
            transforms.Resize([224, 224]),
            transforms.RandomRotation(degrees=(-10, 10)),
            transforms.RandomPerspective(distortion_scale=.1, p=.2),
            transforms.ToTensor(),
        ])

        self.conv1 = nn.Conv2d(in_channels=3, out_channels=64, kernel_size=(3,3)) 
        self.conv2 = nn.Conv2d(64, 64, (3,3))
        self.activation = nn.ReLU()
        self.bnorm = nn.BatchNorm2d(num_features=64)
        self.pool = nn.MaxPool2d(kernel_size=(2,2))
        self.flatten = nn.Flatten()
        self.linear1 = nn.Linear(in_features=14*14*64, out_features=256)
        self.linear2 = nn.Linear(256, 128)
        self.output = nn.Linear(128, 4)

    def load_weights(self, path="./app/models/BrainTumorClassifier/best.pth"):
        self.load_state_dict(load(path, map_location='cpu'))
        

    def transforms(self, x):
        img = Image.open(BytesIO(x)).convert('RGB').resize((64, 64))

        img = np.array(img.getdata()).reshape(*img.size, -1)
        img = img / 255
        img = img.transpose(2, 0, 1)
        img = torch.tensor(img, dtype=torch.float).view(-1, *img.shape)
   
        return img
    
    def forward(self, x):
        x = self.transforms(x)

        x = self.pool(self.bnorm(self.activation(self.conv1(x))))
        x = self.pool(self.bnorm(self.activation(self.conv2(x))))
        x = self.flatten(x)

        # Camadas densas
        x = self.activation(self.linear1(x))
        x = self.activation(self.linear2(x))
        
        return self.output(x)
    

if __name__ == "__main__":
    net = BrainTumorClassifier()
    print(net.requires_grad_())
    net.load_weights()