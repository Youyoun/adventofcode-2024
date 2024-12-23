# Advent of code 2024 solutions <!-- omit in toc -->

⁣    🌟\
    🎄\
   🎄🎄\
  🎄🎄🎄\
 🎄🎄🎄🎄\
🎄🎄🎄🎄🎄\
  🎁🎁🎁

These are proposed solutions for the [Advent of Code 2024](http://adventofcode.com/2024).

The solutions are automatically tested with github-actions.

An automatically updated
[leaderboard](https://cs-advent-of-code-2024.netlify.app/) summarizes the
execution times of each entry submitted for each problem. It takes a few
minutes to update once a new submission is merged.

[![Build Status](https://github.com/th-ch/adventofcode-2024/workflows/CI/badge.svg)](https://github.com/th-ch/adventofcode-2024/actions?query=branch%3Amain)

- [Usage](#usage)
  - [Installation](#installation)
  - [Examples](#examples)
    - [Run last problem](#run-last-problem)
    - [Run specific problems from specific users](#run-specific-problems-from-specific-users)
- [Contribute](#contribute)
  - [New submission with aoc](#new-submission-with-aoc)
  - [New submission without aoc](#new-submission-without-aoc)
- [Installing runners to try out other people code](#installing-runners-to-try-out-other-people-code)
  - [Go](#go)
  - [Rust](#rust)
  - [Deno](#deno)
  - [Nim](#nim)
  - [PHP](#php)
  - [C #](#c-)
  - [Zig](#zig)
- [History](#history)

## Usage

use `./aoc` script

```text
usage: aoc <command> [<args>]

aoc commands are:
   run      Runs submissions
   create   Creates a new submission
   config   Configures user's parameters
```

### Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# And now aoc can work
./aoc run
```

### Examples

#### Run last problem

```bash
./aoc run
```

```text
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Running submissions for day 04:

* part 2:
---------------------------------------------------
Avg over all inputs
---------------------------------------------------
----------  ----------  -----------  ---
silvestre      78452        1.99 ms  py
degemer        43695        2.39 ms  py
jules          23037        2.49 ms  py
david          36371        2.94 ms  py
thomas          9763        2.97 ms  py
ayoub         136461        5.85 ms  cpp
evqna          49137        6.65 ms  cpp
badouralix     51232        7.26 ms  go
tpxp           41668      133.63 ms  rb
----------  ----------  -----------  ---
```

#### Run specific problems from specific users

```bash
./aoc run -d 1 -d 2 -p 1 -a ayoub -a david
```

```text
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Running submissions for day 01:

* part 1:
---------------------------------------------------
Avg over all inputs
---------------------------------------------------
-----  -------  -----------  ---
david    543        0.46 ms  py
ayoub    445        4.94 ms  cpp
-----  -------  -----------  ---
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Running submissions for day 02:

* part 1:
---------------------------------------------------
Avg over all inputs
---------------------------------------------------
-----  --------  -----------  ---
david    5658        1.22 ms  py
ayoub    6448        4.84 ms  cpp
-----  --------  -----------  ---
```

You can use `-r` to run each submission on it's own input, or `-e` to print non-aggregated results.\
see `./aoc run -h` for full arguments description.

## Contribute

To participate, you'll have to create your own files containing your solutions (see next sections for details on how to
create them).

You can add other functions & modules if you need to. Any external dependency should be added to the appropriate files
(`requirements.txt`, `package.json`, and so on).

Once you tested your solution you can submit it by making a PR and a GitHub action will check that your code generates
the same outputs as others' code.

For now we support `c`, `c++`, `java`, `javascript` & `typescript` (with deno), `go`, `python 3` (+
`cython`), `ruby`, `rust (stable)`, `julia`, `bash`, `nim`, `v`,`zig`, scripts and `php`.

### New submission with aoc

You can use `./aoc create` tool to create a new empty submission:

```text
usage: aoc create [-h] [-a AUTHOR] [-d DAY] [-p PART]
                  [-l {c,cpp,go,intcode,java,js,ts,ml,nim,php,py,pyx,rb,rs,sh,v,zig}]

Create a new submission

optional arguments:
  -a AUTHOR, --author AUTHOR
                        submission author
  -d DAY, --day DAY     problem day
  -p PART, --part PART  problem part
  -l {c,cpp,go,intcode,java,js,ts,ml,nim,php,py,pyx,rb,rs,sh,v,zig}, --language {c,cpp,go,intcode,java,js,ts,ml,nim,php,py,pyx,rb,rs,sh,v,zig}
                        submission language
```

you can also use `./aoc config` to setup your local profile

```text
usage: aoc config [-h] username {c,cpp,go,intcode,java,js,ts,ml,nim,php,py,pyx,rb,rs,sh,v,zig}

Configures user parameters

positional arguments:
  username              prefered username
  {c,cpp,go,intcode,java,js,ts,ml,nim,php,py,pyx,rb,rs,sh,v,zig}
                        prefered programming language
```

### New submission without aoc

If you don't use `./aoc create` tool you should follow this convention:

```text
day-[number]/part-[number]/[username].py    # your submission code
day-[number]/input/[username].txt           # your input file
```

Your submission code should follow templates written in the `tool/templates/` folder (there is one for each language).

## Installing runners to try out other people code

### Go

```bash
brew install go
```

### Rust

Follow: <https://www.rust-lang.org/tools/install>

### Deno

```bash
brew install deno
```

or

```bash
curl -fsSL https://deno.land/x/install/install.sh | sh
```

### Nim

```bash
brew install nim
```

### PHP

To have the same version as the one installed in the runner, not mandatory.

```bash
brew install php@7.4
```

### C \#

```bash
brew install dotnet-sdk
```

The official documentation is also available [here](https://docs.microsoft.com/en-us/dotnet/core/install/macos).

### Zig

```bash
brew install zig
```

## History

- [Advent of Code 2023](https://github.com/th-ch/adventofcode-2023)
- [Advent of Code 2022](https://github.com/badouralix/adventofcode-2022)
- [Advent of Code 2021](https://github.com/lypnol/adventofcode-2021)
- [Advent of Code 2020](https://github.com/david-ds/adventofcode-2020)
- [Advent of Code 2019](https://github.com/lypnol/adventofcode-2019)
- [Advent of Code 2018](https://github.com/badouralix/adventofcode-2018)
- [Advent of Code 2017](https://github.com/lypnol/adventofcode-2017)
- [Advent of Code 2016](https://github.com/lypnol/adventofcode-2016)
