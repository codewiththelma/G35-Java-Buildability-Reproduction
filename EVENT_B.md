# Event B – Evolution Response

**Group:** G35
**Project:** P34
**Tag:** EVENT_B

## 1. Prediction Before Testing

We predict that the new requirement to build on a newer JDK in a clean CI environment might cause some problems with dependency caching. Some projects might build differently if the dependencies from earlier builds are no longer available. This could mean that keeping the original caching approach may not always give consistent results.

This prediction was recorded before Event B testing.

## 2. Our Response to Event B

Event B required us to test a newer JDK in a clean CI environment without depending on a developer's computer. We also needed to compare our frozen pre-M4 and M4 versions, consider the repair effort, and decide whether our M4 decision was still reasonable.

Our prediction focused on dependency caching because this was the design decision we had considered during M4. Once we started Event B, we found that the JDK 25 failures were not necessarily caused by caching. We also identified limitations in our original testing setup that made it difficult to use for the new requirement.

We considered two options:

**Option 1 – Modify the original runner.** We could update the Python runner and the authors' build setup to support JDK 25, remove local path dependencies and reconsider caching. This would keep everything in one testing process, but it would also change the setup used for our earlier reproduction.

**Option 2 – Keep the original runner and add separate JDK 25 testing.** This would preserve our earlier method while allowing us to test the newer JDK independently. The disadvantage is that we would have two testing approaches to maintain.

We chose Option 2 because it was the smaller change and allowed us to investigate JDK 25 without affecting our earlier reproduction results.

## 3. What We Implemented and Tested

We created `event-b/Dockerfile` using Eclipse Temurin JDK 25 and Maven 3.9.9. We tested the same four Java projects at the commits used in our original reproduction.

Our initial tests showed that only `equationexploit` passed. After investigating the failures and applying the successful workaround, our final results were:

| Project | JDK 25 result | Notes |
| --- | --- | --- |
| equationexploit | PASS | No workaround needed |
| nextron | FAIL | Compilation errors |
| xiaofanshu | FAIL | Compilation errors |
| cmake4eclipse | PASS | XML parser workaround required |

### equationexploit

This project built successfully on JDK 25 without any changes.

**Evidence:** `event-b/equationexploit-jdk25.log`

### nextron

The build failed with compilation errors, including missing getter methods. We suspected an issue with Lombok annotation processing, but could not confirm the exact cause.

We tested it on JDK 21 for comparison, and it passed. However, the JDK 25 failure remained unresolved.

**Evidence:**
- `event-b/nextron-jdk25.log` — JDK 25 failure
- `event-b/nextron-jdk21-repair.log` — successful JDK 21 build

### xiaofanshu

This project failed during compilation with errors involving its `Result` constructors. We suspected Lombok annotation processing might be involved because the project uses Lombok annotations.

We retried the JDK 25 build, but it failed again. We could not confirm the exact cause or find a successful fix.

**Evidence:**
- `event-b/xiaofanshu-jdk25.log` — initial attempt
- `event-b/xiaofanshu-jdk25-retry.log` — failed retry

### cmake4eclipse

The first build failed because the XML parser reached its general entity size limit (`JAXP00010003`).

We increased `jdk.xml.maxGeneralEntitySizeLimit` to `1000000`, but the next build failed because of the total entity size limit (`JAXP00010004`).

We then increased both `jdk.xml.maxGeneralEntitySizeLimit` and `jdk.xml.totalEntitySizeLimit` to `1000000`, and the build passed. We applied the workaround through Java environment settings without modifying the project's source code.

**Evidence:**
- `event-b/cmake4eclipse-jdk25.log` — original failure
- `event-b/cmake4eclipse-jdk25-xml-fix.log` — first workaround, still failed
- `event-b/cmake4eclipse-jdk25-xml-fix2.log` — second workaround, successful build

### Final Testing Script and CI Attempt

