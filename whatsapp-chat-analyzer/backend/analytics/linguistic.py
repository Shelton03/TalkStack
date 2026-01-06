import pandas as pd
import re
from collections import Counter
from typing import Dict, Any, List

# Comprehensive list of English stopwords and common chat words to filter out
STOPWORDS = {
    # Common English words
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at",
    "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can", "cant", "cannot",
    "could", "couldnt", "did", "didnt", "do", "does", "doesnt", "doing", "dont", "down", "during", "each", "few",
    "for", "from", "further", "had", "hadnt", "has", "hasnt", "have", "havent", "having", "he", "hed", "hell",
    "hes", "her", "here", "heres", "hers", "herself", "him", "himself", "his", "how", "hows", "i", "id", "ill",
    "im", "ive", "if", "in", "into", "is", "isnt", "it", "its", "its", "itself", "just", "let", "lets", "me",
    "more", "most", "my", "myself", "no", "nor", "not", "now", "of", "off", "on", "once", "only", "or", "other",
    "our", "ours", "ourselves", "out", "over", "own", "s", "same", "she", "shes", "should", "shouldnt", "so",
    "some", "such", "t", "than", "that", "thats", "the", "their", "theirs", "them", "themselves", "then", "there",
    "theres", "these", "they", "theyd", "theyll", "theyre", "theyve", "this", "those", "through", "to", "too",
    "under", "until", "up", "very", "was", "wasnt", "we", "wed", "well", "were", "weve", "werent", "what", "whats",
    "when", "whens", "where", "wheres", "which", "while", "who", "whos", "whom", "why", "whys", "will", "with",
    "wont", "would", "wouldnt", "you", "youd", "youll", "youre", "youve", "your", "yours", "yourself", "yourselves",
    
    # Common chat/filler words
    "yeah", "yep", "yes", "yup", "nope", "nah", "ok", "okay", "ohh", "ooh", "umm", "hmm", "haha", "lol", "lmao",
    "hahaha", "like", "really", "actually", "basically", "literally", "honestly", "seriously", "totally", "definitely",
    "probably", "maybe", "guess", "think", "know", "see", "mean", "said", "say", "saying", "going", "get", "got",
    "getting", "go", "went", "gone", "make", "made", "making", "take", "took", "taking", "come", "came", "coming",
    "want", "wanted", "need", "also", "well", "much", "many", "way", "one", "thing", "things", "time", "day", "today",
    "good", "better", "best", "bad", "worse", "worst", "lmfao", "omg", "omfg", "btw", "tbh", "imo", "imho",
    
    # Single letters and numbers often noise
    "u", "ur", "r", "n", "m", "k", "x", "b", "c", "d", "e", "f", "g", "h", "j", "l", "o", "p", "q", "v", "w", "y", "z",
}

def is_valid_word(word: str, min_length: int = 3) -> bool:
    """
    Checks if a word is valid for analysis.
    
    Args:
        word: The word to validate
        min_length: Minimum length for a word to be considered valid
        
    Returns:
        True if word is valid, False otherwise
    """
    if not word or not isinstance(word, str):
        return False
    
    word = word.lower()
    
    # Filter out stopwords
    if word in STOPWORDS:
        return False
    
    # Must be minimum length
    if len(word) < min_length:
        return False
    
    # Must contain at least one letter
    if not any(c.isalpha() for c in word):
        return False
    
    # Filter out pure numbers
    if word.replace(',', '').replace('.', '').isdigit():
        return False
    
    # Filter out repetitive characters (e.g., "hahahaha", "ahhhhh")
    if len(set(word)) <= 2 and len(word) > 3:
        return False
    
    # Filter out words that are mostly non-alphabetic
    alpha_count = sum(c.isalpha() for c in word)
    if alpha_count / len(word) < 0.6:
        return False
    
    return True


def calculate_linguistic_stats(df: pd.DataFrame, top_n: int = 20) -> Dict[str, Any]:
    """
    Calculates linguistic statistics like most common words.

    Args:
        df: The chat DataFrame.
        top_n: The number of top words to return.

    Returns:
        A dictionary containing linguistic statistics.
    """
    if df.empty:
        return {
            "most_common_words": [],
            "most_common_words_per_user": {},
        }
    
    user_df = df[(df["sender"] != "System") & (df["message_type"] == "text")].copy()

    # Pre-process text: lowercase, remove non-alphanumeric, split into words
    words = user_df["message"].str.lower().str.findall(r'\b\w+\b').explode()
    
    # Filter using our validation function
    words = words[words.apply(lambda x: is_valid_word(x))]
    
    # Overall most common words
    most_common_words_counts = Counter(words).most_common(top_n)
    most_common_words = [{"word": word, "count": count} for word, count in most_common_words_counts]

    # Most common words per user
    most_common_words_per_user = {}
    for sender in user_df["sender"].unique():
        sender_words = user_df[user_df["sender"] == sender]["message"].str.lower().str.findall(r'\b\w+\b').explode()
        sender_words = sender_words[sender_words.apply(lambda x: is_valid_word(x))]
        
        counts = Counter(sender_words).most_common(top_n)
        most_common_words_per_user[sender] = [{"word": word, "count": count} for word, count in counts]

    return {
        "most_common_words": most_common_words,
        "most_common_words_per_user": most_common_words_per_user,
    }
