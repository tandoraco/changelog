#!/usr/bin/env bash
git pull
sudo docker-compose -f prod.yml restart
