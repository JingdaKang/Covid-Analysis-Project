# COVID-19 and Twitter Analysis

A University of Melbourne cloud project combining Twitter data, AURIN datasets, sentiment/geospatial processing, CouchDB, a web presentation, and Ansible deployment to the Melbourne Research Cloud.

## Requirements

Python dependencies vary by component; imports include Tweepy, CouchDB, TextBlob, pandas, emoji, Shapely, and GeoJSON. Deployment needs Ansible, OpenStack access, Docker, and authorized data/API access.

## Getting started

Start with one component and its input data. Review the source scripts and Ansible roles before installing or deploying; the repository has no unified dependency manifest or one-command local setup.

## Project structure

| Path | Purpose |
| --- | --- |
| `Twitter_API` | Recent-search and streaming collectors |
| `Historic Twitter` | Historical data processing |
| `Aurin_data` | Socioeconomic/geospatial data and preprocessing |
| `Couchdb` | Database-related project material |
| `Web_server` | Web presentation |
| `Ansible/mrc` | OpenStack and deployment roles |

## Configuration and limitations

The IP address in the original README was a historical private deployment and is not a current public demo. Configure your own Twitter/CouchDB/OpenStack access; do not reuse committed historical credentials or deploy to the original infrastructure.

## Development and validation

Validate a small, permitted dataset locally before deploying. Cloud playbooks change external infrastructure; review inventory, target project, and required variables first. No unified automated test suite is supplied.

## License

No root-level license file is included. Check source-specific notices and obtain permission before redistribution or reuse.
