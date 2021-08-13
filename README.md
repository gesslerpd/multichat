# multichat

Multicast chat command line application.

## Usage

```
$ pipenv run python multichat.py 224.0.0.0 8080
```

```
$ pipenv run python multichat.py -h
usage: multichat [-h] [--ttl TTL] group_address port

Multicast chat client and server

positional arguments:
  group_address  multicast group address
  port           port number

optional arguments:
  -h, --help     show this help message and exit
  --ttl TTL      multicast time to live (default: 1)

```
