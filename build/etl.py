import argparse
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=argparse.FileType('r'))
    args = parser.parse_args()

    source = json.load(args.source)

    print("Parsing source %s, type %s, from %s" % (args.source.name, source['type'], source['data']))


if __name__ == '__main__':
    main()
