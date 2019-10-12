

Raw Ping Program in python
= 

Ping hosts using tcp syn packets.

Simple example


    $ ping example.org

    Pinging example.org 4 times on port 80:

    Reply from 93.184.216.34:80 time=7.40 ms
    Reply from 93.184.216.34:80 time=10.31 ms
    Reply from 93.184.216.34:80 time=7.18 ms
    Reply from 93.184.216.34:80 time=6.92 ms

    Ouput:
    --------------------------

    Host: example.org

    Sent: 4 packets
    Received: 4 packets
    Lost: 0 packets (0.00%)

## Notes

- Works on Python 2 and Python 3
- Uses only Python standard library for maximum compatibility


Usage
=====

using the python interpreter

python ping.py
```
ping hosts using tcp syn packets

    Options:
      --version   show program's version number and exit
      -h, --help  show this help message and exit
      -t          ping host until stopped with 'control-c'
      -n COUNT    number of requests to send (default: 4)
      -p PORT     port number to use (default: 80)
      -w TIMEOUT  timeout in seconds to wait for reply
                  (default: 3)
```

Examples
========
```bash
Ping host on port 80

    $ping host

Ping google on port 400

    $synping google.com -p 400

Ping google 3 times with 10 second timeout

    $ping google.com -n 3 -w 10

```