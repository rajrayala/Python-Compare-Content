import os
import pandas as pd
from datetime import datetime
from fetcher import fetch_content
from parseHTML import parse_and_flatten_html
from comparator import compare_structures
from saveData import save_to_csv
from bs4 import BeautifulSoup
import asyncio

async def main():
    input_file = 'urls.csv'
    url_data = pd.read_csv(input_file)
    
    # Create a unique directory for this run
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"results_{current_time}"
    os.makedirs(output_dir, exist_ok=True)

    total_match_percentage = []

    tasks = []
    for index, row in url_data.iterrows():
        url1 = row['URL1']
        url2 = row['URL2']
        use_tolerance = str(row.get('UseTolerance', 'yes')).strip().lower() != 'no'  # Default to 'yes' if not specified

        tasks.append((index, url1, url2, use_tolerance, output_dir))

    results = await asyncio.gather(*[compare_urls(index, url1, url2, use_tolerance, output_dir) for index, url1, url2, use_tolerance, output_dir in tasks])

    for match_percentage in results:
        if match_percentage is not None:
            total_match_percentage.append(match_percentage)

    # Generate final report
    if total_match_percentage:
        final_report_filename = f"{output_dir}/final_report.csv"
        avg_match_percentage = sum(total_match_percentage) / len(total_match_percentage)
        final_report_data = {
            'Comparison': [f"Comparison {i + 1}" for i in range(len(total_match_percentage))],
            'Match Percentage': total_match_percentage
        }
        final_report_df = pd.DataFrame(final_report_data)
        final_report_df.loc['Average'] = ['Average', avg_match_percentage]
        final_report_df.to_csv(final_report_filename, index=False)
        
        print(f"Final report saved to {final_report_filename}")
        print(f"Average match percentage: {avg_match_percentage:.2f}%")

async def compare_urls(index, url1, url2, use_tolerance, output_dir):
    print(f"Starting comparison for {url1} and {url2}...")

    content1, content2 = await asyncio.gather(fetch_content(url1), fetch_content(url2))

    if content1 and content2:
        print("Parsing HTML content...")
        soup1 = BeautifulSoup(content1, 'html.parser')
        soup2 = BeautifulSoup(content2, 'html.parser')

        flat_structure1 = parse_and_flatten_html(soup1)
        flat_structure2 = parse_and_flatten_html(soup2)

        print("Comparing content...")
        comparison, match_count, mismatch_count = compare_structures(flat_structure1, flat_structure2, use_tolerance)
        
        total_elements = match_count + mismatch_count
        match_percentage = (match_count / total_elements) * 100 if total_elements > 0 else 0

        # Create a unique filename with the current date and time
        filename = f"{output_dir}/comparison_{index + 1}.csv"
        
        print("Saving results...")
        save_to_csv(comparison, filename, match_percentage)
        
        print(f"Total match percentage: {match_percentage:.2f}%")
        print(f"Comparison results saved to {filename}")

        return match_percentage
    else:
        print(f"Failed to fetch content from {url1} or {url2}.")
        return None

if __name__ == "__main__":
    asyncio.run(main())
