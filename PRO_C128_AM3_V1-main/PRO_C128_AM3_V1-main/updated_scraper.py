from selenium import webdriver
browser = webdriver.Chrome()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

urls = [

    'https://exoplanets.nasa.gov/exoplanet-catalog/' 
        
        ]
s = Service(r"C:\Program Files (x86)\chromedriver.exe")

for url in urls:
    driver = webdriver.Chrome(service=s)
    driver.get(url)

# Enlace a NASA Exoplanet
#START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

# Controlador web
#browser = webdriver.Chrome("D:/Setup/chromedriver_win32/chromedriver.exe")
#browser.get(START_URL)

time.sleep(10)

planets_data = []

def scrape():
    for i in range(1,2):
        while True:
            time.sleep(2)

            soup = BeautifulSoup(browser.page_source, "html.parser")

            # Verificar el número de página
            current_page_num = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))

            if current_page_num < i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif current_page_num > i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break

        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")

            # Obtener la etiqueta del hipervínculo
            hyperlink_li_tag = li_tags[0]

            temp_list.append("https://exoplanets.nasa.gov"+ hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            
            planets_data.append(temp_list)

        browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

        print(f"Extracción de datos de la página {i} completada")


# Llamar al método
scrape()

# Definir los encabezados
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink"]

# Definir el dataframe de Pandas
planet_df_1 = pd.DataFrame(planets_data, columns=headers)

# Convertir a CSV
planet_df_1.to_csv('updated_scraped_data.csv',index=True, index_label="id")
