import numpy as np
from hmmlearn import hmm

def build_gaussian_hmm():
    """
    Build and configure a 3-state Gaussian HMM with predefined parameters.
    Represents a simple weather-like model: Sunny, Cloudy, Rainy.
    """
    model = hmm.GaussianHMM(n_components=3, covariance_type="full", n_iter=100)

    # Initial state probabilities
    model.startprob_ = np.array([0.6, 0.3, 0.1])

    # Transition matrix
    model.transmat_ = np.array([
        [0.7, 0.2, 0.1],
        [0.3, 0.5, 0.2],
        [0.1, 0.3, 0.6],
    ])

    # Mean observations per state (e.g. temperature readings)
    model.means_ = np.array([[28.0], [18.0], [8.0]])

    # Covariance per state
    model.covars_ = np.array([[[4.0]], [[9.0]], [[6.0]]])

    return model


def train_hmm_from_observations(observations):
    """
    Train a Gaussian HMM from raw observation data using the Baum-Welch algorithm.
    """
    model = hmm.GaussianHMM(n_components=3, covariance_type="diag", n_iter=200,
                             random_state=42)
    model.fit(observations)
    return model


if __name__ == "__main__":
    rng = np.random.default_rng(42)

    # --- Build a model with known parameters ---
    print("=== Gaussian HMM: Weather Simulation ===")
    model = build_gaussian_hmm()

    # Generate a sequence of 200 observations
    observations, state_sequence = model.sample(200, random_state=42)
    print(f"Generated {len(observations)} observations from the model.")
    print(f"First 10 observations: {observations[:10].flatten().round(2).tolist()}")
    print(f"First 10 true states : {state_sequence[:10].tolist()}")

    # Decode the most likely state sequence using Viterbi
    log_prob, decoded_states = model.decode(observations, algorithm="viterbi")
    print(f"\nViterbi decoding log-probability: {log_prob:.4f}")
    print(f"First 10 decoded states: {decoded_states[:10].tolist()}")

    # Score the observation sequence
    score = model.score(observations)
    print(f"Log-likelihood of the sequence: {score:.4f}")

    # --- Train a model from observations ---
    print("\n=== Training HMM from Observations (Baum-Welch) ===")
    # Simulate observations from two different Gaussian distributions
    obs_train = np.concatenate([
        rng.normal(loc=5.0, scale=1.0, size=(150, 1)),
        rng.normal(loc=15.0, scale=2.0, size=(150, 1)),
    ])
    trained_model = train_hmm_from_observations(obs_train)
    train_score = trained_model.score(obs_train)
    print(f"Trained model log-likelihood: {train_score:.4f}")
    print(f"Learned means: {trained_model.means_.flatten().round(3).tolist()}")
    print("HMM example completed successfully.")
