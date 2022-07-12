# README

```bash
mkdir -p output
docker run -v "$(pwd):/mnt"  ogc-api-te https://api.pdok.nl/geonovum/oaf/v1_0/ --generateHtmlReport true --outputDir /mnt/output
```
