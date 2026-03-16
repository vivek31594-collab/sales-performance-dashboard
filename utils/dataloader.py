import pandas as pd


def load_data(path):
    try:
        # Load dataset safely
        df = pd.read_csv(
            path,
            encoding="latin1",
            on_bad_lines="skip",
            sep=None,
            engine="python"
        )

        # Clean column names
        df.columns = df.columns.str.strip()

        # Standardize column names (replace spaces with dots)
        df.columns = df.columns.str.replace(" ", ".", regex=False)

        # Convert date column safely
        if "Order.Date" in df.columns:
            df["Order.Date"] = pd.to_datetime(df["Order.Date"], errors="coerce")

        return df

    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()


