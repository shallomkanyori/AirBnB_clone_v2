# Sets up Nginx web server for deployment of web_static

# Update
exec {'update':
  provider => shell,
  command  => 'sudo apt-get -y update',
  before   => Exec['nginx'],
}

# Install Nginx
exec {'nginx':
  command  => 'sudo apt-get -y install nginx',
  provider => shell,
  before   => Exec['folders1'],
}

# Create relevant folders
exec {'folders1':
  command  => 'mkdir -p /data/web_static/releases/test/',
  provider => shell,
  before   => Exec['folders2'],
}

exec {'folders2':
  command  => 'mkdir -p /data/web_static/shared/',
  provider => shell,
  before   =>  Exec['fake-html'],
}

# Add fake HTML file
$cmd_fhtml = 'cat << EOF > /data/web_static/releases/test/index.html
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOF
'
exec {'fake-html':
  command  => $cmd_fhtml,
  provider => shell,
  before   => Exec['symlink'],
}

# Create a symlink
exec {'symlink':
  command  => 'ln -sf /data/web_static/releases/test/ /data/web_static/current',
  provider => shell,
  before   => Exec['chown_ubuntu'],
}

# Change onwnership of the /data directory
exec {'chown_ubuntu':
  command  => 'chown -hR ubuntu:ubuntu /data',
  provider => shell,
  before   =>  Exec['conf'],
}

$new = '\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n'
$config = "sed -i '/^\\slocation \\/ {$/i\\ ${new}' /etc/nginx/sites-available/default"

# Update configuration
exec {'conf':
  command  => $config,
  provider => shell,
  before   => Exec['nginx_restart'],
}

# Apply configuration changes
exec {'nginx_restart':
  command  => 'sudo service nginx restart',
  provider => shell,
}
