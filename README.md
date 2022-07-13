# README

```bash
mkdir -p output
docker run -v "$(pwd):/mnt"  pdok/ets-ogcapi-features10-docker:1.4 https://api.pdok.nl/geonovum/oaf/v1_0/ --generateHtmlReport true --outputDir /mnt/output
```
