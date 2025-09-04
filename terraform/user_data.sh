#!/bin/bash
sudo yum update -y
amazon-linux-extras install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create a docker-compose file [cite: 82]
cat <<EOF > /home/ec2-user/docker-compose.yml
services:
  backend:
    image: jiyaa5/backend:latest
    ports:
      - "5000:5000"
    environment:
      - LOGGER_URL=http://logger:5002/log
    depends_on:
      - postgres
      - logger

  frontend:
    image: jiyaa5/frontend:latest
    ports:
      - "8080:80"
    environment:
      - BACKEND_URL=http://backend:5000/api/data
    depends_on:
      - backend

  postgres:
    image: postgres:13
    restart: always
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    volumes:
      - postgres-data:/var/lib/postgresql/data

  logger:
    image: jiyaa5/logger:latest
    ports:
      - "5002:5002"
    volumes:
      - logger-data:/app/logs

volumes:
  postgres-data:
  logger-data:
EOF

# Run docker-compose [cite: 82]
cd /home/ec2-user
sudo /usr/local/bin/docker-compose up -d