from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime
import requests
import time
import os


def stringToDate(str):
    return datetime.datetime.strptime(str, '%d %b %Y')


def season_results(year):
    url = f'https://www.formula1.com/en/results.html/{year}/races.html'

    r = requests.get(url)
    soup = bs(r.content, features='html.parser')

    all_grand_prix = []
    all_grand_prix_urls = []
    all_dates = []
    all_winners_firstname = []
    all_winners_lastname = []
    all_winners_namecode = []
    all_cars = []
    all_lap_counts = []
    all_times = []

    resultsarchive_table = soup.find(
        'table', {'class': 'resultsarchive-table'})

    for row in resultsarchive_table.find('tbody').find_all('tr'):
        tds = row.find_all('td')

        all_grand_prix.append(tds[1].text.strip())

        url = tds[1].find('a')['href']

        all_grand_prix_urls.append(f'https://www.formula1.com{url}')

        all_dates.append(stringToDate(tds[2].text.strip()))

        all_winners_firstname.append(tds[3].text.strip().split('\n')[0])
        all_winners_lastname.append(tds[3].text.strip().split('\n')[1])
        all_winners_namecode.append(tds[3].text.strip().split('\n')[2])
        all_cars.append(tds[4].text.strip())
        all_lap_counts.append(tds[5].text.strip())
        all_times.append(tds[6].text.strip())

    df = pd.DataFrame(columns=[
        'Grand Prix',
        'Grand Prix URL',
        'Grand Prix Date',
        'Winner First Name',
        'Winner Last Name',
        'Winner Name Code',
        'Winning Car',
        'Lap Count',
        'Winning Time'
    ])

    df['Grand Prix'] = all_grand_prix
    df['Grand Prix URL'] = all_grand_prix_urls
    df['Grand Prix Date'] = all_dates
    df['Winner First Name'] = all_winners_firstname
    df['Winner Last Name'] = all_winners_lastname
    df['Winner Name Code'] = all_winners_namecode
    df['Winning Car'] = all_cars
    df['Lap Count'] = all_lap_counts
    df['Winning Time'] = all_times

    soup.decompose()
    return df


def main():
    start = datetime.datetime.now()

    cwd = os.getcwd()

    writer = pd.ExcelWriter(
        f'{cwd}/Formula1_Season_Results.xlsx', engine='xlsxwriter')

    for n in range(1950, 2021):
        season_results(n).to_excel(writer, sheet_name=str(n), index=False)

    writer.save()
    end = datetime.datetime.now()
    print(end - start)


if __name__ == '__main__':
    main()
