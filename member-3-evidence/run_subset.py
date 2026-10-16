#!/usr/bin/env python3
"""Run the authors' exact build procedure, restricted to JDK 11, 17, 21 and 23.
Usage: ./run_subset.py <projects_dir> <result_dir> <log_dir>
"""
import importlib.util
import sys
from csv import DictWriter
from logging import error, info
from pathlib import Path
from random import seed, shuffle

REPO = Path(__file__).resolve().parent
sys.path.insert(1, str(REPO))
_spec = importlib.util.spec_from_file_location("run_builds", REPO / "execution" / "run-builds.py")
rb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rb)

JDKS = [11, 17, 21, 23]
FIELDS = ["name", "commit", "tool", "wrapper"] + [f"java{v}" for v in JDKS]


def build_project(project_name, project_dir, log_dir):
    info("Analyzing %s", project_name)
    builder, result = rb.analyze_project(project_name, project_dir)
    project_log_dir = rb.prepare_log_dir(project_dir, log_dir)
    versions = JDKS.copy()
    seed(project_name)
    shuffle(versions)
    for v in versions:
        info("Building %s with Java %d", project_name, v)
        result[f"java{v}"] = rb.build_project_with_java(project_dir, v, builder, project_log_dir)
    return result


def main(dataset_dir, result_dir, log_dir):
    rb.initialize()
    results_csv = rb.prepare_results_csv(result_dir, FIELDS)
    log_dir.mkdir(parents=True, exist_ok=True)
    pending = rb.list_pending_projects(dataset_dir, results_csv)
    info("%d projects pending", len(pending))
    with open(results_csv, "a", newline="") as out:
        writer = DictWriter(out, FIELDS)
        for project_dir in pending:
            name = rb.get_project_name(project_dir)
            try:
                row = build_project(name, project_dir, log_dir)
            except FileNotFoundError as e:
                error("%s", e)
                row = {"name": name, "tool": "none"}
            writer.writerow(row)
            out.flush()
            rb.remove_cache_volumes()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
