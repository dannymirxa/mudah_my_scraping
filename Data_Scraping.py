import sys
sys.setrecursionlimit(100000)

import httpx
from dataclasses import dataclass
from bs4 import BeautifulSoup as bs
import polars as pl
import os

@dataclass
class Property:
    House : str
    Price : str
    Location : str
    Category : str
    Size : str
    Bedroom : str
    Bathroom : str    
    
def get_html(page):
    url = f"https://www.mudah.my/kuala-lumpur/properties-for-rent?o={page}"
    resp = httpx.get(url)
    return bs(resp.text, 'html.parser')

def parse_properties(html):
    house_catalogues = html.find_all("div", class_ = "sc-ktHwxA iXsADi")
    results = []
    for catalogue in house_catalogues:
        bedroom = None
        bathroom = None
        try:
            bedroom = catalogue.find("div", {"title" : "Bedrooms"}).div.string
        except AttributeError:
            pass
        try:
            bedroom = catalogue.find("div", {"title" : "Bathrooms"}).div.string
        except AttributeError:
            pass

        properties = Property(
            House = catalogue.find("a")["title"],
            Location = catalogue.find("span", class_="sc-uJMKN fgsfIN").string,
            Price = catalogue.find("div", class_="sc-jtRfpW eAwSpO").string,
            Category = catalogue.find("div", class_="sc-dfVpRl eigVMP").string,
            Size = catalogue.find("div", {"title" : "Size"}).div.string,
            Bedroom = bedroom,
            Bathroom = bathroom
            )
        results.append(properties)
    return results

def create_result():
    res_result = []
    for page_number in range (1,10):
        html = get_html(page_number)
        res = parse_properties(html)
        res_result.extend(res)
    df = pl.DataFrame(res_result)
    df.write_csv(os.getcwd() + '/new_result.csv')
    
def main():
    create_result()
    
if __name__ == "__main__":
    main()