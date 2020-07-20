#!/usr/bin/env bash
apt update
apt upgrade
apt install appmenu-gtk3-module
pip3 install -r requirements.txt
sed -i '59i\    window.setFixedSize(width, height)' /usr/local/lib/python3.8/dist-packages/pyfladesk/__init__.py
