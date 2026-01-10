from http_client import get_session

url = "https://asmu.ru/schedule/schedule_list.php"

async def get_data(select_type,schedule_date,group):
    session = await get_session()
    payload = {
    "institute": 1,
    "select_type": select_type,
    "schedule_date": schedule_date,
    "group": group
    }
    async with session.post(url, data=payload, headers=session.headers) as resp:
        data = await resp.json()
    schedule = data.get("schedule", [])
    return schedule
