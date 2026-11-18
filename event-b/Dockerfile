FROM eclipse-temurin:25-jdk

ARG MAVEN_VERSION=3.9.9

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates git && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL \
    "https://archive.apache.org/dist/maven/maven-3/${MAVEN_VERSION}/binaries/apache-maven-${MAVEN_VERSION}-bin.tar.gz" \
    | tar -xz -C /opt

ENV PATH="/opt/apache-maven-3.9.9/bin:${PATH}"

WORKDIR /workspace
