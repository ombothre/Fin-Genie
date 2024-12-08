import pandas as pd
def extract_metadata(df: pd.DataFrame) -> dict:
    metadata = {}

    # Number of columns
    metadata['Number of Columns'] = df.shape[1]

    # Column names
    metadata['Schema'] = df.columns.tolist()

    # Data types of each column
    metadata['Data Types'] = str(df.dtypes)

    # Summary statistics
    metadata['Sample'] = df.head(1).to_dict(orient="records")

    return metadata