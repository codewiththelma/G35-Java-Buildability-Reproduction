#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
WORK="$(mktemp -d)"
RESULTS="$ROOT/event-b/portable-results"

mkdir -p "$RESULTS"

echo "Building JDK 25 Docker image..."
docker build -t g35-event-b:jdk25 -f "$ROOT/event-b/Dockerfile" "$ROOT"

run_project() {
    local name="$1"
    local url="$2"
    local commit="$3"
    local xml_fix="$4"
    local project="$WORK/$name"
    local log="$RESULTS/$name-jdk25.log"
    local code=0

    echo ""
    echo "Testing $name at commit $commit"

    git clone "$url" "$project"
    git -C "$project" checkout --detach "$commit"

    local env_args=()
    if [[ "$xml_fix" == "yes" ]]; then
        env_args=(-e "JAVA_TOOL_OPTIONS=-Djdk.xml.maxGeneralEntitySizeLimit=1000000 -Djdk.xml.totalEntitySizeLimit=1000000")
    fi

    docker run --rm \
        --mount "type=bind,src=$project,dst=/project,readonly" \
        --entrypoint bash \
        "${env_args[@]}" \
        g35-event-b:jdk25 \
        -c 'cp -a /project/. /workspace/ && timeout -k 1m 1h mvn clean package -DskipTests --errors --batch-mode' \
        > "$log" 2>&1 || code=$?

    echo "$name: $([[ "$code" -eq 0 ]] && echo PASS || echo FAIL) (exit $code)"
    echo "Log: $log"
}

run_project "equationexploit" \
    "https://github.com/1135/equationexploit.git" \
    "f5d6bbd1742d335cd94ad037b49765e0b820fcd3" "no"

run_project "nextron" \
    "https://github.com/0pandadev/nextron.git" \
    "c9551c25fc33f8e9884bc585d48aabebc0705bc0" "no"

run_project "xiaofanshu" \
    "https://github.com/123yyh123/xiaofanshu.git" \
    "3c9218e5fb07638abfc9d528a28f273576883fb4" "no"

run_project "cmake4eclipse" \
    "https://github.com/15knots/cmake4eclipse.git" \
    "68bac71ed08cd7e8847362e185e5c6c82bcec33a" "yes"

echo ""
echo "All four builds attempted. Logs saved in $RESULTS"
