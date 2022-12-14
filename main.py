import torchvision.utils
from numpy import size
from torchvision import datasets
from torchvision.transforms import ToTensor
import torch

# Download CIFAR10 dataset
train_data = datasets.CIFAR10(root='data', train=True, transform=ToTensor(), download=True)
test_data = datasets.CIFAR10(root='data', train=False, transform=ToTensor(), download=True)
# Load train and test dataset
trainloader = torch.utils.data.DataLoader(train_data, batch_size=4, shuffle=True, num_workers=0)
testloader = torch.utils.data.DataLoader(test_data, batch_size=4, shuffle=True, num_workers=0)

print(len(train_data))
print(len(test_data))

classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

import torch
from torch.utils.data import DataLoader

# Load train and test dataset
loaders = {'train': torch.utils.data.DataLoader(train_data, batch_size=32, shuffle=True),
           'test': torch.utils.data.DataLoader(test_data, batch_size=32, shuffle=True)}
print(loaders)

import numpy as np
import matplotlib.pyplot as plt

# Plot an image in the dataset with its class
i = 20.0
im, label = train_data[i]
print('image shape:', im.shape)
im = np.transpose(im, [1, 2, 0])
print('image shape:', im.shape)
print('corresponding class is:', classes[label])
plt.imshow(im)
plt.show()

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


# Define a Network
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=6, kernel_size=(3, 3), padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2))
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(in_channels=6, out_channels=16, kernel_size=(3, 3), padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2))
        )

        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(8 * 8 * 16, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x, plot=False):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.flatten(x)
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)

        return x


model = Net()
print(model)

# setting the optimizer as stochastic gradient descent

learning_rate = 0.01
optimizer = optim.SGD(model.parameters(), lr=learning_rate)
print(optimizer)

# Setting the loss function as cross entropy loss
loss_func = nn.CrossEntropyLoss()

from torch.autograd import Variable

# Training the loop
num_epochs = 10


def train(num_epochs, model, loaders):
    model.train()
    # Train the model
    total_step = len(loaders['train'])

    for epoch in range(num_epochs):
        for i, (images, labels) in enumerate(loaders['train']):
            # Gives the batch data and normalises x when iterate train_loader
            b_x = Variable(images)
            b_y = Variable(labels)

            output = model(b_x)
            loss = loss_func(output, b_y)

            # Clear gradients for this training step
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (i + 1) % 100 == 0:
                print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'
                      .format(epoch + 1, num_epochs, i + 1, total_step, loss.item()))


train(num_epochs, model, loaders)

# Save the model to be able to test it and improve it
PATH = "model.pth"
torch.save(model.state_dict(), PATH)


# Testing the model

def test():
    model.eval()
    with torch.no_grad():
        correct = 0
        total = 0
        for images, labels in loaders['test']:
            test_output = model(images)
            pred_y = torch.max(test_output, 1)[1].data.squeeze()
            accuracy = (pred_y == labels).sum().item() / float(labels.size(0))
        print('Test Accuracy of the model: %.2f' % accuracy)
    pass


test()


def imshow(img):
    img = img / 2 + 0.5
    np_img = img.numpy()
    plt.imshow(np.transpose(np_img, (1, 2, 0)))
    plt.show()


dataiter = iter(testloader)
images, labels = dataiter.next()

img_grid = torchvision.utils.make_grid(images)
img_grid = np.reshape(img_grid, newshape=(108, 138))  # Reshaping the image into a 2d array
# Print images
plt.imshow(img_grid)
plt.show()
# Print Labels
print('Actual: ', ' '.join(f'{classes[labels[j]]:5s}' for j in range(4)))
# Print Predicted
outputs = model(images)
_, predicted = torch.max(outputs, 1)
print('Predicted: ', ' '.join(f'{classes[predicted[i]]:5s}' for i in range(4)))
