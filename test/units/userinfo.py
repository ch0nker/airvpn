import os

from airvpn import AirVPN

api = AirVPN(os.getenv("API_KEY"))
userinfo = None

@test.unit
def check_request():
    global userinfo
    userinfo = api.userinfo

@test.unit
def check_user_present():
    if not userinfo.user:
        return "Expected a user value but got None"