from __future__ import annotations

import random
from typing import Dict, List

import sqlite3

def build_quiz_questions(vocab: List[sqlite3.Row]) -> List[Dict]:
    """
    Create a randomized multiple-choice question list.
    Each question maps an Arabic term to the correct English term
    with up to 3 distractors.
    """
    indices = list(range(len(vocab)))
    random.shuffle(indices)

    questions: List[Dict] = []
    for idx in indices:
        w = vocab[idx]
        correct = w["term_en"]

        others = [
            v for j, v in enumerate(vocab)
            if j != idx and v["term_en"] != correct
        ]
        random.shuffle(others)
        distractors = [o["term_en"] for o in others[:3]]

        opts = [correct] + distractors
        random.shuffle(opts)

        questions.append(
            {
                "word_idx": idx,
                "options": opts,
                "correct": correct,
            }
        )

    return questions
