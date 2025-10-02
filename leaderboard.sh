#!/bin/bash

set -ev

# source $HOME/.cargo/env
export PATH=$PATH:~/.cargo/bin:$GOROOT/bin

./aoc run --all --timeout 1

# Upload the content of leaderboard to the web.
netlify deploy --prod --site cs-advent-of-code-2024 -d leaderboard --auth $NETLIFY_AUTH

