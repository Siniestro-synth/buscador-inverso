import json, time, random, logging, os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import urllib.robotparser

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def can_fetch(url, user_agent):
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = urllib.robotparser.RobotFileParser()
    try:
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception as e:
        logging.warning(f"No pude leer robots.txt de {robots_url}: {e}")
        return True  # si falla, dejar al usuario decidir (cuidado)

def extract_field(el, selector, base_url):
    # selector puede ser "a@href" para obtener atributo href
    if "@" in selector:
        sel, attr = selector.split("@", 1)
        found = el.select_one(sel)
        if found and found.has_attr(attr):
            return urljoin(base_url, found[attr].strip())
        return ""
    else:
        found = el.select_one(selector)
        return found.get_text(" ", strip=True) if found else ""

def scrape_page(url, config_domain):
    headers = {"User-Agent": config_domain.get("user_agent")}
    try:
        r = requests.get(url, headers=headers, timeout=12)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        listings = soup.select(config_domain["listing_selector"])
        results = []
        for l in listings:
            item = {}
            for field, sel in config_domain["fields"].items():
                item[field] = extract_field(l, sel, url)
            item["fuente"] = url
            results.append(item)
        return results
    except Exception as e:
        logging.error(f"Error scrapeando {url}: {e}")
        return []

def main():
    cfg = json.load(open("config.json", encoding="utf-8"))
    ua = cfg.get("user_agent", "Mozilla/5.0")
    delay_min = cfg.get("delay_min", 1.0)
    delay_max = cfg.get("delay_max", 2.5)
    all_props = []

    for domain in cfg["domains"]:
        domain_cfg = {
            "listing_selector": domain["listing_selector"],
            "fields": domain["fields"],
            "user_agent": ua
        }
        for page in domain.get("pages", []):
            logging.info(f"Procesando {page}")
            if not can_fetch(page, ua):
                logging.warning(f"robots.txt impide scraping de {page}. Saltando.")
                continue

            if domain.get("use_selenium"):
                # aquí podrías integrar Selenium si el contenido es dinámico
                logging.info("use_selenium=True no implementado en este snippet")
                # Implementar fallback con Selenium si hace falta
            else:
                results = scrape_page(page, domain_cfg)
                all_props.extend(results)

            time.sleep(random.uniform(delay_min, delay_max))

    out = cfg.get("output", "script.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(all_props, f, ensure_ascii=False, indent=2)
    logging.info(f"Guardadas {len(all_props)} propiedades en {out}")

if __name__ == "__main__":
    main()
