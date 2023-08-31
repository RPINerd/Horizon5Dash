'''
    Dummy Telemetry Server | RPINerd 08/29/23
    
    Rethinking the way to handle doing "dry runs" for dev testing.
    
    The main dumping script option will dump the raw binary data packets
    into a pickle file as an iterable
    
    Dummy server simply loops over this list and sends each packet via UDP
    to a provided address/port as if Forza was actually running.
    Also can provide a time delay to wait between packets.
'''

import argparse
import socket


def parse_args():
    

def main(args):

    ip_target = args.ip

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind(())

if __name__ == '__main__':
    args = parse_args()
    main(args)