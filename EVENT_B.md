# Event B – Evolution Response

**Group:** G35
**Project:** P34
**Tag:** EVENT_B

## 1. Prediction Before Testing

We predict that the new requirement to build on a newer JDK in a clean CI environment might cause some problems with dependency caching. Some projects might build differently if the dependencies from earlier builds are no longer available. This could mean that keeping the original caching approach may not always give consistent results.

This prediction was recorded before Event B testing.
