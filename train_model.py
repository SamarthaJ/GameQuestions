import pandas as pd
from sentence_transformers import SentenceTransformer, InputExample, losses, util
from torch.utils.data import DataLoader

# Load your dataset
file_path = r'C:\Users\Shrey\Desktop\game\GameQuestions\train_data.csv'
data = pd.read_csv(file_path)

# Convert the dataset into InputExample format
train_examples = []
for index, row in data.iterrows():
    train_examples.append(InputExample(texts=[row['Sentence 1'], row['Sentence 2']], label=float(row['Label'])))

# Load a pre-trained SentenceTransformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Define the loss function (CosineSimilarityLoss)
train_loss = losses.CosineSimilarityLoss(model)

# Create a DataLoader
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)

# Fine-tune the model
model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=3,  # Adjust based on dataset size
    warmup_steps=100,
    show_progress_bar=True
)

# Save the fine-tuned model
model.save("fine-tuned-never-have-i-ever-model")
