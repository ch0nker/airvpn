from airvpn.web.auth.services.dns import RecordType
from airvpn import WebClient

import os

sequential_search_n = 3
message_recipient = "chonk's test"
follow_id = 66 # AirVPN BOT

client = WebClient()

user = None

port_obj = None
answer_obj = None
record_obj = None
api_obj = None

@test.unit
def login():
    global user
    user = client.login(os.getenv("LOGIN"), os.getenv("PASSWORD"))

@test.unit
def notifications():
    notifs, msgs = user.get_unread_notifications()

    for notification in notifs:
        print(notification.title, notification.content)

    for msg in msgs:
        print(msg.title, msg.message)

@test.unit
def message():
    assert user.send_message(message_recipient, "Message Test", "This is a test."), "Failed to send message"

@test.unit
def follow():
    assert user.follow(follow_id), "Failed to follow"

@test.unit
def unfollow():
    assert user.unfollow(follow_id), "Failed to unfollow"

@test.unit
def edit():
    assert user.edit_profile(website="https://airvpn.chonker.cc"), "Failed to edit profile"

@test.unit
def port_init():
    user.ports

@test.unit
def open_port():
    global port_obj
    port_obj = user.ports.open()

    print(f"Opened port {port_obj.port}")

@test.unit
def edit_port():
    user.ports.edit(port_obj, note="Test note")
    print(f"Edited note: {port_obj.notes}")

@test.unit
def close_port():
    user.ports.close(port_obj)

@test.unit
def sequential_search():
    start_port = user.ports.sequential_search(sequential_search_n)
    print(f"Found {sequential_search_n} sequential ports starting at {start_port}.")

@test.unit
def get_used_ports():
    used_ports = user.ports.get_used_ports()
    print(f"Used ports: {used_ports[:5]}")

@test.unit
def init_devices():
    user.devices

@test.unit
def add_device():
    device = user.devices.add()
    print(f"Device: {device.id}")
    user.devices.delete(device)

@test.unit
def dns_init():
    user.dns

@test.unit
def add_answer():
    global answer_obj
    answer_obj = user.dns.add_answer("example.com")

@test.unit
def add_record():
    global record_obj, answer_obj
    record_obj = user.dns.add_record(answer_obj, RecordType.A, "0.0.0.0")

@test.unit
def remove_record():
    user.dns.remove_record(answer_obj, record_obj)

@test.unit
def remove_answer():
    user.dns.remove_answer(answer_obj)

@test.unit
def dns_lists():
    for dns_list in user.dns.lists:
        print(dns_list.name, dns_list.description)

@test.unit
def api_init():
    user.api

@test.unit
def list_keys():
    print(f"There are {len(user.api.keys)} api keys.")

@test.unit
def add_key():
    global api_obj
    api_obj = user.api.add()

@test.unit
def edit_key():
    user.api.edit(api_obj, "Test")
    print(api_obj.name)

@test.unit
def delete_key():
    user.api.delete(api_obj)

@test.unit
def init_sessions():
    user.sessions

@test.unit
def list_sessions():
    print(f"There are currently {len(user.sessions.sessions)} active sessions.")

