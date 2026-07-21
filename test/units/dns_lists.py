from airvpn import AirVPN

api = AirVPN()
dns_lists = None

@test.unit
def check_service():
    global dns_lists
    dns_lists = api.dns_lists

@test.unit
def check_lists():
    for name, dns in dns_lists.lists.items():
        print(name, dns.description)