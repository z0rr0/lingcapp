#!/usr/bin/env python3
"""It translates a word or a phrase from one language to another using Lingvo Live API"""
import argparse
import asyncio
import os

from app import Handler, Params

if __name__ == '__main__':
    cache_file = os.path.join(os.getenv('HOME'), '.lingcapp.json')

    parser = argparse.ArgumentParser(description='LingCApp is a command line client tool for Lingvo Live API.')
    parser.add_argument('-v', '--verbose', action='store_true', help='debug mode')
    parser.add_argument(
        '-t', '--timeout',
        type=float,
        default=5.0,
        help='waiting timeout as float seconds, default 5.0',
    )
    parser.add_argument(
        '-c', '--cache',
        type=str,
        default=cache_file,
        help='use cache from JSON file, default $HOME/.lingcapp.json',
    )
    parser.add_argument(
        '-d', '--direction',
        type=str,
        choices=Handler.LANG_CHOICES,
        default=Handler.LANG_CHOICES[0],
        help='translation direction',
    )
    parser.add_argument(
        '-k', '--key',
        type=str,
        default=os.getenv('LINGCAPP_API_KEY', ''),
        help='api key, default environment variable LINGCAPP_API_KEY',
    )
    parser.add_argument('words', nargs='+', type=str, help='words to translate')

    args, _ = parser.parse_known_args()
    params = Params(args.key, args.direction, args.timeout, args.cache, args.verbose)

    handler = Handler(params)
    handler.prepare()

    asyncio.run(handler.run(args.words))
