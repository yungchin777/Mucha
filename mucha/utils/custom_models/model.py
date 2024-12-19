import torch.nn as nn

__all__ = ["mymodel"]

class MyModel(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.conv = nn.Conv2d(3, 16, 3, stride=1, padding=1)
        self.fc = nn.Linear(16 * 32 * 32, num_classes)

    def forward(self, x):
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

def mymodel(**params):
    return MyModel(**params)