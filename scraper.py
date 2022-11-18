from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from time import sleep
from typing import List
import pandas as pd
from os.path import exists

def gen_table(driver : webdriver.Chrome, timeout : int) -> pd.DataFrame:



    try:

        cols = [
        "unidades_desligadas",
        "emprestimo_total",
        "emprestimo_medio",
        "desconto_total",
        "desconto_medio",
        "compra_media",
        "renda_media",
        "taxa_de_juros_media"
        ]


        df = pd.DataFrame([], index=["G1", "G2", "G3"], columns=cols, dtype=float)

        xpath = "//*[@id=\"pvExplorationHost\"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[8]/transform/div/div[2]/div/visual-modern/div/div/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div"
        index_col = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

        # xpath = '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[3]/transform/div/div[2]/div/visual-modern/div/div/div[2]/div[1]/div[3]/div'
        # index_col = driver.find_element(By.XPATH, xpath)

        xpath = '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[3]/transform/div/div[2]/div/visual-modern/div/div/div[2]/div[1]/div[3]/div/*'
        indexes = index_col.find_elements(By.XPATH, xpath)



        index_names = [id.find_element(By.XPATH, f'//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[3]/transform/div/div[2]/div/visual-modern/div/div/div[2]/div[1]/div[3]/div/div[{i + 1}]/div').accessible_name for i, id in enumerate(indexes)]

    
        for i in range(1, 9):

            xpath = f'//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[3]/transform/div/div[2]/div/visual-modern/div/div/div[2]/div[1]/div[4]/div/div/div[{i}]'
            column = driver.find_element(By.XPATH, xpath)
            cells = column.find_elements(By.CLASS_NAME, "pivotTableCellWrap")

            for j, cell in enumerate(cells):

                try:
                    df.at[index_names[j], cols[i - 1]] = float(cell.accessible_name.replace("R$", "").replace(",", "").strip())
                except ValueError:
                    print("Unable to convert 1 value")
                    df.at[index_names[j], cols[i - 1]] = None

        return df
    except NoSuchElementException:

        cols = [
        "unidades_desligadas",
        "emprestimo_total",
        "emprestimo_medio",
        "desconto_total",
        "desconto_medio",
        "compra_media",
        "renda_media",
        "taxa_de_juros_media"
        ]

        df = pd.DataFrame([], index=["G1", "G2", "G3"], columns=cols, dtype=float)

        return df

def startup_proccedures(driver : webdriver.Chrome, timeout : int, ano : int) -> None:

    # passar para a segunda página do dash
    xpath = "//*[@id=\"embedWrapperID\"]/div[2]/logo-bar/div/div/div/logo-bar-navigation/span/button[2]"
    next_key = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    next_key.click()

    xpath = "//*[@id=\"pvExplorationHost\"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[8]/transform/div/div[2]/div/visual-modern/div/div/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div"
    element = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    element.click()

    # selecionando todos os meses
    anos = {
        2019 : 1,
        2020 : 2,
        2021 : 3,
        2022 : 4
    }

    #desleciona 2022
    xpath = '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[4]/transform/div/div[2]/div/visual-modern/div/div/div[2]/div/div[2]/div/div[1]/div/div/div[4]/div/span'
    year_button = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    year_button.click()

    #seleciona ano
    xpath = f'//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[4]/transform/div/div[2]/div/visual-modern/div/div/div[2]/div/div[2]/div/div[1]/div/div/div[{anos[ano]}]/div/span'
    year_button = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    year_button.click()

def get_mun_window(driver : webdriver.Chrome) -> list[WebElement]:
    
    xpath = '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[13]/transform/div/div[2]/div/visual-modern/div/div/div[2]/div/div[2]/div/div[1]/div/div/div'
    return [driver.find_element(By.XPATH, xpath + f'[{i}]/div/span') for i in range(1, 9)]

def generate_df(ano : int) -> pd.DataFrame:

    cols = [
        "ano",
        "municipio",
        "estado",
        "grupo",
        "unidades_desligadas",
        "emprestimo_total",
        "emprestimo_medio",
        "desconto_total",
        "desconto_medio",
        "compra_media",
        "renda_media",
        "taxa_de_juros_media"
    ]
    if exists(f"temp{ano}.csv"):
        df = pd.read_csv(f"temp{ano}.csv", index_col=0)
        
        print(f"Found previous temp file containing {len(df.index)} cities. Last reading at {df.municipio[-1]}")
    else:
        df = pd.DataFrame([], columns=cols, dtype=float)
        print("No temporary file found")

    return df

