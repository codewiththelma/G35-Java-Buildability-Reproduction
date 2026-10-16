
# CS4297 Lab — Java Buildability Reproduction Notes

**Group:** G35  
**Project:** Java Buildability across JDK Versions

## Method
Tested four frozen Java projects using JDK 11, 17, 21 and 23. The experiment used Maven or Gradle build commands in Docker. Each project/JDK combination was recorded as PASS or FAIL.

## Results
- Total builds: 16
- Passed: 8
- Failed: 8
- Success rate: 50%
- Results matching the original study: 2/16

## Failure investigation
- lorne_core, JDK 21 and 23: unsupported Java 7 source/target options.
- nodejs, JDK 11 and 17: Maven Enforcer requires JDK 21 or newer.
- nodejs, JDK 23: compilation uses Java 21 with preview features, which conflicts with JDK 23's preview-feature rules.
- hopperoptimizations, JDK 17, 21 and 23: Groovy runtime initialisation error.

## Evidence
- Megan_comparison.csv
- Project result CSV files
- Megan_logs/ containing raw build logs

## Limitations
The results differed from the original study in 14 of 16 cases. The reasons for every difference have not yet been fully established.
