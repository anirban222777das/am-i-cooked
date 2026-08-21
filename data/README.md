# Dataset and Labeling Methodology

This directory contains the datasets used to train the "Am I Cooked? 💀" NLP model.

## Folder Structure
- `raw/`: Raw, unmodified datasets from external sources.
- `processed/`: Cleaned, labeled datasets ready for ML training.

## The Cooked Rubric
Because our target variable (`cooked_level`) is not a standard NLP label (like "sentiment"), we map real-world stress and emotion data to our target, and supplement it with custom synthetic data.

The formal definition of a situation's "Cookedness" is derived from three independent sub-factors:
1. **U = Urgency** (1 to 5): 1 = Far away / No time limit, 5 = Immediate / Past due.
2. **P = Lack of Preparation** (1 to 5): 1 = Fully prepared / In control, 5 = Zero preparation / Completely lost.
3. **C = Consequences** (1 to 5): 1 = Trivial / Easily fixable, 5 = Life-ruining / Irreversible.

### Mathematical Labeling
We define the **Severity Score (S)** as the sum of these factors:
`S = U + P + C`  (Range: 3 to 15)

We map the severity score `S` to our ground-truth `cooked_level` (0-5) as follows:
- **0 (NOT COOKED)**: S ∈ [3, 4] -> e.g., "I have an exam in a month and I'm studying."
- **1 (SLIGHTLY COOKED)**: S ∈ [5, 6] -> e.g., "Lost $50."
- **2 (GETTING COOKED)**: S ∈ [7, 9] -> e.g., "Exam next week, haven't started."
- **3 (VERY COOKED)**: S ∈ [10, 12] -> e.g., "Broke production, boss is angry."
- **4 (ABSOLUTELY COOKED)**: S ∈ [13, 14] -> e.g., "Exam in 1 hour, haven't studied all semester."
- **5 (CHARCOAL)**: S = 15 -> e.g., "Expelled from university, debt collectors at the door."

## Data Pipeline
To build our final dataset:
1. **Synthetic Core**: We generated a diverse set of synthetic situations covering Academic, Career, Financial, Social, and Coding. This ensures all categories and edge cases (sarcasm, short texts, slang, typos) are represented with exact `U`, `P`, `C` scoring.
2. **Real-world Distillation**: We sample thousands of real texts from `tweet_emotions.csv` and `Stress.csv`. We map emotions like `worry`, `sadness`, and `anger` to mid/high cooked levels, and `happiness` to low cooked levels. This gives our model the vocabulary of real human complaints.
3. **Augmentation**: We apply random lowercase and spelling permutations to prevent overfitting on perfect grammar.

Run `python scripts/prepare_data.py` to reproduce the final `data/processed/cooked_dataset.csv`.
