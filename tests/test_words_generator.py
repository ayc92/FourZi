import random
from typing import List
import pytest
import numpy as np
from unittest import mock
from fourzi.types import PhraseToScore, WordMatrix
from fourzi.words_generator import RandomWordsFromFourZiPhrasesGenerator


class TestRandomWordsFromFourZiPhrasesGenerator__pick_random_phrases:
    def test_num_phrases_zero__returns_empty(
        self,
        random_words_from_four_zi_phrases_generator: RandomWordsFromFourZiPhrasesGenerator,
    ) -> None:
        random_phrases = (
            random_words_from_four_zi_phrases_generator._pick_random_phrases(0)
        )
        assert random_phrases == []

    def test_empty_phrases__returns_empty(
        self,
        random_words_from_four_zi_phrases_generator: RandomWordsFromFourZiPhrasesGenerator,
    ) -> None:
        random_words_from_four_zi_phrases_generator._phrases = []
        random_phrases = (
            random_words_from_four_zi_phrases_generator._pick_random_phrases(3)
        )
        assert random_phrases == []

    def test_picks_random_phrases_from_phrases(
        self,
        random_words_from_four_zi_phrases_generator: RandomWordsFromFourZiPhrasesGenerator,
    ) -> None:
        with mock.patch.object(random, "randint", side_effect=[3, 0, 1, 0]):
            random_phrases = (
                random_words_from_four_zi_phrases_generator._pick_random_phrases(4)
            )

        expected = ["一以當十", "一世龍門", "一乾二淨", "一丘之貉"]
        assert random_phrases == expected


class TestRandomWordsFromFourZiPhrasesGenerator__extract_words_from_phrases:
    def test_empty_phrases__returns_empty(
        self,
        random_words_from_four_zi_phrases_generator: RandomWordsFromFourZiPhrasesGenerator,
    ) -> None:
        phrases = (
            random_words_from_four_zi_phrases_generator._extract_words_from_phrases([])
        )
        assert phrases == []

    def test_parses_phrases_into_words(
        self,
        random_words_from_four_zi_phrases_generator: RandomWordsFromFourZiPhrasesGenerator,
    ) -> None:
        phrases = (
            random_words_from_four_zi_phrases_generator._extract_words_from_phrases(
                ["一以當十", "一世龍門", "一乾二淨", "一丘之貉"]
            )
        )
        expected = [
            "一",
            "以",
            "當",
            "十",
            "一",
            "世",
            "龍",
            "門",
            "一",
            "乾",
            "二",
            "淨",
            "一",
            "丘",
            "之",
            "貉",
        ]
        assert phrases == expected


class TestRandomWordsFromFourZiPhrasesGenerator__shuffle_words_from_phrases:
    def test_words_from_phrases_empty__returns_empty(
        self,
        random_words_from_four_zi_phrases_generator: RandomWordsFromFourZiPhrasesGenerator,
    ) -> None:
        words = []
        shuffled = (
            random_words_from_four_zi_phrases_generator._shuffle_words_from_phrases(
                words
            )
        )
        assert shuffled == []

    def test_uses_provided_shuffle_func_to_shuffle_results(
        self,
        random_words_from_four_zi_phrases_generator: RandomWordsFromFourZiPhrasesGenerator,
    ) -> None:
        words = [
            "一",
            "世",
            "龍",
            "門",
            "一",
            "丘",
            "之",
            "貉",
        ]

        shuffled = (
            random_words_from_four_zi_phrases_generator._shuffle_words_from_phrases(
                words
            )
        )
        assert shuffled == list(reversed(words))


class TestRandomWordsFromFourZiPhrasesGenerator__words_list_to_matrix:
    WORDS_LIST = [
        "一",
        "以",
        "當",
        "十",
        "一",
        "世",
        "龍",
        "門",
        "一",
        "乾",
        "二",
        "淨",
        "一",
        "丘",
        "之",
        "貉",
    ]

    @pytest.mark.parametrize(
        "words, matrix_side_size, expected",
        [
            (
                WORDS_LIST,
                4,
                np.array(
                    [
                        [
                            "一",
                            "以",
                            "當",
                            "十",
                        ],
                        [
                            "一",
                            "世",
                            "龍",
                            "門",
                        ],
                        [
                            "一",
                            "乾",
                            "二",
                            "淨",
                        ],
                        [
                            "一",
                            "丘",
                            "之",
                            "貉",
                        ],
                    ]
                ),
            ),
            (
                WORDS_LIST,
                2,
                np.array(
                    [
                        [
                            "一",
                            "以",
                        ],
                        [
                            "當",
                            "十",
                        ],
                        [
                            "一",
                            "世",
                        ],
                        [
                            "龍",
                            "門",
                        ],
                        [
                            "一",
                            "乾",
                        ],
                        [
                            "二",
                            "淨",
                        ],
                        [
                            "一",
                            "丘",
                        ],
                        [
                            "之",
                            "貉",
                        ],
                    ]
                ),
            ),
        ],
        ids=[
            "16_words_4x4",
            "16_words_8x2",
        ],
    )
    def test_turns_words_list_into_ndarray(
        self,
        random_words_from_four_zi_phrases_generator: RandomWordsFromFourZiPhrasesGenerator,
        words: List[str],
        matrix_side_size: int,
        expected: WordMatrix,
    ) -> None:
        matrix = random_words_from_four_zi_phrases_generator._words_list_to_matrix(
            words, matrix_side_size=matrix_side_size
        )
        assert np.array_equal(matrix, expected)


phrase_to_score: PhraseToScore = {
    "一世龍門": 195,
    "一丘之貉": 1443,
    "一乾二淨": 959,
    "一以當十": 167,
    "一刀兩斷": 234,
    "一勞永逸": 1070,
}


@pytest.fixture
def random_words_from_four_zi_phrases_generator() -> RandomWordsFromFourZiPhrasesGenerator:
    # To make it deterministic, let's just make the shuffle a reverse
    reverse_func = lambda lst: lst.reverse()

    return RandomWordsFromFourZiPhrasesGenerator(
        phrase_to_score,
        shuffle_func=reverse_func,
    )
