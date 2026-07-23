import os
import time
import platform

from airvpn import AirVPN

api = AirVPN(os.getenv("API_KEY"))

@test.unit
def check_service():
    print("Sending notification..")
    api.notification.send(f"Test @ {time.ctime()} [Python {platform.python_version()}]", "Test body")
    print("Finished.")