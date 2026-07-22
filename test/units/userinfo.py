import os

from airvpn import AirVPN

api = AirVPN(os.getenv("API_KEY"))
userinfo = None

@test.unit
def check_request():
    print("Caching service.")
    global userinfo
    userinfo = api.userinfo

@test.unit
def check_user_present():
    print("Checking username.")
    if not userinfo.user:
        return "Expected a user value but got None"
    print("Finished.")