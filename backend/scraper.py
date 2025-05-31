import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    return webdriver.Chrome(options=chrome_options)

def add_linkedin_cookie(driver, cookie_value):
    driver.get("https://www.linkedin.com")
    time.sleep(2)
    driver.add_cookie({
        "name": "li_at",
        "value": cookie_value,
        "domain": ".linkedin.com",
        "path": "/",
        "secure": True,
        "httpOnly": True,
        "sameSite": "None"
    })
    driver.get("https://www.linkedin.com/feed/")
    time.sleep(3)

def obter_nome_empresa_e_leads(cookie_value, empresa_url):
    driver = setup_driver()
    add_linkedin_cookie(driver, cookie_value)

    # 1. Ir para a URL da empresa
    driver.get(empresa_url)
    time.sleep(3)

    # 2. Pegar o nome da empresa
    try:
        nome_empresa = driver.find_element(
    By.CLASS_NAME,
        "org-top-card-summary__title"
        ).text.strip()
    except Exception:
        nome_empresa = "Desconhecida"

    # 3. Ir para a aba de "people"
    people_url = empresa_url.rstrip("/") + "/people/?facetGeoRegion=106057199"
    driver.get(people_url)
    time.sleep(5)

    leads = []

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".artdeco-entity-lockup--stacked-center")
            )
        )
        cards = driver.find_elements(By.CSS_SELECTOR, ".artdeco-entity-lockup--stacked-center")[:10]

        for card in cards:
            try:
                nome_el = card.find_element(By.CSS_SELECTOR, ".lt-line-clamp--single-line")
                nome = nome_el.text.strip()

                try:
                    cargo_el = card.find_element(By.CSS_SELECTOR, ".lt-line-clamp--multi-line")
                    cargo = cargo_el.text.strip()
                except:
                    cargo = ""

                try:
                    foto_el = card.find_element(By.CSS_SELECTOR, ".evi-image.lazy-image.ember-view")
                    foto = foto_el.get_attribute("src")
                except:
                    foto = ""

                leads.append({
                    "nome": nome,
                    "cargo": cargo,
                    "foto": foto
                })

            except Exception as e:
                print("Erro ao extrair perfil:", e)
                continue

    except Exception as e:
        print("Erro ao buscar perfis:", e)

    driver.quit()
    return nome_empresa, leads