import time
import re
import csv
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By


# ---------------- TELEGRAM ----------------

TOKEN = "8796131370:AAF3Si8rUa_5prVIGedyOa92PlLS7LtpLuY"
CHAT_ID = "1362457827"

def notificar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Erro Telegram:", e)


# ---------------- PEGAR VIEWS ----------------

def pegar_views(driver):
    try:
        body_text = driver.find_element(By.TAG_NAME, "body").text

        match = re.search(r"([\d\.,]+)\s*(views|visualizações)", body_text, re.IGNORECASE)
        if match:
            return match.group(1)

        return None

    except Exception as e:
        print("Erro ao pegar views:", e)
        return None


# ---------------- SALVAR HISTÓRICO ----------------

def salvar_csv(views, diff):
    with open("views_historico.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), views, diff])


# ---------------- MAIN ----------------

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

tweet_url = "https://x.com/pennywwisee/status/2046568090272481322"
driver.get(tweet_url)

time.sleep(5)

ultimo_valor = None

notificar_telegram("teste")
while True:
    try:
        views = pegar_views(driver)

        if views:
            views_num = int(re.sub(r"\D", "", views))

            if ultimo_valor is None:
                ultimo_valor = views_num

            diff = views_num - ultimo_valor

            print(f"Views: {views_num} | +{diff}")

            # salva histórico
            salvar_csv(views_num, diff)

            # alerta normal
            if diff >= 10:
                notificar_telegram(f"📊 +{diff} views (total: {views_num})")
                ultimo_valor = views_num

            # alerta crescimento rápido
            if diff >= 50:
                notificar_telegram(f"🚀 CRESCIMENTO RÁPIDO! +{diff} views")

        else:
            print("Não consegui pegar views")

        time.sleep(10)

    except Exception as e:
        print("Erro no loop:", e)
        time.sleep(5)