def get_data(driver : webdriver.Chrome, timeout : int, name : str, estado :str) -> pd.DataFrame:
    
    cols = [
        "ano",
        "municipio",
        "estado",
        "grupo",
        "unidades_desligadas",
        "emprestimo_total",
        "emprestimo_medio",
        "desconto_total",
        "desconto_medio",
        "compra_media",
        "renda_media",
        "taxa_de_juros_media"
    ]

    data = gen_table(driver, timeout)
    data.reset_index(inplace=True)
    data.rename(columns={"index" : "grupo"}, inplace=True)
    data["ano"] = str(ano)
    data["municipio"] = name
    data["estado"] = estado

    data = data[cols]

    return data

def scroll_to_mun(driver : webdriver.Chrome, name : str, timeou : int) -> None:

    window = get_mun_window(driver)
    names = [mun.accessible_name for mun in window]

    while name not in names:

        driver.execute_script("arguments[0].scrollIntoView(true);", window[-1])

        window = get_mun_window(driver)
        names = [mun.accessible_name for mun in window]

    driver.execute_script("arguments[0].scrollIntoView(true);", window[names.index(name)])
        


if __name__ == "__main__":

    # iniciando web driver
    driver = webdriver.Chrome("/usr/local/bin/chromedriver")

    # entrando na página
    url = "https://app.powerbi.com/view?r=eyJrIjoiMzUyODg5YjEtMjQ1Yi00NDZlLWI2MGQtZmQyNGFmZTMyOTQ0IiwidCI6Ijc1YzQ2ZWJhLTFhMzAtNDcxZS04YmQ2LTExZDc4MWU1NWFkMyJ9&pageName=ReportSection8a977849e715fa85312a"
    driver.get(url)

    TIMEOUT = 5
    ano = int(input("Selecione o ano a ser coletado\n"))

    startup_proccedures(driver, TIMEOUT, ano)


    # gerar lista de municípios
    mun_in_view = get_mun_window(driver)
    print(mun_in_view[0].accessible_name)
    mun_names = [mun.accessible_name for mun in mun_in_view]


    df = generate_df(ano)



    while "Zé Doca" not in mun_in_view:

        xpath = "//*[@id=\"pvExplorationHost\"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[13]/transform/div/div[2]/div/visual-modern/div/div/div[2]/div/div[2]/div"
        lista = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, xpath),)
        )
        rows = lista.find_elements(By.CLASS_NAME, "row")

        for row in rows:

            name = row.find_element(By.CLASS_NAME, "slicerText").accessible_name
            

            if name != "Select all" and (name not in df.municipio.to_list()):
                

                driver.execute_script("arguments[0].scrollIntoView(true);", row)
                mun = row.find_element(By.CLASS_NAME, "slicerCheckbox")
                #seleciona municipio
                mun.click()
                sleep(TIMEOUT)
                xpath = "//*[@id=\"pvExplorationHost\"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[13]/transform/div/div[2]/div/visual-modern/div/div/div[2]/div/div[2]/div"
                estados_div = WebDriverWait(driver, TIMEOUT).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                estados = estados_div.find_elements(By.CLASS_NAME, "row")

                if len(estados) > 2:

                    for estado in estados:
                        
                        if estado.accessible_name != "Select all":
                            estado.click()
                            sleep(TIMEOUT)
                            print(f"Getting data for {name}, estado {estado.accessible_name}")
                            data = get_data(driver, TIMEOUT, name, estado)
                            estado.click()
                else:
                    print(f"Getting data for {name}, estado {estados[-1].accessible_name}")
                    data = get_data(driver, TIMEOUT, name, estados[-1])

                df = pd.concat([df, data], ignore_index=True)
                df.drop_duplicates(inplace=True)
                
                # coleta dados e salva em csv
                df.to_csv(f"temp{ano}.csv")


                mun.click()
            else:
                driver.execute_script("arguments[0].scrollIntoView(true);", row)


        # atualiza janela de municipios
        mun_in_view = get_mun_window(driver)
        mun_names = [mun.accessible_name for mun in mun_in_view]


    df.to_csv(f"final_data{ano}.csv")

    driver.close()
    driver.quit()


