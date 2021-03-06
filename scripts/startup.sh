#!/usr/bin/env bash
set -euo pipefail

run_props="$1"
service_url=""

if  grep -E "https?://" <<< "$run_props" > /dev/null;then
  service_url="$run_props"
  cat > /tmp/test-run-props.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties version="1.0">
  <comment>Test run arguments</comment>
  <entry key="iut">${run_props}</entry>
</properties>
EOF
    nr_args="$#"
    set -- "/tmp/test-run-props.xml" "${@:2:$nr_args}" # replace first argument with path to test-run-props.xml
fi

EXIT_ON_FAIL=""
if [[ $* == *--exitOnFail* ]];then
  EXIT_ON_FAIL="--exit-on-fail"
fi

PRETTY_PRINT=""
if [[ $* == *--prettyPrint* ]];then
  PRETTY_PRINT="--pretty-print"
fi

if [[ $* == *--verbose* ]];then
  exec 5>&1 # capture output command and write to stdout see https://stackoverflow.com/a/16292136
  output=$(java -jar /opt/ets-ogcapi-features10-aio.jar "$@"|tee /dev/fd/5)
else
  output=$(java -jar /opt/ets-ogcapi-features10-aio.jar "$@")
fi

output_dir=$(grep "Test results" <<< "$output" | cut -d: -f3 | xargs dirname)
python3 /src/parse-results.py "${output_dir}" --service-url "${service_url}" ${EXIT_ON_FAIL} ${PRETTY_PRINT}

