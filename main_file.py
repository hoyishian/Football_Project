from bs4 import BeautifulSoup
import requests
import pandas as pd
import pathlib

from os.path import basename



headers = {'User-Agent':
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

url = "https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1"

tree = requests.get(url, headers=headers)
soup = BeautifulSoup(tree.content, 'html.parser')

# Create an empty list to assign these values to
teamLinks = []

# Extract all links with the correct CSS selector
links = soup.select("a.vereinprofil_tooltip")

# We need the location that the link is pointing to, so for each link, take the link location.
# Additionally, we only need the links in locations 1,3,5,etc. of our list, so loop through those only
for i in range(1, 41, 2):
    teamLinks.append(links[i].get("href"))

# For each location that we have taken, add the website before it - this allows us to call it later
for i in range(len(teamLinks)):
    teamLinks[i] = "https://www.transfermarkt.co.uk" + teamLinks[i]

playerLinks = []
newPlayerLinks = []

for i in range(len(teamLinks)):
    page = teamLinks[i]
    tree = requests.get(page, headers=headers)
    soup = BeautifulSoup(tree.content, 'html.parser')

    # Extract all links
    links = soup.select("a.spielprofil_tooltip")

    # For each link, extract the location that it is pointing to
    for j in range(len(links)):
        playerLinks.append(links[j].get("href"))

    # Add the location to the end of the transfermarkt domain to make it ready to scrape
for j in range(len(playerLinks)):
    playerLinks[j] = "https://www.transfermarkt.co.uk"+ playerLinks[j]

# The page list the players more than once - let's use list(set(XXX)) to remove the duplicates
playerLinks = list(set(playerLinks))


# page = playerLinks[0]
# tree = requests.get(page, headers=headers)
# soup = BeautifulSoup(tree.content, 'html.parser')
#
# name = soup.find_all("h1")
# value = soup.select("span.waehrung")
# value1 = soup.find_all("span", class_="hauptpunkt")
# print(value1[0].a.text)

# print(value1)
# print(value[0].text)
# print(value[0].next_sibling)
# print(value[1].text)


# tempValue = soup.find_all("div", class_="dataMarktwert")
# print(tempValue[0])
# print(tempValue[0].a.span.text)
# print(tempValue[0].a.span.next_sibling)
# print(tempValue[0].a.span.next_sibling.next_sibling.text)

nameList = []
club = []
currency = []
value = []

# for i in range(len(playerLinks)):
#     page = playerLinks[i]
#     tree = requests.get(page, headers=headers)
#     soup = BeautifulSoup(tree.content, 'html.parser')
#
#     try:
#         tempValue = soup.find_all("div", class_="dataMarktwert")
#         currency.append(tempValue[0].a.span.text)
#     except IndexError:
#         continue
#     try:
#         tempValue = soup.find_all("div", class_="dataMarktwert")
#         value.append(float(tempValue[0].a.span.next_sibling))
#     except IndexError:
#         currency.pop()
#         continue
#
#     try:
#         tempValue = soup.find_all("div", class_="dataMarktwert")
#         denom.append(tempValue[0].a.span.next_sibling.next_sibling.text)
#     except IndexError:
#         currency.pop()
#         value.pop()
#         continue
#
#     try:
#         tempValue = soup.find_all("div", class_="dataMarktwert")
#         total_value.append(tempValue[0].a.span.text + str(tempValue[0].a.span.next_sibling) + tempValue[0].a.span.next_sibling.next_sibling.text)
#     except IndexError:
#         currency.pop()
#         value.pop()
#         denom.pop()
#         continue
#     try:
#         tempClub = soup.find_all("span", class_="hauptpunkt")
#         club.append(tempClub[0].a.text)
#     except IndexError:
#         currency.pop()
#         value.pop()
#         denom.pop()
#         total_value.pop()
#         continue
#     try:
#         name = soup.find_all("h1")
#         nameList.append(name[0].text)
#     except IndexError:
#         currency.pop()
#         value.pop()
#         denom.pop()
#         total_value.pop()
#         club.pop()
#         continue
#
# print(len(nameList))
# print(len(club))
# print(len(currency))
# print(len(value))
# print(len(denom))
# print(len(total_value))

for i in range(len(playerLinks)):
    page = playerLinks[i]
    tree = requests.get(page, headers=headers)
    soup = BeautifulSoup(tree.content, 'html.parser')
    try:
        tempValue = soup.find_all("div", class_="dataMarktwert")
        currency.append(tempValue[0].a.span.text)
    except IndexError:
        continue
    try:
        tempValue = soup.find_all("div", class_="dataMarktwert")
        value.append(float(tempValue[0].a.span.next_sibling))
    except IndexError:
        currency.pop()
        continue
    try:
        tempValue = soup.find_all("div", class_="dataMarktwert")
        denom = tempValue[0].a.span.next_sibling.next_sibling.text
        if denom == 'm':
            value[-1] = value[-1] * 1000000
        elif denom == "Th.":
            value[-1] = value[-1] * 1000
        else:
            value[-1] = value[-1]
    except IndexError:
        currency.pop()
        value.pop()
        continue
    try:
        tempClub = soup.find_all("span", class_="hauptpunkt")
        club.append(tempClub[0].a.text)
    except IndexError:
        currency.pop()
        value.pop()
        continue
    try:
        name = soup.find_all("h1")
        nameList.append(name[0].text)
    except IndexError:
        currency.pop()
        value.pop()
        club.pop()
        continue


columns = ['Name', 'Club', 'Currency', 'Value']
zippedList = list(zip(nameList, club, currency, value))
newdf = pd.DataFrame(zippedList, columns = columns)

currentPath = str(pathlib.Path(__file__).parent.absolute())
currentPath = currentPath + "/marketvalue.csv"
newdf.to_csv(currentPath, index = False)
print(currentPath)