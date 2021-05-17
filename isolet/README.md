# Isolated Letter Speech Recognition (ISOLET)

**Source:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/isolet)

**Tasks:** Classification

**Number of instances:** 7797

**Number of Attributes:** 617

150 subjects spoke the name of each letter of the alphabet twice. Hence, there are 52 training examples from each speaker. The speakers are grouped into sets of 30 speakers each, 4 groups can serve as training set, the last group as the test set. A total of 3 examples are missing, the authors dropped them due to difficulties in recording.

This is a good domain for a noisy, perceptual task. It is also a very good domain for testing the scaling abilities of algorithms.

## Get Started

* Download the dataset from UCI's repository and put all `.data` files in this directory
* Run `python3 read_data.py` to import data and visualize. Need `numpy, matplotlib` and `sklearn.preprocessing`.

