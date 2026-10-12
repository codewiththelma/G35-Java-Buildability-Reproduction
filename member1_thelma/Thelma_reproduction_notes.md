# CS4928 Lab 4 — Reproduction Notes
Name: Thelma
Group: G35
Project: Java Buildability across JDK Versions

## Method
Reproduced part of the original Java buildability study.
Tested 4 frozen GitHub projects using JDK 11, 17, 21 and 23.
Used the researchers' build scripts with Docker.

## Results
Total builds: 16
Passed: 11
Failed: 5

All 16 results matched the original researchers' dataset.

## Failure Investigation
- Nextron JDK 11: Java 17 target not supported by JDK 11.
- Nextron JDK 23: Missing Java methods; possible annotation processing issue.
- Xiaofanshu JDK 21: Java compiler incompatibility (NoSuchFieldError).
- Xiaofanshu JDK 23: Cannot infer type arguments for Result.
- Cmake4eclipse JDK 11: Eclipse Tycho component requires Java 17.

## Setup Changes
- Updated the Apache Ant download URL in the Dockerfile.
- Fixed JDK extraction in the Dockerfile.
- Converted the build script to Linux line endings.
- Created a Python script to run the selected JDK versions.

## Evidence
- Thelma_results.csv
- Thelma_comparison.csv
- logs/ folder
- Thelma_run-member1.py (in scripts/)

## Status
My 4-project reproduction matched the original study.
