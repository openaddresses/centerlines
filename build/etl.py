import argparse
import json
import logging
import sys


logger = logging.getLogger('etl')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=argparse.FileType('r'))
    args = parser.parse_args()

    setup_logging()

    source = json.load(args.source)

    logger.info("Parsing source %s, type %s, from %s", args.source.name, source['type'], source['data'])

    with tempfile.TemporaryFile() as fp:
        extract(source, fp)
        logger.info("Downloaded %d bytes", fp.tell())

        fp.seek(0)
        transform(source, fp)


def setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)


def extract(source, output):
    source_type = source.get('type')
    source_url = source.get('data')

    if source_type == 'esri':
        from esridump.dumper import EsriDumper

        dumper = EsriDumper(source_url)

        features = list(dumper)
        feature_collection = {
            'type': "FeatureCollection",
            'features': features,
        }

        json.dump(features, delimiters=(':',','))

    elif source_type == 'http':
        import requests

        r = requests.get(source_url, stream=True)
        shutil.copyfileobj(r.raw, output)

    elif source_type == 'ftp':
        import requests_ftp
        s = requests_ftp.FTPSession()
        r = s.retr(source_url)
        shutil.copyfileobj(r, output)

    else:
        logger.error("Unknown source type %s", source_type)


def transform():
    pass


if __name__ == '__main__':
    main()
