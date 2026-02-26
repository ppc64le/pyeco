import sentencepiece as spm
import pandas as pd
import os

print("✅ Running sub_test3: SentencePiece + Pandas")

# Create sample text data
df = pd.DataFrame({"text": ["Hello world", "Testing SentencePiece", "Python is fun"]})

# Save sample text to file
with open("sample3.txt", "w") as f:
    for t in df['text']:
        f.write(t + "\n")

# Train SentencePiece model
# vocab_size should be <= number of unique characters in sample text
spm.SentencePieceTrainer.Train(input="sample3.txt", model_prefix="spm_model3", vocab_size=26)

# Load the trained tokenizer
tokenizer = spm.SentencePieceProcessor(model_file="spm_model3.model")

# Tokenize each text entry
df['tokens'] = df['text'].apply(lambda x: tokenizer.encode(x, out_type=str))
print("Tokenized values:\n", df)

# Cleanup temporary files
os.remove("sample3.txt")
os.remove("spm_model3.model")
os.remove("spm_model3.vocab")

print("✅ sub_test3 completed successfully.")

