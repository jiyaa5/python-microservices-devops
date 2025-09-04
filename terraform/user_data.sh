#!/bin/bash
# Update OS & install Docker + Docker Compose
yum update -y
amazon-linux-extras install docker -y
service docker start
usermod -a -G docker ec2-user

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Copy docker-compose.yml (optional: pull from GitHub)
cd /home/ec2-user
curl -O https://raw.githubusercontent.com/jiyaa5/python-microservices-devops/main/docker-compose.yml

# Start the stack
docker-compose up -d
