# AWS renew IAM access key

## Installation

### Clone and install

By using git, and keeping the repo up to date:
```
git clone git@github.com:Ezka77/renew-aws-access-key.git
cd renew-aws-access-key
pip3 install --user -e .
```

To update use `git pull`

### Direct install

Or by using pip
```
pip3 install --user git+https://github.com/Ezka77/renew-aws-access-key
```
and to update: 
```
pip3 install --user --upgrade git+https://github.com/Ezka77/renew-aws-access-key
```

## Usage

In a terminal:
```
$ aws_renew_access_key
```

## Crontab ... almost

### Systemd

Copy files from `service` to `~/.config/systemd/user/` and enable the timer:

```
systemctl --user daemon-reload

# Optional: renew your key
systemctl --user start aws_key_renew.service

# add a timer: the renew is done monthly
systemctl --user enable aws_key_renew.timer

# check the timer
systemctl --user list-timers
```
