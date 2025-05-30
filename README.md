# Temporal Reasoning with POMDPs: The Little Prince

This project implements a temporal reasoning agent using the Viterbi algorithm for a Partially Observable Markov Decision Process (POMDP) in the "Little Prince" scenario. The goal is to infer the most likely sequence of hidden states given a sequence of observations and actions in a dynamic environment.

## 🧠 Project Overview

In partially observable environments, an agent must reason about hidden states based on noisy or incomplete observations. This project tackles this challenge by:

* Parsing environment definitions and sequences from structured input files
* Building normalized probability distributions from weighted state, transition, and observation tables
* Applying the Viterbi algorithm to find the most probable state sequence traversed by the agent

## 📁 Repository Structure

```
.
├── viterbi.py                # Main script implementing the Viterbi-based state inference
├── state_weights.txt             # Initial state distribution (unnormalized)
├── state_action_state_weights.txt # Transition model (unnormalized)
├── state_observation_weights.txt  # Observation likelihoods (unnormalized)
├── observation_actions.txt       # Sequence of observations and corresponding actions
├── states.txt                    # Output: most probable sequence of hidden states
├── Homework 3 Description.pdf    # Full problem specification and sample test case
```

## 🔍 How It Works

1. **Input Parsing**
   The program reads:

   * Prior state weights
   * (state, action, state) transition weights
   * (state, observation) observation weights
   * Observation-action pairs to analyze

2. **Probability Normalization**
   All weight tables are normalized into probability distributions:

   * $P(s_0)$ — Initial state probability
   * $P(s' | s, a)$ — Transition model
   * $P(o | s)$ — Observation likelihood

3. **Viterbi Algorithm**
   The algorithm builds a trellis and backpointer table to efficiently compute the most likely hidden state sequence that matches the input observation-action chain.

4. **Output Generation**
   The most probable state path is written to `states.txt` in the required format.

## 📄 Sample Input (excerpt)

**observation\_actions.txt**

```
observation_actions
4
"Apple" "Turnaround"
"Apple" "Backward"
"Apple" "Forward"
"Volcano"
```

**state\_weights.txt**

```
state_weights
3 0
"S0" 2
"S1" 5
"S2" 5
```

## 📄 Sample Output

**states.txt**

```
states
4
"S2"
"S2"
"S2"
"S1"
```

## 🛠️ Run Instructions

Make sure Python 3 is installed. Then simply run:

```bash
python3 viterbi.py
```

The output will be saved to `states.txt`.

## ✅ Project Highlights

* Implements Viterbi decoding for POMDPs
* Handles missing probabilities via default weight normalization
* Modular input design to allow flexible testing and extension