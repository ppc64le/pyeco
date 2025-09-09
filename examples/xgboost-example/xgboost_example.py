import os
import shutil
import numpy as np
import pandas as pd
from scipy.stats import mode
import xgboost as xgb
import requests
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import sentencepiece as spm
from roman import fromRoman
from sphinx.application import Sphinx

print("✅ Starting fully connected environment test...\n")

# --- 1. Generate synthetic dataset and preprocess ---
X = np.random.rand(50, 5)
y = np.random.randint(0, 2, size=50)
df = pd.DataFrame(X, columns=[f"f{i}" for i in range(X.shape[1])])
df['target'] = y

# --- 2. Train XGBoost model ---
dtrain = xgb.DMatrix(X, label=y)
params = {"objective": "binary:logistic", "eval_metric": "logloss"}
bst = xgb.train(params, dtrain, num_boost_round=5)
preds = bst.predict(dtrain)
df['pred'] = preds

# --- 3. Analyze predictions using SciPy and convert some to Roman numerals ---
most_common = mode(np.round(preds), keepdims=True).mode.item()
df['pred_roman'] = [fromRoman("X")+fromRoman("V") if p > 0.5 else fromRoman("V") for p in preds]
print("Most common prediction (rounded):", most_common)
print("DataFrame head with Roman numerals:\n", df.head())

# --- 4. Tokenize textual representation of predictions using SentencePiece ---
with open("predictions.txt", "w") as f:
    for i, val in enumerate(df['pred']):
        f.write(f"Prediction {i}: {val}\n")

spm.SentencePieceTrainer.Train(input="predictions.txt", model_prefix="spm_model", vocab_size=30)
tokenizer = spm.SentencePieceProcessor(model_file="spm_model.model")
tokenized = [tokenizer.encode(f"Prediction {i}: {val}", out_type=str) for i, val in enumerate(df['pred'])]
print("Tokenized first 3 predictions:", tokenized[:3])

# --- 5. Sign predictions using Cryptography ---
key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
message = str(df['pred'].tolist()).encode()
signature = key.sign(message, padding.PKCS1v15(), hashes.SHA256())
key.public_key().verify(signature, message, padding.PKCS1v15(), hashes.SHA256())
print("Cryptography sign/verify successful for predictions")

# --- 6. Send signed data via HTTP request ---
response = requests.post("https://httpbin.org/post", data=message)
print("POST request status code:", response.status_code)

# --- 7. Generate minimal Sphinx documentation for this workflow ---
docs_dir = "sphinx_test_docs"
os.makedirs(docs_dir, exist_ok=True)
with open(os.path.join(docs_dir,"conf.py"),"w") as f:
    f.write("project='TestProject'\nmaster_doc='index'\n")
with open(os.path.join(docs_dir,"index.rst"),"w") as f:
    f.write("TestProject\n===========\nSample Documentation for Environment Test\n")

out_dir = os.path.join(docs_dir, "_build")
doctree_dir = os.path.join(docs_dir, "_doctrees")
app = Sphinx(docs_dir, docs_dir, out_dir, doctree_dir, buildername="html")
app.build()
print("Sphinx HTML build successful ->", out_dir)

# --- 8. Cleanup temporary files ---
os.remove("predictions.txt")
os.remove("spm_model.model")
os.remove("spm_model.vocab")
shutil.rmtree(docs_dir)

print("\n🎉 Fully connected environment test completed successfully.")

