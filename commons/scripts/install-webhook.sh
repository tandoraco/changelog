#!/usr/bin/env bash
wget https://dl.google.com/go/go1.11.4.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.11.4.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
go get github.com/adnanh/webhook
~/go/bin/webhook
mkdir ~/webhooks
mkdir ~/webhooks/tandora-production
cp ~/tandora-backend/commons/scripts/hooks.json ~/webhooks/tandora-production/hooks.json
cp ~/tandora-backend/commons/scripts/deploy.sh ~/webhooks/tandora-production/deploy.sh
chmod +x ~/webhooks/tandora-production/deploy.sh
~/go/bin/webhook -hooks ~/webhooks/hooks.json -ip "000.000.000.000" -verbose
