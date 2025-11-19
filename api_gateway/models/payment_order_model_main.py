import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Step 1: Define Model Architecture
class PaymentOrderModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(PaymentOrderModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, hidden_size // 2)
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(hidden_size // 2, output_size)
        self.softmax = nn.Softmax(dim=1)
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        return self.softmax(x)

# Step 2: Data Preprocessing
class PaymentOrderDataset(Dataset):
    def __init__(self, data, labels):
        self.data = torch.tensor(data, dtype=torch.float32)
        self.labels = torch.tensor(labels, dtype=torch.long)
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]

# Sample Data (Replace with real dataset)
data = np.random.rand(1000, 10)  # 1000 samples, 10 features
labels = np.random.randint(0, 2, 1000)  # Binary classification (0 or 1)

# Split dataset
data_train, data_test, labels_train, labels_test = train_test_split(data, labels, test_size=0.2, random_state=42)
scaler = StandardScaler()
data_train = scaler.fit_transform(data_train)
data_test = scaler.transform(data_test)

train_dataset = PaymentOrderDataset(data_train, labels_train)
test_dataset = PaymentOrderDataset(data_test, labels_test)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

# Step 3: Model Training
input_size = 10
hidden_size = 64
output_size = 2
model = PaymentOrderModel(input_size, hidden_size, output_size)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

epochs = 20
best_accuracy = 0
for epoch in range(epochs):
    total_loss = 0
    model.train()
    for batch_data, batch_labels in train_loader:
        optimizer.zero_grad()
        outputs = model(batch_data)
        loss = criterion(outputs, batch_labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    
    # Step 4: Model Evaluation on Validation Set
    model.eval()
    predictions = []
    actuals = []
    with torch.no_grad():
        for batch_data, batch_labels in test_loader:
            outputs = model(batch_data)
            preds = torch.argmax(outputs, dim=1)
            predictions.extend(preds.numpy())
            actuals.extend(batch_labels.numpy())
    
    accuracy = accuracy_score(actuals, predictions)
    print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss:.4f}, Accuracy: {accuracy * 100:.2f}%")
    
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        joblib.dump(model.state_dict(), 'best_payment_order_model.pth')
        print("Best model saved!")

# Step 5: Load & Deploy Model
def load_model(model_path):
    model = PaymentOrderModel(input_size, hidden_size, output_size)
    model.load_state_dict(joblib.load(model_path))
    model.eval()
    return model

loaded_model = load_model('best_payment_order_model.pth')
print(f"Loaded model is ready for deployment with {best_accuracy * 100:.2f}% accuracy!")
