import pandas as pd
import load_datafiles

class Analyzer :
    def __init__(self, csv_path, output_path="samples") :
        self.path = csv_path
        self.df = self._load_csv()
        self.output_path = output_path
        
    def _load_csv(self) -> pd.DataFrame:
        try:
            df = pd.read_csv(self.path)
            return df
        except Exception as e:
            raise RuntimeError(f"fail to load csv: {e}")
        
    def _cleansing_data(self) :
        load_datafiles.check_result_directory(self.df)
        self.success_rate = load_datafiles.check_success_rate(self.df)
        
        confidence_dict = load_datafiles.check_confidence(self.df)
        self.confidence_length_max = confidence_dict["confidence_length_max"]
        self.confidence_offset = confidence_dict["confidence_offset"]
        