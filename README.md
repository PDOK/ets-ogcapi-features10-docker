# README

PDOK Docker image for [OGC API - Features Compliance Test Suite](https://github.com/opengeospatial/ets-ogcapi-features10) for command-line use, with additional features:

- pass service url as command-line argument
- when passing `-exitOnFail` flag, return code `0` if test suite passes all tests, otherwise `1` (instead of always returning `0`)

## Usage examples

```bash
docker run -t -v "$(pwd):/mnt" pdok/ets-ogcapi-features10-docker https://api.pdok.nl/geonovum/oaf/v1_0/ --generateHtmlReport true --outputDir /mnt/output --exitOnFail --prettyPrint
```

```bash
URL=https://api.pdok.nl/geonovum/oaf/v1_0/
cat > ./test-run-props.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties version="1.0">
  <comment>Test run arguments</comment>
  <entry key="iut">${URL}</entry>
</properties>
EOF
docker run -v "$(pwd):/mnt" pdok/ets-ogcapi-features10-docker /mnt/test-run-props.xml --generateHtmlReport true --outputDir /mnt/output
```
