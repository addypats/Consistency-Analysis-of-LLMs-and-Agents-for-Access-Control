import os
import re
import json
import sys
from typing import Dict, Any
from fuzzywuzzy import fuzz
from Levenshtein import distance as levenshtein_distance
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Compare_Metrics:
    def __init__(self):
        pass

    @staticmethod
    def read_file(file_path: str) -> str:
        """
        Read the raw content of a file.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normalize text by lowercasing and trimming whitespace.
        """
        return text.lower().strip()

    @staticmethod
    def jaccard_similarity(text1: str, text2: str) -> float:
        """
        Calculate Jaccard Similarity between two texts.
        """
        set1 = set(text1.split())
        set2 = set(text2.split())
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union != 0 else 0

    @staticmethod
    def cosine_similarity_score(text1: str, text2: str) -> float:
        """
        Calculate Cosine Similarity between two texts using TF-IDF.
        """
        vectorizer = TfidfVectorizer().fit_transform([text1, text2])
        similarity_matrix = cosine_similarity(vectorizer)
        return similarity_matrix[0, 1]

    def compare_configs(self, file1: str, file2: str) -> Dict[str, Any]:
        """
        Compare the raw content of two config files using various similarity metrics.
        """
        text1 = self.normalize_text(self.read_file(file1))
        text2 = self.normalize_text(self.read_file(file2))

        # Levenshtein Similarity
        levenshtein_score = 1 - (levenshtein_distance(text1, text2) / max(len(text1), len(text2)))

        # Jaccard Similarity
        jaccard_score = self.jaccard_similarity(text1, text2)

        # Cosine Similarity
        cosine_score = self.cosine_similarity_score(text1, text2)

        # Fuzzy Matching Score
        fuzzy_score = fuzz.ratio(text1, text2) / 100

        return {
            "Levenshtein Similarity": levenshtein_score,
            "Jaccard Similarity": jaccard_score,
            "Cosine Similarity": cosine_score,
            "Fuzzy Matching Score": fuzzy_score
        }


# if __name__ == "__main__":
#     comparator = EnhancedConfigComparator()
#     file1, file2 = sys.argv[1], sys.argv[2]  # Take file paths as arguments
#     results = comparator.compare_configs(file1, file2)
#     print(json.dumps(results))  # Print results as JSON for piping
