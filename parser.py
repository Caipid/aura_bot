import requests
from bs4 import BeautifulSoup


def get_data(select_type,schedule_date,group):
    url = "https://asmu.ru/schedule/schedule_list.php"

    payload = {
    "institute": 1,
    "select_type": select_type,
    "schedule_date": schedule_date,
    "group": group
    }

    headers = {
        "accept":"*/*",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 OPR/125.0.0.0 (Edition Yx GX)"
    }
    response = requests.post(url, data=payload, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    print(soup.find("schedule").text)
def main():
    get_data(2,"10.1.2026","ЛД2404")

if __name__ == '__main__':
    main()