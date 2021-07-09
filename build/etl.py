import argparse
import json
import logging
import shutil
import sys
import tempfile


logger = logging.getLogger('etl')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=argparse.FileType('r'))
    args = parser.parse_args()

    setup_logging()

    source = json.load(args.source)

    logger.info("Parsing source %s, type %s, from %s", args.source.name, source['type'], source['data'])

    with tempfile.NamedTemporaryFile('w+b') as fp:
        extract(source, fp)
        logger.info("Downloaded %d bytes to %s", fp.tell(), fp.name)

        fp.seek(0)
        transform(source, fp)


def setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.INFO)

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
        import codecs

        dumper = EsriDumper(source_url, logger)

        features = list(dumper)
        feature_collection = {
            'type': "FeatureCollection",
            'features': features,
        }

        json.dump(features, codecs.getwriter('utf-8')(output), separators=(',', ':'))

    elif source_type == 'http':
        import requests

        r = requests.get(source_url, stream=True)
        r.raise_for_status()
        shutil.copyfileobj(r.raw, output)

    elif source_type == 'ftp':
        import requests
        import requests_ftp
        requests_ftp.monkeypatch_session()

        s = requests.Session()
        r = s.get(source_url)
        r.raw.seek(0)
        shutil.copyfileobj(r.raw, output)

    else:
        logger.error("Unknown source type %s", source_type)


def transform(source, output):
    pass


if __name__ == '__main__':
    main()
