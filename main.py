#!/usr/bin/env python3
"""It translates a word or a phrase from one language to another using Lingvo Live API"""
import argparse
import asyncio
import os

from client import Client

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='LingCApp is a command line client tool for Lingvo Live API.')
    parser.add_argument('-t', '--timeout', type=float, default=5.0, help='waiting timeout as float seconds')
    parser.add_argument('-n', '--no-cache', action='store_true', help='do not use key cache')
    parser.add_argument(
        '-d', '--direction',
        type=str,
        choices=Client.LANG_CHOICES,
        default=Client.LANG_CHOICES[0],
        help='translation direction',
    )
    parser.add_argument(
        '-k', '--key',
        type=str,
        default=os.getenv('LINGCAPP_API_KEY', ''),
        help='api key, default environment variable LINGCAPP_API_KEY',
    )
    parser.add_argument('words', nargs='+', type=str, help='word or phrase to translate')

    args, _ = parser.parse_known_args()

    print(args)

    handler = Client(args.key, args.direction, *args.words)
    asyncio.run(handler.run('hello'))
