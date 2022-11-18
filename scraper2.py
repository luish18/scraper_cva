from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from time import sleep
import pandas as pd
from os.path import exists

def get_table(driver : webdriver.Chrome) -> pd.DataFrame:



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
        index_col = WebDriverWait(driver, WAI_TIMES).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

        xpath = '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[3]/transform/div/div[2]/div/visual-modern/div/div/div[2]/div[1]/div[3]/div'
        index_col = driver.find_element(By.XPATH, xpath)

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
    
WAI_TIMES = 5

if __name__ == "__main__":

    # iniciando web driver
    driver = webdriver.Chrome("/usr/local/bin/chromedriver")

    # entrando na página
    url = "https://app.powerbi.com/view?r=eyJrIjoiMzUyODg5YjEtMjQ1Yi00NDZlLWI2MGQtZmQyNGFmZTMyOTQ0IiwidCI6Ijc1YzQ2ZWJhLTFhMzAtNDcxZS04YmQ2LTExZDc4MWU1NWFkMyJ9&pageName=ReportSection8a977849e715fa85312a"
    driver.get(url)

    # passar para a segunda página do dash
    xpath = "//*[@id=\"embedWrapperID\"]/div[2]/logo-bar/div/div/div/logo-bar-navigation/span/button[2]"
    next_key = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    next_key.click()


    # selecionando todos os meses
    xpath = "//*[@id=\"pvExplorationHost\"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[8]/transform/div/div[2]/div/visual-modern/div/div/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div"
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    element.click()

    sleep(WAI_TIMES)
    anos = {
        2019 : 1,
        2020 : 2,
        2021 : 3,
        2022 : 4
    }

    ano = int(input("Selecione o ano a ser coletado\n"))

    #desleciona 2022
    xpath = '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[4]/transform/div/div[2]/div/visual-modern/div/div/div[2]/div/div[2]/div/div[1]/div/div/div[4]/div/span'
    year_button = driver.find_element(By.XPATH, xpath)
    year_button.click()

        #desleciona 2022
    xpath = f'//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[4]/transform/div/div[2]/div/visual-modern/div/div/div[2]/div/div[2]/div/div[1]/div/div/div[{anos[ano]}]/div/span'
    year_button = driver.find_element(By.XPATH, xpath)
    year_button.click()

    sleep(WAI_TIMES)

    # gerar lista de municípios
    mun_in_view = [driver.find_element(By.XPATH, f'//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[13]/transform/div/div[2]/div/visual-modern/div/div/div[2]/div/div[2]/div/div[1]/div/div/div[{i}]/div/span').accessible_name for i in range(1, 9)]

    cols = [
        "ano",
        "municipio",
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
        print("Found previous temp file")
    else:
        df = pd.DataFrame([], columns=cols, dtype=float)



    while "Zé Doca" not in mun_in_view:

        xpath = "//*[@id=\"pvExplorationHost\"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[13]/transform/div/div[2]/div/visual-modern/div/div/div[2]/div/div[2]/div"
        lista = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
        )
        rows = lista.find_elements(By.CLASS_NAME, "row")

        for row in rows:
            try:
                name = row.find_element(By.CLASS_NAME, "slicerText").accessible_name
                

                if name != "Select all" and (name not in df.municipio.to_list()):
                    
                    driver.execute_script("arguments[0].scrollIntoView(true);", row)
                    mun = row.find_element(By.CLASS_NAME, "slicerCheckbox")
                    #seleciona municipio
                    mun.click()
                    
                    sleep(WAI_TIMES)
                    # coleta dados e salva em csv
                    print(f"Getting data for {name}")
                    data = get_table(driver)
                    data.reset_index(inplace=True)
                    data.rename(columns={"index" : "grupo"}, inplace=True)
                    data["ano"] = str(ano)
                    data["municipio"] = name

                    data = data[cols]

                    df = pd.concat([df, data], ignore_index=True)
                    df.drop_duplicates(inplace=True)

                    df.to_csv(f"temp{ano}.csv")


                    mun.click()
                else:
                    driver.execute_script("arguments[0].scrollIntoView(true);", row)

            except StaleElementReferenceException:
                pass


        # atualiza janela de municipios
        sleep(0.1)
        mun_in_view = [driver.find_element(By.XPATH, f'//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[13]/transform/div/div[2]/div/visual-modern/div/div/div[2]/div/div[2]/div/div[1]/div/div/div[{i}]/div/span').accessible_name for i in range(1, 9)]


    df.to_csv(f"final_data{ano}.csv")

    driver.close()
    driver.quit()


