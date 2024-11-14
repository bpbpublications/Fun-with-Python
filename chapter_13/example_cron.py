import pycron
from datetime import datetime


@pycron.cron("*/1 * * * *")
async def test_call(timestamp: datetime):
    timestamp = datetime.now()
    print(f"Executed at {timestamp}")


if __name__ == "__main__":
    pycron.start()
