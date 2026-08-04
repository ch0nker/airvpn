from airvpn import WebClient

import os

client = WebClient()
user = None

@test.unit
def login():
    global user
    user = client.login(os.getenv("LOGIN"), os.getenv("PASSWORD"))

@test.unit
def follow():
    assert user.follow(842942), "Failed to follow"

@test.unit
def unfollow():
    assert user.unfollow(842942), "Failed to unfollow"

@test.unit
def edit():
    assert user.edit_profile(website="https://airvpn.chonker.cc"), "Failed to edit profile"
