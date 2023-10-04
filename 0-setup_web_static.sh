#!/usr/bin/env bash
# Sets up Nginx web server for deployment of web_static

# Install Nginx
apt-get update
apt-get -y install nginx

service nginx start

# Create relevant folders
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Add fake HTML file
cat << EOF > /data/web_static/releases/test/index.html
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOF

# Create symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Change ownership of the  /data directory
chown -hR ubuntu:ubuntu /data

# Update Nginx configuration to serve web_static content
config='\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n'
sed -i "/^\slocation \/ {$/i\ $config" /etc/nginx/sites-available/default

# Apply configuration changes
service nginx restart
