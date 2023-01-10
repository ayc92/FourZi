from abc import ABC, abstractmethod
import pandas as pd

from fourzi.types import PhraseToScore


class PhrasesLoader(ABC):
    @abstractmethod
    def load_phrases(self) -> PhraseToScore:
        ...


class XlsxPhrasesLoader(PhrasesLoader):
    _xlsx_file_path: str

    def __init__(self, xlsx_file_path: str) -> None:
        self._xlsx_file_path = xlsx_file_path

    def load_phrases(self) -> PhraseToScore:
        phrases_df = self._read_excel()
        return self._phrase_to_score_map(phrases_df)

    def _read_excel(self) -> pd.DataFrame:
        return pd.read_excel(self._xlsx_file_path)

    def _phrase_to_score_map(self, phrases_df: pd.DataFrame) -> PhraseToScore:
        phrases = pd.Series(phrases_df.Complete)
        scores = pd.Series(phrases_df.TotScr)

        return dict(zip(phrases, scores))
