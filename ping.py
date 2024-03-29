






import socket
import time
import sys
import optparse





def get_parsed_args():
    usage = 'usage: %prog host [options]'
    
    parser = optparse.OptionParser(
        description='ping hosts using tcp syn packets',
        usage=usage, version=1
    )
    parser.add_option('-t', action='store_true', default=False,
                      help="ping host until stopped with 'control-c'")
    parser.add_option('-n', dest='count', default=4, type=int,
                      help="number of requests to send (default: %default)")
    parser.add_option('-p', dest='port', default=80, type=int,
                      help="port number to use (default: %default)")
    parser.add_option('-w', dest='timeout', default=3, type=float,
                      help="timeout in seconds to wait for reply \
                        (default: %default)")

    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(2)

    
    (options, args) = parser.parse_args()

    
    if len(args) == 0:
        parser.error('host not informed')
    if len(args) > 1:
        parser.error('incorrect number of arguments')
    if options.port <= 0 or options.port > 65535:
        parser.error('port must be a number between 1 and 65535')
    if options.timeout <= 0:
        parser.error('timeout must be greater than 0')
    if options.count <= 0:
        parser.error('count must be a positive number')
    return (options, args)



def get_ip(host):
    try:
        remote_ip = socket.gethostbyname(host)
    except:
        print('error: unknown host %s' % host)
        sys.exit(1)
    return remote_ip



def ping(host, port, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    init_time = time.time()
    try:
        s.connect((host, port))
    except Exception as ex:
        
        if '22' in str(ex) or 'argument' in str(ex):
            print('error: invalid host %s' % host)
            sys.exit(1)
        
        
        if 'refused' not in str(ex):
            raise(ex)
    end_time = time.time()
    s.close()
    return (end_time - init_time) * 1000



def cli():
    (options, args) = get_parsed_args()
    host = args[0]

    
    rcvd = 0
    sent = 0
    total_time = 0

    
    remote_ip = get_ip(host)

    
    if not options.t:
        print('\nPinging %s %d times on port %d:\n'
              % (host, options.count, options.port))
    else:
        print('\nPinging %s on port %d:\n' % (host, options.port))

    
    try:
        while True:
            try:
                ping_time = ping(remote_ip, options.port, options.timeout)
                sent += 1
                rcvd += 1
                
                if rcvd == 1:
                    min_time = ping_time
                    max_time = ping_time
                
                if ping_time < min_time:
                    min_time = ping_time
                if ping_time > max_time:
                    max_time = ping_time
                
                total_time += ping_time
                print('Reply from %s:%d time=%.2f ms'
                      % (remote_ip, options.port, ping_time))
            except Exception as ex:
                if 'timed out' in str(ex):
                    sent += 1
                    print(
                        'Timed out after ' + str(options.timeout) + ' seconds'
                    )
                else:
                    sent += 1
                    print(ex)
            
            if not options.t:
                if sent == options.count:
                    break
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print('\nAborted.')

    
    if sent == 0:
        sys.exit(1)

    
    if rcvd == 0:
        print("\nDidn't receive any packets...")
        print("Host is probably DOWN or firewalled. Sorry :'(\n")
        sys.exit(1)

    
    print('\nResults')
    print('-' * 26)
    print('\nHost: %s\n' % host)
    print(
        "Sent: %d packets\nReceived: %d packets\n"
        "Lost: %d packets (%.2f%%)\n"
        % (sent, rcvd, sent - rcvd, float(sent - rcvd) / sent * 100)
    )
    print('Min time: %.2f ms\nMax time: %.2f ms\nAverage time: %.2f ms\n'
          % (min_time, max_time, total_time / rcvd))



if __name__ == '__main__':
    cli()
