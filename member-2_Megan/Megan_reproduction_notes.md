# CS4297 Lab — Java Buildability Reproduction Notes

**Group:** G35  
**Project:** Java Buildability across JDK Versions

## Method
Tested four frozen Java projects using JDK 11, 17, 21 and 23. The experiment used Maven or Gradle build commands in Docker. Each project/JDK combination was recorded as PASS or FAIL based on the build outcome.

## Results
- Total builds: 16
- Passed: 8
- Failed: 8
- Success rate: 50%
- Results matching the original study: 16/16 (100%)

All 16 project/JDK results matched the original study for the same projects, commits and JDK versions.

### Results by JDK
- JDK 11: 3 projects passed.
- JDK 17: 2 projects passed.
- JDK 21: 2 projects passed.
- JDK 23: 1 project passed.

## Failure investigation
- lorne_core, JDK 21 and 23: unsupported Java 7 source/target options.
- nodejs, JDK 11 and 17: Maven Enforcer requires JDK 21 or newer.
- nodejs, JDK 23: compilation targets Java 21 while enabling preview features, which conflicts with JDK 23 preview-feature rules.
- hopperoptimizations, JDK 17, 21 and 23: Groovy runtime initialisation error involving `org.codehaus.groovy.vmplugin.v7.Java7`.

## Evidence
- Megan_comparision.csv: project-by-project comparison with the original study.
- Project result CSV files.
- Megan_logs/: raw build logs.

## Limitations
Although all 16 results matched the original study, the failure messages identify the immediate build errors rather than proving every underlying cause. The experiment was limited to four selected projects and four JDK versions.
