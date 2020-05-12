import os

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data

from src.nn.model import AlphaZeroNet


class ModelWrapper(object):
    def __init__(self, game, device, **params):
        super(ModelWrapper, self).__init__()
        self.device = device
        self.nn = AlphaZeroNet(game, params['n_res_layers']).to(self.device)
        self.optimizer = optim.Adam(self.nn.parameters(), lr = params['learning_rate'], weight_decay = params['weight_decay'])

    def train(self, data, batch_size = 16, loss_display = 5, training_steps = 150):
        self.nn.train()

        total_loss = 0.0
        running_loss = 0

        for i in range(training_steps): 
            board, policy, value = data.sample_batch(batch_size)
            self.optimizer.zero_grad()
            v, p = self.nn(torch.Tensor(board).to(self.device))
            loss = self.nn.loss((v, p), (torch.Tensor(value).to(self.device), torch.Tensor(policy).to(self.device)))
            loss.backward()
            self.optimizer.step()
            running_loss += loss.item()
            total_loss += loss.item()
            
            if i!= 0 and i % loss_display == 0:    
                print('[%d, %5d] loss: %.3f' %
                      (1, i + 1, running_loss / loss_display))
                running_loss = 0.0

        return total_loss/training_steps
    
    def predict(self, board):
        self.nn.eval()
        board = torch.Tensor(board).to(self.device)
        with torch.no_grad():
            v, p = self.nn(board)

        p = p.detach().cpu().numpy()
        return v, p

    def save_model(self, folder = "models", model_name = "fdsmodel.pt"):
        if not os.path.isdir(folder):
            os.mkdir(folder)

        torch.save({
            'model_state_dict': self.nn.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            }, "{}/{}".format(folder, model_name))

    def load_model(self, path = "models/fdsmodel.pt", load_optim = False):
        cp = torch.load(path, map_location=self.device)
        self.nn.load_state_dict(cp['model_state_dict'])
        if load_optim:   
            self.optimizer = optim.Adam(self.nn.parameters(), lr = 0.1, weight_decay = 0.005)
            self.optimizer.load_state_dict(cp['optimizer_state_dict'])
        return self.nn
