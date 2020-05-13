import os

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data

from alphazero.src.nn.layers import ConvLayer, PolicyHead, ResLayer, ValueHead


class AlphaZeroNet(nn.Module):
    def __init__(self, game, res_layer_number = 5):
        super(AlphaZeroNet, self).__init__()

        input_planes = game.get_input_planes()
        board_dim = game.get_board_dimensions()

        self.conv = ConvLayer(board_dim = board_dim, inplanes = input_planes)
        self.res_layers = nn.ModuleList([ ResLayer() for i in range(res_layer_number)])
        self.valueHead = ValueHead(board_dim = board_dim)
        self.policyHead = PolicyHead(board_dim = board_dim, action_size = game.get_action_size(), output_planes = game.get_output_planes())

    def forward(self,s):
        s = self.conv(s)

        for res_layer in self.res_layers:
            s = res_layer(s)

        v = self.valueHead(s)
        p = self.policyHead(s)

        return v, p

    def loss(self, predicted, label):
        (v, p) = predicted
        (z, pi) = label

        value_error = (z.float() - torch.transpose(v,0,1))**2
        policy_error = (pi.float()*p.log()).sum(1)

        return (value_error - policy_error).mean() #no need to add the l2 regularization term as it is done in the optimizer
