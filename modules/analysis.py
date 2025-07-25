import pandas as pd

class Analyzer :
    def __init__(self, csv_path) :
        self.path = csv_path
        self.df = self._load_csv()
        
    def _load_csv(self) -> pd.DataFrame:
        try:
            df = pd.read_csv(self.path)
            return df
        except Exception as e:
            raise RuntimeError(f"fail to load csv: {e}")