After investigating the builds, we created `event-b/scripts/run-jdk25.sh` to make the testing easier to repeat. It downloads the four projects at their recorded commits, runs their builds in Docker and saves the results. The XML workaround is applied only to `cmake4eclipse`.

We ran the script locally and reproduced the final results shown above.

**Evidence:**
- `event-b/scripts/run-jdk25.sh`
- `event-b/portable-results/equationexploit-jdk25.log`
- `event-b/portable-results/nextron-jdk25.log`
- `event-b/portable-results/xiaofanshu-jdk25.log`
- `event-b/portable-results/cmake4eclipse-jdk25.log`

We also prepared a GitHub Actions workflow for a JDK 25 build. However, GitHub blocked the job from starting because of an account billing restriction. The workflow covered only `equationexploit`, so hosted CI verification remains incomplete.

**Evidence:** `.github/workflows/event-b-jdk25.yml`

## 4. Before and After Comparison

We compared the frozen pre-M4 (`b7716ea`) and M4 (`3988943`) versions using Git. The only difference was the addition of `M4 Pre-Event B decision.pdf`, meaning the original Python runner was unchanged.

The frozen setup was configured for JDK 11, 17, 21 and 23, not JDK 25. Both versions therefore had the same limitation under the new requirement. We checked their code and configuration rather than separately executing the frozen versions on JDK 25.

| Area | Pre-M4 | M4 | Event B |
| --- | --- | --- | --- |
| Build runner | Original Python runner | Unchanged | Separate JDK 25 script added |
| Dependency caching | Shared cache volumes | Shared caching retained | Fresh Maven cache per container |
| JDK support | 11, 17, 21, 23 | No change | JDK 25 tested separately |
| Local folder paths | Required | Still required | New script avoids these paths |
| Build results | Original reproduction results | Same executable setup | Two passes and two failures on JDK 25 |

Our earlier JDK 23 results also had two passes and two failures. However, `cmake4eclipse` needed an additional XML workaround on JDK 25.

The repair effort involved setting up the new Docker environment, investigating the build failures and creating the separate testing script. We resolved the XML-related failure, while the two compilation failures remained unresolved.

**Evidence:**
- Commits `b7716ea` and `3988943` — frozen versions
- `M4 Pre-Event B decision.pdf` — M4 decision
- `scripts/Thelma_run-member1.py` — original runner
- `~/g35-projects/results/member1/Thelma_results.csv` — original results stored locally

## 5. Design Impact and Final Evaluation

The main additions were `event-b/Dockerfile`, `event-b/scripts/run-jdk25.sh` and `.github/workflows/event-b-jdk25.yml`, together with the build logs. We did not modify the original runner, the authors' scripts, the Java project source code or our earlier results.

This kept the changes mainly within the Event B files. The new script no longer relies on our personal project folder paths, although it still needs Docker, Git, Bash, internet access and Maven dependencies.

Our original prediction about caching was not confirmed. The two compilation failures occurred with fresh Maven caches, and the `cmake4eclipse` failure was related to XML parser limits. Since we did not compare shared and fresh caches under identical conditions, we cannot completely rule out caching effects.

We consider our M4 decision **supported for the original reproduction, but only partly supported under the new Event B requirements**. Keeping the original caching method preserved our earlier approach, while the separate script addressed the need for newer-JDK testing without changing it.

The main trade-off is maintaining two testing approaches. The XML workaround also introduces a security consideration because increasing parser limits can reduce protection against untrusted XML. We limited the workaround to the affected project.

Overall, Event B showed that we could respond to the new requirement with a small addition rather than redesigning our original runner. We recorded both successful and unsuccessful attempts, kept our earlier results unchanged and made the JDK 25 testing easier to repeat locally.

**Supporting commits:**
- `44f5141` — original Event B prediction
- `218f985` — Dockerfile and GitHub Actions workflow
- `5888ce0` — testing script and build logs
