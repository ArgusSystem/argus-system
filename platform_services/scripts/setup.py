from services import services

for service in services:
    service.clean()
    service.setup()
