import pandas as pd

def save_to_csv(comparison, filename, match_percentage):
    df = pd.DataFrame(comparison)
    df = df[(df['Content 1'] != '') | (df['Content 2'] != '')]  # Exclude rows with empty content
    df.to_csv(filename, index=False)

    # Add match percentage at the end of the CSV file
    with open(filename, 'a') as f:
        f.write(f"\nTotal Match Percentage: {match_percentage:.2f}%\n")
