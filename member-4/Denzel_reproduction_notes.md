# CS4928 Lab 4 — Reproduction Notes
Name: Denzel
Group: G35
Project: Java Buildability across JDK Versions

## Method
Reproduced part of the original Java buildability study.
Tested 4 frozen GitHub projects (13-16) using JDK 11, 17, 21 and 23.
Used the researchers' Docker images (sulir/jdk-study) and build script.

## Results
Total builds: 16
Passed: 4
Failed: 12

All 16 results matched the original researchers' dataset.

## Failure Investigation
- Ripme JDK 17, 21, 23: Project targets Java 6; JDK 12+ no longer supports Java 6 ("Source option 6 is no longer supported").
- Jar-analyzer-gui JDK 11, 17, 21, 23: Dependency error; Maven could not resolve the project's local jars (lib:panel, lib:fern). Not JDK related.
- Super-xray JDK 11, 17, 21, 23: Goal 'assembly' removed from maven-assembly-plugin 3.7.1. Not JDK related.
- Jiron-cloud JDK 23: Compilation error, cannot find symbol in jiron-common-translation. Builds on JDK 21, so caused by JDK 23.

## Setup Changes
- None. Used the researchers' pre-built Docker images from Docker Hub without changes.
- Ran the builds with docker run commands instead of a Python script (commands in scripts/).
- Jiron-cloud builds were run a second time because the first run did not record results.

## Evidence
- Denzel_results.csv
- Denzel_comparison.csv
- Denzel_logs/ folder
- Denzel_run-member4.sh (in scripts/)

## Status
My 4-project reproduction matched the original study.
