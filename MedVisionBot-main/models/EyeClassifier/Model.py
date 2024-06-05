import torch
from torch import nn, load

from PIL import Image
from io import BytesIO

import numpy as np


class EyeClassifier(nn.Module):
  def __init__(self):
    super().__init__()

    self.class_names = ['Antecedentes da Retinopatia Diabética', 'Neovascularização Coroidal', 'Oclusão da veia central da retina', 'Normal']

    self.conv1 = nn.Conv2d(in_channels=3, out_channels=64, kernel_size=(3,3)) 
    self.conv2 = nn.Conv2d(64, 64, (3,3))
    self.activation = nn.ReLU()
    self.bnorm = nn.BatchNorm2d(num_features=64)
    self.pool = nn.MaxPool2d(kernel_size=(2,2))
    self.flatten = nn.Flatten()

    # output = (input - filter + 1) / stride
    # Convolução 1 -> (64 - 3 + 1) / 1 = 62x62
    # Pooling 1 -> Só dividir pelo kernel_size = 31x31
    # Convolução 2 -> (31 - 3 + 1)/ 1 = 29x29
    # Pooling 2 -> Só dividir pelo kernel_size = 14x14
    # 14 * 14 * 64
    # 33907200 valores -> 256 neurônios da camada oculta
    self.linear1 = nn.Linear(in_features=14*14*64, out_features=256)
    self.linear2 = nn.Linear(256, 128)
    self.output = nn.Linear(128, 4)

  
  
  def load_weights(self, path="./app/models/EyeClassifier/best.pth"):
    self.load_state_dict(load(path, map_location='cpu'))
        

  def transforms(self, x):
    imagem = Image.open(BytesIO(x)).convert('RGB').resize((64, 64))

    imagem = np.array(imagem.getdata()).reshape(*imagem.size, -1)
    imagem = imagem / 255
    imagem = imagem.transpose(2, 0, 1)
    imagem = torch.tensor(imagem, dtype=torch.float).view(-1, *imagem.shape)

    return imagem
    
  def forward(self, x):
    x = self.transforms(x)

    x = self.pool(self.bnorm(self.activation(self.conv1(x))))
    x = self.pool(self.bnorm(self.activation(self.conv2(x))))
    x = self.flatten(x)

    x = self.activation(self.linear1(x))
    x = self.activation(self.linear2(x))
    
    return self.output(x)
