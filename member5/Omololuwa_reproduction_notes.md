# CS4928 Lab 4 — Reproduction Notes

**Name:** Omololuwa Adejinmi  **Group:** G35  **Project:** Java Buildability across JDK Versions

## Method

Reproduced part of the original Java buildability study. Tested 4 frozen GitHub projects (18-21) using JDK 11, 17, 21 and 23. Used the researchers' Docker image setup (`sulir/jdk-study`) and their build functions, called through a runner script (`run-member.py`) that builds each project on each JDK and records the exit codes.

## Results

Total builds: 16  Passed: 3  Failed: 13

| Project | JDK 11 | JDK 17 | JDK 21 | JDK 23 |
|---|---|---|---|---|
| spring-boot-seed | PASS | PASS | PASS | FAIL |
| xjavafxtool-spring | FAIL | FAIL | FAIL | FAIL |
| ssgwt-lib | FAIL | FAIL | FAIL | FAIL |
| tyme4j | FAIL | FAIL | FAIL | FAIL |

All 16 results matched the original researchers' dataset.

## Failure Investigation

* **spring-boot-seed JDK 23:** Compilation error. JDK 23 cannot read `aspectjweaver-1.8.13.jar` ("Invalid CEN header (invalid zip64 extra data field size)"), which then causes many "cannot access" and "cannot find symbol" errors in `mc-core`. Builds on JDK 11, 17 and 21, so this is caused by JDK 23.
* **xjavafxtool-spring JDK 11, 17, 21, 23:** Maven rejects the project's `pom.xml` because the repository id `xwintop-maven` is declared twice (line 36). Fails before compiling. Not JDK related.
* **ssgwt-lib JDK 11, 17, 21, 23:** Ant reports that the targets `jar`, `war` and `dist` do not exist in `build.xml`, so nothing is built. Not JDK related.
* **tyme4j JDK 11, 17, 21, 23:** Compilation succeeds and all 395 tests pass, but the build fails in `maven-javadoc-plugin:2.9` ("Unable to find javadoc command" at `/opt/java/../bin/javadoc`). The old plugin assumes the JDK 8 layout, which differs on JDK 9+. JDK related.

## Setup Changes

* Applied two fixes to `environment/Dockerfile`: the Apache Ant download URL now points to `archive.apache.org`, and the Zulu JDK extraction uses `mkdir -p $JAVA_HOME` with `tar -xz -C` instead of `--one-top-level`.
* Converted `environment/run-build.sh` from Windows (CRLF) to Linux (LF) line endings.
* Built the four Docker images locally (JDK 11, 17, 21, 23) instead of pulling them. [CHANGE THIS IF YOU PULLED THE IMAGES.]
* Ran the builds with `run-member.py`, which calls the authors' `build_project_with_java` function. The authors' Python scripts were not edited.
* The first attempt (`member-5`) failed all 16 builds with exit code 1 because Docker Desktop's WSL integration was not enabled ("docker could not be found in this WSL 2 distro"). No builds ran, so it is not a valid result. The builds were rerun after enabling Docker integration (`member-5-rerun`). The results in this report are from the rerun.

## Evidence

* `Omololuwa_results.csv` (valid results, from `member-5-rerun`)
* `Omololuwa_comparison.csv` (my results compared with the authors' published `results.csv`, 16 of 16 matched)
* `Omololuwa_logs/` folder (from `member-5-rerun`)
* `Omololuwa_first-attempt-INVALID_results.csv` (the invalid first attempt from `member-5`, kept as a record; contains no real build results)
* `run-member.py` (runner script)

## Status

My 4-project reproduction matched the original study.
