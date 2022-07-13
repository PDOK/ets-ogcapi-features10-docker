#!/usr/bin/env bash
set -u

SCRIPT_DIR=$(dirname "$0")

docker-compose -f $SCRIPT_DIR/docker-compose.yaml up -d
export KUBECONFIG=$SCRIPT_DIR/kubeconfig.yaml

mkdir -p output

sleep 5
docker wait $(docker-compose -f $SCRIPT_DIR/docker-compose.yaml ps | grep kubernetes-agent_ | cut -d " " -f1)
kustomize build $SCRIPT_DIR/kubernetes-config | kubectl apply -f -

docker build . -t pdok/ets-ogcapi-features10-docker:test

kubectl wait pods -l app=ogcapi-features --for=condition=Ready --timeout=180s

docker run -v "$(pwd):/mnt"  pdok/ets-ogcapi-features10-docker:test https://localhost:32788/geonovum/oaf/v1_0/ --generateHtmlReport true --outputDir /mnt/output
