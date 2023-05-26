# LingCApp

This is a simple python client for [Lingvo Live API](https://www.lingvolive.com/). 

## Usage

```
python3 main.py --help

usage: main.py [-h] [-v] [-t TIMEOUT] [-c CACHE] [-d {auto,en-ru,ru-en}] [-k KEY] words [words ...]

LingCApp is a command line client tool for Lingvo Live API.

positional arguments:
  words                 words to translate

options:
  -h, --help            show this help message and exit
  -v, --verbose         debug mode
  -t TIMEOUT, --timeout TIMEOUT
                        waiting timeout as float seconds, default 5.0
  -c CACHE, --cache CACHE
                        use cache from JSON file, default $HOME/.lingcapp.json
  -d {auto,en-ru,ru-en}, --direction {auto,en-ru,ru-en}
                        translation direction
  -k KEY, --key KEY     api key, default environment variable LINGCAPP_API_KEY
```

## Examples

Mini-card translation for english to russian:

```sh
python3 main.py book

book - книга, том, печатное издание
LingvoUniversal (En-Ru)
```

Reverse translation:

```sh
python3 main.py книга

книга - book
LingvoUniversal (Ru-En)
```

Verbose mode shows additional information:

```sh
python3 main.py -v lion panther tiger
2023-05-26 16:35:47,791 DEBUG: read token from file cache

lion - лев
LingvoUniversal (En-Ru) 642.81 ms

panther - леопард; пантера; барс
LingvoUniversal (En-Ru) 641.73 ms

tiger - тигр
LingvoUniversal (En-Ru) 640.30 ms
2023-05-26 16:35:48,441 DEBUG: total duration: 649.94 ms
```

## License

This source code is governed by a MIT license that can be found
in the [LICENSE](https://github.com/z0rr0/lingcapp/blob/main/LICENSE) file.