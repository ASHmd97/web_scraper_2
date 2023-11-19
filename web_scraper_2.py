"""
This script is a web scraper that fetches football match details from the Yallakora website based on the user-provided date.
It utilizes the 'requests' library to make HTTP requests, 'BeautifulSoup' for web scraping, and 'csv' for handling CSV files.

1. The user is prompted to input a date in the format MM/DD/YYYY.
2. The script sends a GET request to the Yallakora website, fetching match details for the specified date.
3. The 'main' function processes the HTML content of the response, extracting information about various football matches.
4. Match details, including championship title, team names, scores, and match time, are stored in a list of dictionaries called 'matches_details'.
5. The 'matches_details' list is then written to a CSV file named 'matches_details.csv' with appropriate headers.

Note: Make sure to have the required libraries installed before running the script. You can install them using:
    - pip install requests
    - pip install beautifulsoup4
"""

import requests
from bs4 import BeautifulSoup
import csv

# User input for the date
date = input("Enter a Date (in the following format MM/DD/YYYY): ")

# Sending a GET request to the Yallakora website with the specified date
response = requests.get(f"https://www.yallakora.com/match-center/?date={date}")

def main(response):
    # Extracting HTML content
    src = response.content
    soup = BeautifulSoup(src, "lxml")
    matches_details = []

    # Finding all match cards on the webpage
    championships = soup.find_all("div", {'class': 'matchCard'})
    
    def get_match_info(championships):
        """
        Extracts information about each match in a given championship and appends it to the 'matches_details' list.
        Args:
        - championships: List of HTML elements representing match cards for a specific championship.
        """
        
        # get Championship Type
        champion_title = championships.contents[1].find("h2").text.strip()
        
        # get all matches at that date
        all_matches = championships.contents[3].find_all("div", {'class': 'liItem'})
        num_of_matches = len(all_matches)

        for i in range(num_of_matches):
            # get teams names
            teamA = all_matches[i].find("div", {"class": "teamA"}).text.strip()
            teamB = all_matches[i].find("div", {"class": "teamB"}).text.strip()
            
            # get score
            m_result = all_matches[i].find("div", {"class": "MResult"}).find_all('span', {"class": "score"})
            score = f"{m_result[0].text} - {m_result[1].text}"
            
            # get match time
            m_time = all_matches[i].find("div", {"class": "MResult"}).find('span', {"class": "time"}).text
            
            # Appending match details to the list
            matches_details.append({
                "Championship Type": champion_title,
                "Team A": teamA,
                "Result": score,
                "Team B": teamB,
                "Time": m_time
            })

    # Iterating through each championship and extracting match details
    for i in range(len(championships)):
        get_match_info(championships[i])

    # Writing match details to a CSV file
    keys = matches_details[0].keys()
    with open("D:\Python-Project\codezilla\web_scraper_2/matches_details.csv", 'w', encoding='utf-8', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(matches_details)
        print("file created")

# Running the main function
main(response)
