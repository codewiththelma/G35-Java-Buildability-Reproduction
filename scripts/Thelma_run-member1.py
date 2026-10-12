import csv
import importlib.util
from pathlib import Path
import random
import sys

REPO = Path("/mnt/c/Users/user/OneDrive - University of Limerick/SEM7/CS4928_Project/jdk-study")
DATASET = Path.home() / "g35-projects/member1"
OUTPUT = Path.home() / "g35-projects/results/member1"
LOGS = OUTPUT / "Thelma_logs"
VERSIONS = [11, 17, 21, 23]

sys.path.insert(0, str(REPO))
spec = importlib.util.spec_from_file_location(
    "original_builds", REPO / "execution/run-builds.py"
)
original = importlib.util.module_from_spec(spec)
spec.loader.exec_module(original)

LOGS.mkdir(parents=True, exist_ok=True)
OUTPUT.mkdir(parents=True, exist_ok=True)

results_path = OUTPUT / "Thelma_results.csv"
fields = ["name", "commit", "tool", "wrapper"] + [
    f"java{v}" for v in VERSIONS
]

if results_path.exists():
    raise SystemExit(
        f"Results already exist: {results_path}. "
        "Refusing to overwrite them."
    )

with results_path.open("w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()

    for project in sorted(DATASET.iterdir()):
        if not project.is_dir():
            continue

        name = original.get_project_name(project)
        builder, result = original.analyze_project(name, project)
        log_dir = original.prepare_log_dir(project, LOGS)

        versions = VERSIONS.copy()
        random.Random(name).shuffle(versions)

        print(f"\nBuilding {name}", flush=True)

        for version in versions:
            print(f"  JDK {version}...", flush=True)
            code = original.build_project_with_java(
                project, version, builder, log_dir
            )
            result[f"java{version}"] = code
            print(f"  JDK {version}: {'PASS' if code == 0 else 'FAIL'}", flush=True)

        writer.writerow(result)
        file.flush()
        original.remove_cache_volumes()

print(f"\nFinished! Results saved to {results_path}")
