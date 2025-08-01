# Made by Horacio Gonzalez
# Sep 9th, 2024

# The purpose of this script is to scrape all the contents of a webpage containing the Names of the Staff
#   members and their Titles, Roles, or Class Taught. Then the scripts saves all this information to a csv file

# The script should work with all schools that have the Name and Title available in their website.

# To scrape a different school just change the URL before /staff?page_no={}


###########     stuff to add      ################
#   - should I ask for the url? 
#   - should the url be passed as an argument when executing?
#   - maybe excracting the tag 'department'
#   - extracting only STEM related Courses? what about departments?
#   - executable file? mac? windows? terminal based?

import requests
from bs4 import BeautifulSoup
import re
import sys

# Base URL with a placeholder for page numbers
# base_url = 'https://zms.lcps.net/o/zms/staff?page_no={}'
input_url = sys.argv[1]
staff_url = '/staff?page_no={}'
base_url = input_url + staff_url


# Function to scrape a single page
def scrape_page(page_no):
    url = base_url.format(page_no)
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page {page_no}. Status code: {response.status_code}")
        return None, None

    # Parse the page content using BeautifulSoup lib
    soup = BeautifulSoup(response.text, 'html.parser')
    
    staff_list = []
    # Extract staff names and titles/courses from the page
    for staff_card in soup.find_all('div', class_='contact-box'):
        name = staff_card.find('div', class_='name').text.strip()
        title = staff_card.find('div', class_='title').text.strip()
        staff_list.append((name, title))
    
    return staff_list, soup

# Function to extract school name
def extract_school_name(soup):
    # Find the school name in <h1 class="bold"> inside the div with class "name"
    school_name_tag = soup.find('div', class_='name').find('h1', class_='bold')
    
    if school_name_tag:
        school_name = school_name_tag.text.strip()
        # Clean the school name for use in filenames (remove spaces, special characters)
        school_name_clean = re.sub(r'[^a-zA-Z0-9]+', '_', school_name)
        return school_name_clean
    else:
        return "unknown_school"

# Scrape multiple pages
all_staff_list = []
page_no = 1
school_name = None
number_staff = 0

while True:
    staff_data, soup = scrape_page(page_no)
    
    # Extract the school name only on the first page
    if page_no == 1 and not school_name and soup:
        school_name = extract_school_name(soup)

    # If no data is returned, we've likely reached the end of the pages
    if not staff_data:
        break
    
    all_staff_list.extend(staff_data)
    print(f"Scraped page {page_no}")
    page_no += 1  # go to the next page

# Use the school name to create the file
filename = f"{school_name}_staff.csv"

print('\n')

# Print the results
for name, title in all_staff_list:
    print(f"Name: {name}, Title/Course: {title}")
    number_staff += 1


# Save the results to a CSV file
with open(filename, 'w') as f:
    f.write('Name,Title/Course\n')
    for name, title in all_staff_list:
        f.write(f'{name},{title}\n')

print(f"\nScraping completed!        Data saved to {filename} \nTotal pages scraped: {page_no - 1}      Total number of people scraped: {number_staff}\n\n")
