# Enabling SSL/TLS for Argus platform and services

Follow these steps to enable SSL/TLS encryption on Argus-web

# Install

Follow current installation instructions for homebrew.
At this time, the steps for Linux are:

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
test -d ~/.linuxbrew && eval "$(~/.linuxbrew/bin/brew shellenv)"
test -d /home/linuxbrew/.linuxbrew && eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
echo "eval \"\$($(brew --prefix)/bin/brew shellenv)\"" >> ~/.bashrc
```

Then run:

```
sudo apt install libnss3-tools
brew install mkcert
```

To configure a local trusted certificate authority and certificates for localhost plus any other needed hostnames (argus-web, argus, etc.) run:

```
mkcert -install
mkcert -cert-file argus-cert.pem -key-file argus-key.pem localhost argus-web argus
cp ($mkcert -CAROOT)/* .
chmod 664 ./*
```

# Configure for argus-web

Make sure the configure file at web/development.yml includes at root level:

```
server:
  ssl_cert_path: '../ssl/argus-cert.pem'      #set to null to disable ssl
  ssl_key_path: '../ssl/argus-key.pem'   #set to null to disable ssl
```


Make sure the configure file at web/api/development.yml includes at root level:

```
ssl:
  certfile: '../../ssl/argus-cert.pem'      # set to null to disable ssl
  keyfile: '../../ssl/argus-key.pem'   # set to null to disable ssl
```