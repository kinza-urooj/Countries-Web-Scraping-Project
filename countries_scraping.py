import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from pathlib import Path

# Website URL
url = "https://www.scrapethissite.com/pages/simple/"

# Create data folder
data_folder = Path("data")
data_folder.mkdir(exist_ok=True)

# Headers
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Create session
session = requests.Session()
session.headers.update(headers)

# Store country data
countries = []

try:
    print("Scraping countries website...")

    # Send request
    response = session.get(url, timeout=30)
    response.raise_for_status()

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all country blocks
    country_blocks = soup.select(".country")

    print("Country blocks found:", len(country_blocks))

    # Extract information
    for block in country_blocks:

        # Country name
        country = block.select_one(".country-name")
        country = country.get_text(strip=True) if country else None

        # Capital
        capital = block.select_one(".country-capital")
        capital = capital.get_text(strip=True) if capital else None

        # Population
        population = block.select_one(".country-population")
        population = population.get_text(strip=True) if population else None

        # Area
        area = block.select_one(".country-area")
        area = area.get_text(strip=True) if area else None

        # Convert population to integer
        if population:
            population = int(population.replace(",", ""))

        # Convert area to float
        if area:
            area = float(area.replace(",", ""))

        # Store record
        country_data = {
            "country": country,
            "capital": capital,
            "population": population,
            "area_km2": area,
            "source_url": url
        }

        countries.append(country_data)

    # Create DataFrame
    df = pd.DataFrame(countries)

    # Save CSV
    csv_path = data_folder / "countries_data.csv"

    df.to_csv(
        csv_path,
        index=False,
        encoding="utf-8-sig"
    )

    # Save JSON
    json_path = data_folder / "countries_data.json"

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(
            countries,
            file,
            indent=4,
            ensure_ascii=False
        )

    # Summary
    print("\n========== COUNTRIES SCRAPING COMPLETED ==========")
    print("Total countries scraped:", len(countries))
    print("CSV saved:", csv_path)
    print("JSON saved:", json_path)

    print("\nFirst 5 countries:")
    print(df.head())

    print("\nProject completed successfully!")

except requests.exceptions.RequestException as error:
    print("Website request error:", error)

except Exception as error:
    print("Error:", error)
    