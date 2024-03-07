#!/usr/bin/env python3

from services import services

if __name__ == "__main__":
    for service in services:
        service.clean()
        service.setup()
