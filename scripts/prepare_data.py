import pandas as pd
import numpy as np
import random
import os
import itertools

np.random.seed(42)
random.seed(42)

def generate_synthetic_data():
    """Generates synthetic data with strict adherence to the severity rubric."""
    
    variations = []
    
    # -------------------------------------------------------------------------
    # LEVEL 5 (CHARCOAL) - Literal Crimes, Disasters, and Ruin
    # -------------------------------------------------------------------------
    l5_subjects = ["I", "My friend", "My dad", "We", "My team"]
    l5_actions = [
        ("committed tax fraud", "Financial"), ("robbed a bank", "Financial"), 
        ("dropped the production database without backups", "Coding"),
        ("got sued for 10 million dollars", "Financial"), ("burned down the office", "Career"), 
        ("deleted the entire codebase", "Coding"), ("was arrested for embezzlement", "Financial"), 
        ("crashed the company car into a building", "Career"),
        ("leaked all user data to the dark web", "Coding"), ("stole from the cartel", "Financial"), 
        ("got 10 years in prison", "General"), ("ruined the company", "Career"), 
        ("murdered someone", "General"), ("committed treason", "General"), 
        ("am fleeing the country", "General")
    ]
    for s, (a, cat) in itertools.product(l5_subjects, l5_actions):
        variations.append({"text": f"{s} {a}.", "U": 5, "P": 5, "C": 5, "category": cat, "S": 15, "cooked_level": 5})

    # -------------------------------------------------------------------------
    # LEVEL 4 (ABSOLUTELY COOKED) - Fired, Failed out, Massive Debt
    # -------------------------------------------------------------------------
    l4_actions = [
        ("got fired today", "Career"), ("failed out of college", "Academic"), 
        ("have an exam in 5 minutes and haven't opened the book", "Academic"),
        ("am 50k in credit card debt", "Financial"), ("totaled my car without insurance", "Financial"), 
        ("accidentally replied all with an insult", "Social"),
        ("pushed a bug that cost the company 50k", "Coding"), ("lost my passport in a foreign country", "General")
    ]
    for s, (a, cat) in itertools.product(l5_subjects, l4_actions):
        variations.append({"text": f"{s} {a}.", "U": 5, "P": 4, "C": 5, "category": cat, "S": 14, "cooked_level": 4})

    # -------------------------------------------------------------------------
    # LEVEL 0 & 1 (NOT COOKED) - Fine, Chilling
    # -------------------------------------------------------------------------
    l0_actions = [
        ("got a promotion", "Career"), ("aced the exam", "Academic"), 
        ("found 20 bucks", "Financial"), ("finished all my work early", "Career"),
        ("am completely prepared", "Academic"), ("have zero bugs in my code", "Coding"), 
        ("just relaxing at home", "General"),
        ("paid off my loans", "Financial"), ("had a great day", "Social")
    ]
    for s, (a, cat) in itertools.product(l5_subjects, l0_actions):
        variations.append({"text": f"{s} {a}.", "U": 1, "P": 1, "C": 1, "category": cat, "S": 3, "cooked_level": 0})
        
    df = pd.DataFrame(variations)
    df["source"] = "synthetic"
    return df

def map_tweet_emotions():
    try:
        tweets = pd.read_csv("best datasets/tweet_emotions.csv")
        mapping = {'happiness': 0, 'relief': 0, 'neutral': 1, 'worry': 2, 'sadness': 3, 'anger': 4, 'hate': 4}
        tweets_mapped = tweets[tweets['sentiment'].isin(mapping.keys())].copy()
        tweets_mapped['cooked_level'] = tweets_mapped['sentiment'].map(mapping)
        # Downsample heavily so they don't overpower the crimes
        tweets_sampled = tweets_mapped.groupby('cooked_level').sample(n=100, random_state=42, replace=True)
        return pd.DataFrame({
            "text": tweets_sampled["content"],
            "category": "General",
            "cooked_level": tweets_sampled["cooked_level"],
            "source": "tweet_emotions"
        })
    except Exception as e:
        return pd.DataFrame()

if __name__ == "__main__":
    print("Generating custom dataset...")
    syn_df = generate_synthetic_data()
    print(f"Generated {len(syn_df)} synthetic examples (Catastrophes & Successes).")
    tw_df = map_tweet_emotions()
    final_df = pd.concat([syn_df, tw_df], ignore_index=True).sample(frac=1, random_state=42).reset_index(drop=True)
    final_df['text'] = final_df['text'].astype(str)
    os.makedirs("data/processed", exist_ok=True)
    out_path = "data/processed/cooked_dataset.csv"
    final_df.to_csv(out_path, index=False)
    print(f"Final dataset created: {out_path} with {len(final_df)} rows.")
