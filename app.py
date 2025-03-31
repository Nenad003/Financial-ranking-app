import pandas as pd
from flask import Flask, request, render_template

app = Flask(__name__)

def apply_investing_criteria(df):
    try:
        # Standardize column names: strip spaces, convert to lowercase, replace spaces with underscores
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

        # Define required columns (also converted to lowercase with underscores)
        required_columns = {"roe", "debt_to_equity", "roce", "peg_ratio"}
        missing = required_columns - set(df.columns)

        if missing:
            raise KeyError(f"Missing columns in CSV: {missing}")

        # Apply filtering criteria
        df_filtered = df[
            (df["roe"] > 12) &
            (df["debt_to_equity"] < 0.5) &
            (df["roce"] > 15) &
            (df["peg_ratio"] < 1)
        ]
        return df_filtered

    except Exception as e:
        print(f"⚠️ Error in apply_investing_criteria: {e}")  # Debugging output
        raise e  # Rethrow the error to show in Flask logs

@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        if request.method == 'POST':
            if 'file' not in request.files:
                return "⚠️ No file part", 400  # No file uploaded
            
            file = request.files['file']
            if file.filename == '':
                return "⚠️ No selected file", 400  # No file chosen
            
            try:
                df = pd.read_csv(file, encoding='utf-8')  # Read CSV with encoding
            except Exception as e:
                return f"⚠️ Error reading CSV file: {e}", 400
            
            df_filtered = apply_investing_criteria(df)  # Apply filters
            return df_filtered.to_html()

    except Exception as e:
        print(f"⚠️ Error in home route: {e}")  # Debugging output
        return f"❌ Internal Server Error: {e}", 500  # Show error on page
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
