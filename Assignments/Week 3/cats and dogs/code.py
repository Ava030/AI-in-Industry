import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from torchvision import datasets, models
from torch.utils.data import DataLoader

# Data Transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# Load Data
train_data = datasets.ImageFolder(
    'cats_and_dogs_data/training_set/training_set', transform=transform)
val_data = datasets.ImageFolder(
    'cats_and_dogs_data/test_set/test_set', transform=transform)
train_dl = DataLoader(train_data, batch_size=32, shuffle=True)
val_dl = DataLoader(val_data, batch_size=32)

# Model


class DogsCatsResNet50(nn.Module):
    def __init__(self):
        super().__init__()
        self.network = models.resnet50(pretrained=True)
        in_features = self.network.fc.in_features
        self.network.fc = nn.Linear(in_features, 2)

    def forward(self, xb):
        return self.network(xb)

# Training Functions


def accuracy(outputs, labels):
    _, preds = torch.max(outputs, dim=1)
    return torch.tensor(torch.sum(preds == labels).item() / len(preds))


def train_model(model, criterion, optimizer, num_epochs=10):
    for epoch in range(num_epochs):
        for images, labels in train_dl:
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

        # Validation
        val_loss = 0.0
        val_acc = 0.0
        with torch.no_grad():
            for images, labels in val_dl:
                outputs = model(images)
                loss = criterion(outputs, labels)
                val_loss += loss.item()
                val_acc += accuracy(outputs, labels)

        val_loss /= len(val_dl)
        val_acc /= len(val_dl)
        print(
            f"Epoch [{epoch+1}/{num_epochs}], Loss: {val_loss:.4f}, Acc: {val_acc:.4f}")


# Main
model = DogsCatsResNet18()
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.001)

train_model(model, criterion, optimizer)
