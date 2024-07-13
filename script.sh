#!/bin/bash

run_sims() {
    /usr/local/bin/python3 /Users/opias/Desktop/a_sencron_bfs_algorithm/codes/main.py
}


index=1

while [ $index -le 10 ]; do

osascript <<EOF
  tell application "Terminal"
      do script "$(declare -f run_sims); run_sims"
  end tell
EOF

  sleep 1

  index=$(( $index + 1 ))
done
