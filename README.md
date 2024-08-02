# Python Content Comparator

## Overview

The HTML Content Comparator is a Python-based tool designed to compare the content of two websites. It fetches, parses, and compares the textual content and structure of two web pages to determine how closely they match. This tool is particularly useful for validating content migration between different versions of web applications.

## Features

- Concurrent fetching of web page content using `aiohttp` and `asyncio`.
- Flexible tolerance-based content comparison.
- Generates detailed CSV reports of the comparisons.
- Supports batch processing of multiple URL pairs.
- Provides a summary report with match percentages.

## Project Structure

- main.py
- fetcher.py
- parseHTML.py
- comparator.py
- saveData.py
- urls.csv # Example input file with URLs
- requirements.txt

## Requirements

- Python 3.7+
- Libraries specified in `requirements.txt`

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/rajrayala/Python-Compare-Content.git
    ```

2. Install the required libraries:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Prepare a `urls.csv` file with the following format:

    ```csv
    URL1,URL2,UseTolerance
    https://example1.com,https://example2.com,yes
    https://example3.com,https://example4.com,no
    ```

    - `URL1` and `URL2`: The URLs of the web pages to compare.
    - `UseTolerance`: Optional; if not specified, defaults to 'yes'.

2. Run the comparator:

    ```sh
    python main.py
    ```

    This will fetch content from the specified URLs, compare the structures, and save the results in a uniquely named directory.

## Output

- Individual comparison results are saved as CSV files in a directory named `results_<timestamp>`.
- Each comparison CSV file includes:
  - `Element 1`: The HTML tag from the first URL.
  - `Content 1`: The textual content from the first URL.
  - `Element 2`: The HTML tag from the second URL.
  - `Content 2`: The textual content from the second URL.
  - `Content Matched`: Whether the contents are considered matched based on the tolerance setting.
- A `final_report.csv` file summarizing the match percentages for all comparisons.

## Example Output

Here is an example of what the output CSV might look like:

```csv
Element 1,Content 1,Element 2,Content 2,Content Matched
html>body>div>h1,Welcome to Example 1,html>body>div>h1,Welcome to Example 2,True
html>body>div>p,This is a test paragraph.,html>body>div>p,This is a test paragraph.,True
...
```csv
Comparison,Match Percentage
Comparison 1,100.0
Average,95.45454545454545
...
