#!/usr/bin/env bash
# G35 Member 4 (Denzel) - commands used to build projects 13-16 on JDK 11, 17, 21 and 23
# Uses the researchers' Docker images sulir/jdk-study:<JDK> from Docker Hub
# Exit code 0 = PASS, anything else = FAIL

mkdir -p ~/g35-projects/member-4/logs
cd ~/g35-projects/member-4
echo "project,commit,tool,builder,jdk,exit_code,seconds" > member4_results.csv

run_project () {
  cd ~/g35-projects/member-4
  git clone https://github.com/$1.git $2
  cd $2
  git checkout $3
  git rev-parse HEAD
  mkdir -p ../logs/$2
  for v in 11 17 21 23; do
    s=$(date +%s)
    docker run --rm --mount=type=bind,src="$PWD",dst=/mnt/project,readonly sulir/jdk-study:$v mvn > ../logs/$2/java$v.log 2>&1
    c=$?
    echo "$1,$(git rev-parse HEAD),Maven,mvn,$v,$c,$(( $(date +%s)-s ))" | tee -a ../member4_results.csv
  done
}

run_project 4pr0n/ripme            ripme            351b58ce22974c9b7bc290e0afe0d9c3f4133a0c
run_project 4ra1n/jar-analyzer-gui jar-analyzer-gui 96b11d16dd7e098902996051964543e3b73a9426
run_project 4ra1n/super-xray       super-xray       cda5fd16754cc03bcf9b77940cd67506921567f9
run_project 642933588/jiron-cloud  jiron-cloud      ddd6c2e992bacd9931839f2d2f1eb2819160f6a7
