
# G35-Java-Buildability-Reproduction

**CS4928 Software Design – Group G35**

## About the Project

This project is part of our CS4928 Software Design module. Our aim was to reproduce part of the experiment from the research paper *Local Software Buildability across Java Versions*.

We wanted to see how different Java projects build across different JDK versions and compare our results with the original study.

## What We Did

- Selected 20 Java projects from the original study.
- Tested each project using JDK 11, 17, 21 and 23.
- Used Docker to run the builds in consistent environments.
- Recorded whether each build passed or failed.
- Compared our results with the original study.
- Saved the build logs and documented our findings.

## Our Results

We successfully reproduced the experiment from the original paper.

Our group's results matched the original study, showing how some Java projects could build successfully on one JDK version but fail on another.

We also looked into the build failures, saved the logs and documented our findings as evidence of our reproduction.

## Tools Used

- **Python** – To automate the builds and record results.
- **Docker** – To run builds using different JDK versions.
- **Java (JDK 11, 17, 21 and 23)** – The Java versions we tested.
- **Maven and Gradle** – The build tools used by the projects.
- **Git and GitHub** – To manage the projects and our repository.
- **Ubuntu (WSL)** – Our testing environment.

## Repository Contents

This repository contains:

- Python scripts used to run the builds.
- CSV files containing our test results.
- Build logs showing successful and failed builds.
- Documentation of our reproduction process.

## Reference

**Original paper:** *Local Software Buildability across Java Versions* – Sulír et al. (2026)

**Original GitHub repository:**  
https://github.com/sulir/jdk-study
