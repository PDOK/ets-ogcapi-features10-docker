#!/usr/bin/env bash
set -u

SCRIPT_DIR=$(dirname "$0")

docker-compose -f $SCRIPT_DIR/docker-compose.yaml up -d
export KUBECONFIG=$SCRIPT_DIR/kubeconfig.yaml

mkdir -p output

sleep 5
#docker wait $(docker-compose -f $SCRIPT_DIR/docker-compose.yaml ps | grep kubernetes-agent_ | cut -d " " -f1)
kustomize build $SCRIPT_DIR/goaf | kubectl apply -f -

docker build . -t pdok/ets-ogcapi-features10-docker:test

kubectl wait pods -l app=ogcapi-features --for=condition=Ready --timeout=180s

docker run --network=example_ogcapi -v "$(pwd):/mnt"  pdok/ets-ogcapi-features10-docker:test http://kubernetes-server/geonovum/oaf/v1_0/ --generateHtmlReport true --outputDir /mnt/output
