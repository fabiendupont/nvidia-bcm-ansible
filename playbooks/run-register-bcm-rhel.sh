#!/bin/bash
# Quick script to register bcm-rhel VM with BCM and deploy BCM Agent

set -e

PLAYBOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "========================================="
echo "BCM Registration and Agent Deployment"
echo "========================================="
echo ""
echo "This will:"
echo "  1. Install Podman on bcm-rhel (10.141.255.253)"
echo "  2. Register bcm-rhel as a node in BCM"
echo "  3. Deploy BCM Agent via Quadlet/Podman"
echo ""
read -p "Press Enter to continue or Ctrl+C to abort..."
echo ""

cd "$PLAYBOOK_DIR"

echo "Running playbook..."
ansible-playbook \
  -i bcm-rhel-inventory.yml \
  register-bcm-rhel.yml

echo ""
echo "========================================="
echo "Deployment Complete!"
echo "========================================="
