import csv
import importlib.util
import os
from pathlib import Path
import random
import sys

if len(sys.argv) != 2 or sys.argv[1] not in ('1', '2', '3', '4', '5'):
    raise SystemExit('Usage: python run-member.py MEMBER_NUMBER')

member = 'member-' + sys.argv[1]
repo = Path(os.environ['JDK_STUDY_REPO']).resolve()
projects = Path.home() / 'g35-projects' / member
output = Path.home() / 'g35-projects' / 'results' / member
logs = output / 'logs'
versions = [11, 17, 21, 23]

if not projects.is_dir():
    raise SystemExit(f'Missing projects folder: {projects}')

project_dirs = sorted(p for p in projects.iterdir() if p.is_dir())

if len(project_dirs) != 4:
    raise SystemExit(f'Expected 4 projects, found {len(project_dirs)}')

results = output / 'results.csv'

if results.exists():
    raise SystemExit(f'Results already exist; not overwriting: {results}')

sys.path.insert(0, str(repo))
spec = importlib.util.spec_from_file_location(
    'original_builds', repo / 'execution/run-builds.py'
)
original = importlib.util.module_from_spec(spec)
spec.loader.exec_module(original)

logs.mkdir(parents=True, exist_ok=True)
fields = ['name', 'commit', 'tool', 'wrapper'] + [
    f'java{v}' for v in versions
]

with results.open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    for project in project_dirs:
        name = original.get_project_name(project)
        builder, row = original.analyze_project(name, project)
        log_dir = original.prepare_log_dir(project, logs)
        order = versions.copy()
        random.Random(name).shuffle(order)

        print(f'\nBuilding {name}', flush=True)

        for version in order:
            print(f' JDK {version}...', flush=True)

            code = original.build_project_with_java(
                project, version, builder, log_dir
            )
            row[f'java{version}'] = code

            print(
                f' JDK {version}: '
                f'{"PASS" if code == 0 else "FAIL"}',
                flush=True
            )

        writer.writerow(row)
        f.flush()

    original.remove_cache_volumes()

print(f'\nFinished! Results: {results}')
