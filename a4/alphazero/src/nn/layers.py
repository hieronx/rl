import torch
import torch.nn as nn
import torch.nn.functional as F


class ConvLayer(nn.Module):
    def __init__(self, board_dim = (), inplanes = 1, planes=128, stride=1):
        super(ConvLayer, self).__init__()
        self.inplanes = inplanes
        self.board_dim = board_dim
        self.conv = nn.Conv2d(inplanes, planes, kernel_size=3, stride=stride,
                     padding=1, bias=False)
        self.bn = nn.BatchNorm2d(planes)

    def forward(self, s):
        s = s.view(-1, self.inplanes, self.board_dim[0], self.board_dim[1])  # batch_size x planes x board_x x board_y
        s = F.relu(self.bn(self.conv(s)))

        return s

class ResLayer(nn.Module):
    def __init__(self, inplanes=128, planes=128, stride=1):
        super(ResLayer, self).__init__()
        self.conv1 = nn.Conv2d(inplanes, planes, kernel_size=3, stride=stride,
                     padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=stride,
                     padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)

    def forward(self, x):
        residual = x
        out = self.conv1(x)
        out = F.relu(self.bn1(out))
        out = self.conv2(out)
        out = self.bn2(out)
        out += residual
        out = F.relu(out)
        
        return out


class PolicyHead(nn.Module):
    def __init__(self, board_dim = (), action_size = -1, output_planes = -1):
        super(PolicyHead, self).__init__()
        self.board_dim = board_dim
        self.action_size = action_size
        self.output_planes = output_planes

        self.conv1 = nn.Conv2d(128, 32, kernel_size=1) # policy head
        self.bn1 = nn.BatchNorm2d(32)
        
        self.logsoftmax = nn.LogSoftmax(dim=1)
        
        if self.output_planes > 1:
            self.conv2 = nn.Conv2d(32, self.output_planes, kernel_size=1) # policy head
        else:
            self.fc = nn.Linear(self.board_dim[0]*self.board_dim[1]*32, self.action_size)

    def forward(self,s):
        p = F.relu(self.bn1(self.conv1(s))) # policy head

        if self.output_planes > 1:
            p = conv2(p)
        else:
            p = p.view(-1, self.board_dim[0]*self.board_dim[1]*32)
            p = self.fc(p)
            
        p = self.logsoftmax(p).exp()

        return p


class ValueHead(nn.Module):
    def __init__(self, board_dim = ()):
        super(ValueHead, self).__init__()
        self.board_dim = board_dim
        self.conv = nn.Conv2d(128, 1, kernel_size=1) # value head
        self.bn = nn.BatchNorm2d(1)
        self.fc1 = nn.Linear(self.board_dim[0]*self.board_dim[1], 32) 
        self.fc2 = nn.Linear(32, 1)

    def forward(self,s):
        v = F.relu(self.bn(self.conv(s))) # value head
        v = v.view(-1, self.board_dim[0]*self.board_dim[1])  # batch_size X channel X height X width
        v = F.relu(self.fc1(v))
        v = torch.tanh(self.fc2(v))
        
        return v
