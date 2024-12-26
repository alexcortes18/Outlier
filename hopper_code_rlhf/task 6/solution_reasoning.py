from transformers import AutoTokenizer
from datasets import load_dataset
from sklearn.preprocessing import OneHotEncoder
from transformers import DataCollatorWithPadding
from transformers import AutoModelForSequenceClassification
import numpy as np
from transformers import TrainingArguments, Trainer
import torch
from torch import nn

# Import dataset and model's name
dataset = load_dataset("csv", data_files={"train": ["evp.train.csv"], "test": "evp.test.csv"})
MODEL_NAME = 'distilbert-base-uncased'

# Tokenize
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
encoder = OneHotEncoder(handle_unknown = 'ignore', sparse= False)
X = dataset['train']['level']
X = np.array(X).reshape(-1,1)
encoder.fit_transform(X)
LABEL_COUNT = len(encoder.categories_[0])

# Preprocess data
def preprocess(data_slice):
    """ Input: a batch of your dataset
        Example: { 'text': [['sentence1'], ['setence2'], ...],
                   'label': ['label1', 'label2', ...] }
    """
    """ Output: a batch of processed dataset
        Example: { 'input_ids': ...,
                   'attention_masks': ...,
                   'label': ... }
    """
    tokenized_text = tokenizer(data_slice["text"])
    data_slice['input_ids'] = tokenized_text['input_ids']
    data_slice['attention_mask'] = tokenized_text['attention_mask']

    level_array = np.array(data_slice['level']).reshape(-1, 1)
    encoded_labels = encoder.transform(level_array)

    data_slice['label'] = encoded_labels
    return data_slice

processed_data = dataset.map(preprocess,
                            batched = True,
                            batch_size = 1000)

# Pad and prepare model
data_collator = DataCollatorWithPadding(tokenizer = tokenizer)
model = AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased',num_labels = LABEL_COUNT)
train_val_dataset = processed_data['train'].train_test_split(test_size=0.1)

OUTPUT_DIR = "./checkpoints/"
LEARNING_RATE = 0.00005
BATCH_SIZE = 8
EPOCH = 3.0
training_args = TrainingArguments(
    output_dir = OUTPUT_DIR,
    learning_rate = LEARNING_RATE,
    per_device_train_batch_size = BATCH_SIZE,
    per_device_eval_batch_size = BATCH_SIZE,
    num_train_epochs = EPOCH,
)

trainer = Trainer(
    model = model,
    args = training_args,
    train_dataset = train_val_dataset['train'],
    eval_dataset = train_val_dataset['test'],
    data_collator = data_collator
)
# Train:
trainer.train()

# Save model:
trainer.save_model("./model/alex")

# Load model:
my_model = AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased',num_labels = LABEL_COUNT)
checkpoint = torch.load('./model/alex/pytorch_model.bin')
my_model.load_state_dict(checkpoint)

#Preparing test data
testing = processed_data['test']['text']#[0:1400]
testing_tokenized = tokenizer(testing, truncation=True, padding=True, return_tensors="pt")

# Predictions
with torch.no_grad():
    logits = my_model(**testing_tokenized).logits
predicts_testing = nn.functional.softmax(logits, dim = -1)
predictions_testing = predicts_testing.detach().numpy()
predictions_testing = np.argmax(predictions_testing,axis=1)

# Results: transform to one hot encodings
results_testing = []
for value in predictions_testing:
    temporal_testing = [0 for i in range(6)]
    temporal_testing[value] = 1
    results_testing.append(temporal_testing)
    
#And back to labels
results_testing = np.array(results_testing)
labels_testing = encoder.inverse_transform(results_testing)

# Evaluating Accuracy
same_levels = 0
for i in range(len(testing)):
    if processed_data['test']['level'][i] == labels_testing[i]:
        same_levels +=1

accuracy = same_levels / len(testing)
print(f"Accuracy is: ", accuracy)