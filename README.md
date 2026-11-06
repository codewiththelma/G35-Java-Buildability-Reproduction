
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

We reproduced the original study's build outcomes for 20 Java projects across JDK 11, 17, 21 and 23, giving 80 build attempts in total.

### Build Success Rate Comparison

| JDK Version | Original Study (PASS) | G35 (PASS) | G35 Build Success Rate |
|---|---:|---:|---:|
| JDK 11 | 11/20 | 11/20 | 55% |
| JDK 17 | 9/20 | 9/20 | 45% |
| JDK 21 | 9/20 | 9/20 | 45% |
| JDK 23 | 5/20 | 5/20 | 25% |
| **Total** | **34/80** | **34/80** | **42.5%** |

Our results matched the original study for all 80 individual project-JDK build outcomes (80/80 agreement). These rates describe our selected 20-project sample, not the full original dataset.

### Results Evidence

The individual comparison CSV files contain the recorded outcomes:

- [Member 1 – Thelma](member1_thelma/Thelma_comparison.csv)
- [Member 2 – Megan](member-2_Megan/Megan_comparision.csv)
- [Member 3 – Build results](member-3-evidence/results.csv)
- [Member 4 – Denzel](member-4/Denzel_comparison.csv)
- [Member 5 – Omololuwa](member5/Omololuwa_comparison.csv)

For Member 3's raw results CSV, `0` indicates PASS and `1` indicates FAIL.

We also investigated build failures and preserved logs as supporting evidence.

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
