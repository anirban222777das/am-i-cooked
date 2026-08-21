# Dataset Research & Sources

This document details the evaluation of the publicly available datasets provided for the "Am I Cooked? 💀" project.

## 1. `Stress.csv` (Reddit Stress Dataset)
- **Source**: Appears to be the Dreaddit dataset (or similar subset) from Kaggle (often licensed CC-BY or similar for research).
- **Number of Samples**: 2,838
- **Relevant Columns**: `text`, `label`
- **Target Labels**: Binary (1 = Stressed [1488 samples], 0 = Not Stressed [1350 samples]).
- **Text Quality**: High. Contains real, long-form Reddit posts from subreddits like `r/ptsd`, `r/relationships`, and `r/assistance`.
- **Missing Values**: None.
- **Suitability**: Excellent for baseline stress detection. The text length is varied, capturing genuine human complaints and worries.
- **Our Use Case**: We will map these into our synthetic generation pipeline or use them directly as examples of "Cooked" vs "Not Cooked" situations to bootstrap our target labels.

## 2. `tweet_emotions.csv` (Tweet Emotion Dataset)
- **Source**: Standard Kaggle Twitter emotion dataset (likely CC0 / public domain).
- **Number of Samples**: 40,000
- **Relevant Columns**: `content`, `sentiment`
- **Target Labels**: 13 emotions (`neutral`: 8638, `worry`: 8459, `happiness`: 5209, `sadness`: 5165, `love`: 3842, `surprise`: 2187, `fun`: 1776, `relief`: 1526, `hate`: 1323, `empty`: 827, `enthusiasm`: 759, `boredom`: 179, `anger`: 110)
- **Text Quality**: Good for short-form, slang-heavy internet text. Contains @mentions and emojis.
- **Missing Values**: None.
- **Suitability**: Very high. We can filter for negative emotions (`worry`, `sadness`, `anger`, `hate`) to represent "Cooked" states, and positive/neutral ones for "Not Cooked". 

## 3. `mental_health_dataset.csv`
- **Source**: Unknown (Likely generated for a class project).
- **Number of Samples**: 500
- **Relevant Columns**: `Daily_Reflections`, `Stress_Level`
- **Text Quality**: Very poor. Analysis reveals the text is entirely synthetic gibberish (e.g., *"Onto foreign do environmental anyone every nearly another."*).
- **Missing Values**: None.
- **Suitability**: **REJECTED**. The text column does not contain semantic meaning, which would completely ruin an NLP model's ability to learn text representations.

## 4. `Student Stress Factors.csv` & `Student Stress Factors (2).csv`
- **Source**: Kaggle / Survey data.
- **Number of Samples**: 53 and 520, respectively.
- **Relevant Columns**: Survey questions (e.g., "How would you rate your sleep quality?").
- **Text Quality**: N/A. There is no free-form text description column.
- **Missing Values**: None.
- **Suitability**: **REJECTED**. Our ML task is *text classification* based on a user's description of a situation. Since these datasets only contain multiple-choice survey responses, they cannot be used to train our NLP model.

---

## Conclusion & Next Steps for Data Labeling (Phase 2)
The raw datasets (`Stress.csv` and `tweet_emotions.csv`) contain binary stress labels and multi-class emotion labels, respectively. **They do not contain our target variable (`cooked_level` 0-5) or our `category` variable.** 

Therefore, in **Phase 2 (Custom Dataset Design)**, we will need to:
1. Sample the highest-quality texts from `Stress.csv` and `tweet_emotions.csv`.
2. Map their existing labels to our Cooked rubric (or use an LLM script to carefully annotate a subset with `cooked_level` and `category`).
3. Supplement with high-quality synthetic data to ensure edge cases (e.g. coding bugs, specific humor profiles) are well represented.
