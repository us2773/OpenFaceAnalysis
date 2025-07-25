import pandas as pd
import load_datafiles
import os
import glob

class Analyzer :
    def __init__(self, csv_path, output_path="samples") :
        self.path = csv_path
        self.au_df = self._load_au_csv()
        self.fatigue_df = self._load_fatigue_csv()
        self.output_path = output_path
        
    def _load_au_csv(self) -> pd.DataFrame:
        try:
            df = pd.read_csv(self.path)
            return df
        except Exception as e:
            raise RuntimeError(f"fail to load csv: {e}")
        
    def _load_fatigue_csv(self) -> pd.DataFrame :
        pass
        
    def _cleansing_data(self) :
        load_datafiles.check_result_directory(self.au_df)
        self.success_rate = load_datafiles.check_success_rate(self.au_df)
        
        confidence_dict = load_datafiles.check_confidence(self.au_df)
        self.confidence_length_max = confidence_dict["confidence_length_max"]
        self.confidence_offset = confidence_dict["confidence_offset"]