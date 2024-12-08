import pandas as pd
from helpers.metadat import extract_metadata

class File:
    def __init__(self, path: str):
        self.data: pd.DataFrame | None = None
        if path.split('.')[1] == 'csv':
            self.data = pd.read_csv(path)
        else:
            self.data = pd.read_excel(path)
        self.meta = extract_metadata(self.data)