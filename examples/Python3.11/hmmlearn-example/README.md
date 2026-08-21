## Purpose: Demonstrates sequence modeling and state inference using the hmmlearn library with a Gaussian Hidden Markov Model (HMM).

### Packages used:
hmmlearn
numpy
scikit-learn
scipy

### Functionality:

- Creates a 3-state Gaussian HMM representing a synthetic weather-like sequence model.
- Generates sample observation sequences from the trained model.
- Decodes the most likely hidden state sequence using the Viterbi algorithm.
- Scores the likelihood of an observation sequence under the model.
- Retrains the model from observations using the Baum-Welch (EM) algorithm.

### How to run the example :
```
chmod +x install_test_example.sh
./install_test_example.sh
```

### License:
It's covered under Apache 2.0 licenses
