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
cp $(mkcert -CAROOT)/* .
chmod 664 ./*
```

By the end this folder should contain:
argus-cert.pem
argus-key.pem
rootCA.pem
rootCA-key.pem