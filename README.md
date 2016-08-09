# centerlines
A repository of street centerline datasets to aid in improving OpenStreetMap.

This repository is intended to maintain two things: a collection of data sources for street centerlines and information describing how to convert those centerlines into a visible tileset for use as an overlay while editing OpenStreetMap data. This is roughly modeled after the [OpenAddresses.io](https://github.com/openaddresses/openaddresses) project, which does a similar thing for address point data.

## Centerline Data Sources
The `sources/` directory includes small JSON files that describe where to get centerline data, what method should be used to get that data (e.g. downloading a file over HTTP, scraping an ESRI layer endpoint, etc), and what the useful data fields are in that source.

## Attribute Information
Once the raw source data is downloaded, it needs to be rendered somehow. The JSON files in `source/` will include information about which source data columns contain the important information. The process will copy those fields over to consistently-named columns so that centerline attributes can be rendered world-wide.

Once the source data is converted into a consistent format, the plan is to use [tippecanoe](https://github.com/mapbox/tippecanoe) and Mapbox to render image tiles that can be used in JOSM or iD.
