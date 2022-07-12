ARG REGISTRY="docker.io"
FROM ${REGISTRY}/maven:3.6.3-openjdk-8

ARG MAVEN_OPTS
ARG REPO=https://github.com/opengeospatial/ets-ogcapi-features10.git


WORKDIR /src
RUN git clone ${REPO} . && git checkout tags/1.4

RUN mvn clean install
RUN mv /src/target/ets-ogcapi-features10-*-aio.jar /src/target/ets-ogcapi-features10-aio.jar

# Run CI profile: unittests, but skip integrationtests, unfortunately they fail on the CI server, because testcontainers fail
# RUN mvn clean install -P ci -e

FROM ${REGISTRY}/azul/zulu-openjdk:8u265-8.48.0.53
RUN apt update && apt install -y python3 \
    python3-pip

WORKDIR /src
COPY scripts /src

RUN python3 -m pip install -r requirements.txt
LABEL AUTHOR="pdok@kadaster.nl"
# set correct timezone
ENV TZ Europe/Amsterdam

COPY --from=0 /src/target/ets-ogcapi-features10-aio.jar /opt/ets-ogcapi-features10-aio.jar
ENTRYPOINT ["bash", "/src/startup.sh"]
