# Note: This script was written by GitHub Copilot (using Claude Sonnet 3.7).
# Every item within the CSV file, has been checked against the original PyCharm generated HTML file.
# I DO NOT claim to have written this code - Matthew Vallance 23/04/2025
# URL: https://github.com/features/copilot
import bs4
import csv
import re
import sys
import os

def extract_test_results(html_file_path, csv_output_path):
    # Read the HTML file content
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Parse the HTML using BeautifulSoup
    soup = bs4.BeautifulSoup(html_content, 'html.parser')
    
    # Initialize a list to store test results
    test_results = []
    
    # Find all test suite elements
    test_modules = soup.find_all('li', {'class': 'level top open'})
    
    for module in test_modules:
        # Extract module name without time
        module_name_elem = module.find('span')
        if module_name_elem:
            full_text = module_name_elem.text.strip()
            # Remove the embedded time that appears at the beginning
            module_name = re.sub(r'^\s*\d+(?:\.\d+)?\s*(?:ms|s)\s*', '', full_text)
        else:
            module_name = "Unknown Module"
        
        # Get the module time separately
        module_time_elem = module.find('div', {'class': 'time'})
        module_time = module_time_elem.text.strip() if module_time_elem else 'N/A'
        
        # Get the test suite name
        suite = module.find('li', {'class': 'level suite open'})
        if suite:
            # Extract suite name without time
            suite_name_elem = suite.find('span')
            if suite_name_elem:
                full_text = suite_name_elem.text.strip()
                # Remove the embedded time
                suite_name = re.sub(r'^\s*\d+(?:\.\d+)?\s*(?:ms|s)\s*', '', full_text)
            else:
                suite_name = module_name
        else:
            suite_name = module_name
        
        # Get all tests within the suite
        tests = suite.find_all('li', {'class': 'level test'}) if suite else []
        
        for test in tests:
            # Extract test name without time and status
            test_name_elem = test.find('span')
            if test_name_elem:
                full_text = test_name_elem.text.strip()
                # Remove time and 'passed' status
                test_name = re.sub(r'^\s*\d+(?:\.\d+)?\s*(?:ms|s)\s*', '', full_text)
                test_name = re.sub(r'passed', '', test_name).strip()
            else:
                test_name = "Unknown Test"
            
            # Get execution time
            time_element = test.find('div', {'class': 'time'})
            execution_time = time_element.text.strip() if time_element else 'N/A'
            
            # Get status
            status_element = test.find('em', {'class': 'status'})
            status = status_element.text.strip() if status_element else 'N/A'
            
            # Get stdout if available (for progress percentage)
            stdout_element = test.find('span', {'class': 'stdout'})
            stdout = stdout_element.text.strip() if stdout_element else ''
            
            # Extract progress percentage
            progress_match = re.search(r'PASSED\s*\[\s*(\d+)%\s*\]', stdout)
            progress = progress_match.group(1) if progress_match else 'N/A'
            
            # Add test result to list
            test_results.append({
                'Module': module_name,
                'Suite': suite_name,
                'Test': test_name,
                'Status': status,
                'Time': execution_time,
                'Progress': progress
            })
    
    # Write results to CSV
    with open(csv_output_path, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Module', 'Suite', 'Test', 'Status', 'Time', 'Progress']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for result in test_results:
            writer.writerow(result)
    
    return len(test_results)

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "Test Results.html"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "test_results.csv"
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    
    test_count = extract_test_results(input_file, output_file)
    print(f"Successfully extracted {test_count} test results to {output_file}")