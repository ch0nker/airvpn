from airvpn.web import WebClient
from airvpn.web.user import WebUser

import os

client = WebClient()
user = None

@test.unit
def login():
    global user
    user = client.login(os.getenv("LOGIN"), os.getenv("PASSWORD"))

@test.unit
def follow():
    assert user.follow(65), "Failed to follow"

@test.unit
def unfollow():
    user.unfollow(65)

@test.unit
def edit():
    user.edit_profile(website="https://airvpn.chonker.cc")