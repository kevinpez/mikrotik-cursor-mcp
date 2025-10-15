#!/bin/bash
# Complete WireGuard VPN Server Setup for AWS EC2
# Optimized based on real-world deployment experience
# MikroTik MCP Server v2.1.1+
set -e

echo "=== Starting WireGuard VPN Server Setup ==="

# Update system and install required packages
echo "[1/7] Updating system and installing packages..."
yum update -y
yum install -y wireguard-tools iptables

# Enable IP forwarding
echo "[2/7] Enabling IP forwarding..."
echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf
sysctl -p

# Generate WireGuard keys
echo "[3/7] Generating WireGuard keys..."
cd /etc/wireguard
wg genkey | tee server_private.key | wg pubkey > server_public.key
chmod 600 server_private.key

# Get the private key
SERVER_PRIVATE_KEY=$(cat server_private.key)

# Generate pre-shared key for extra security
wg genpsk > preshared.key
chmod 600 preshared.key

# Create WireGuard configuration
echo "[4/7] Creating WireGuard configuration..."
cat > /etc/wireguard/wg0.conf <<EOF
[Interface]
Address = 10.13.13.1/24
ListenPort = 51820
PrivateKey = $SERVER_PRIVATE_KEY

# Enable packet forwarding
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -A FORWARD -o %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

# Client peer will be added via MCP
EOF

chmod 600 /etc/wireguard/wg0.conf

# Enable and start WireGuard
echo "[5/7] Starting WireGuard service..."
systemctl enable wg-quick@wg0
systemctl start wg-quick@wg0

# Save configuration for retrieval
echo "[6/7] Saving configuration..."
mkdir -p /home/ec2-user/wireguard-config
cp /etc/wireguard/server_public.key /home/ec2-user/wireguard-config/
cp /etc/wireguard/preshared.key /home/ec2-user/wireguard-config/

cat > /home/ec2-user/wireguard-config/server-info.txt <<EOF
WireGuard Server Configuration
================================
Server Public Key: $(cat /etc/wireguard/server_public.key)
Preshared Key: $(cat /etc/wireguard/preshared.key)
Server VPN IP: 10.13.13.1/24
Client VPN IP: 10.13.13.2/24
Listen Port: 51820

Configuration Commands:
=======================
Retrieve keys:
  sudo cat /etc/wireguard/server_public.key
  sudo cat /etc/wireguard/preshared.key

Add client peer:
  echo '' | sudo tee -a /etc/wireguard/wg0.conf
  echo '[Peer]' | sudo tee -a /etc/wireguard/wg0.conf
  echo 'PublicKey = CLIENT_PUBLIC_KEY' | sudo tee -a /etc/wireguard/wg0.conf
  echo 'PresharedKey = $(cat /etc/wireguard/preshared.key)' | sudo tee -a /etc/wireguard/wg0.conf
  echo 'AllowedIPs = 10.13.13.2/32' | sudo tee -a /etc/wireguard/wg0.conf
  sudo systemctl restart wg-quick@wg0
EOF

chmod 644 /home/ec2-user/wireguard-config/*
chown -R ec2-user:ec2-user /home/ec2-user/wireguard-config

echo "[7/7] WireGuard setup completed successfully!"
echo "Server is ready for client connections."
echo "Retrieve configuration with: sudo cat /home/ec2-user/wireguard-config/server-info.txt"

# Mark completion
echo "WIREGUARD_SETUP_COMPLETE" > /tmp/wireguard-setup.status
date >> /tmp/wireguard-setup.status

