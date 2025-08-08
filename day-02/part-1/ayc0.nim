from times import cpuTime
from os import paramStr

import strutils

proc sign(x: int): int =
  (x > 0).int - (x < 0).int

proc run(s: var string): int =
    # Your code here
    let lines = splitLines(s)

    var total = 0

    var lastNb: int
    var lastSign: int
    var currentNb: int
    var currentSign: int
    var okay: bool
    for line in lines:
        lastNb = 0
        okay = true
        lastSign = 0
        if line.len == 0:
            continue
        for currentNbStr in line.split(' '):
            currentNb = parseInt(currentNbStr)
            if lastNb == 0:
                lastNb = currentNb
                continue
            let diff = abs(currentNb - lastNb)
            currentSign = sign(currentNb - lastNb)
            if lastSign == 0:
                lastSign = currentSign
            lastNb = currentNb
            if diff > 3 or diff < 1 or lastSign != currentSign:
                okay = false
                break
        if okay:
            total += 1

    return total


var input: string = paramStr(1)

let t0 = cpuTime()
let output = run(input)

echo "_duration:", (cpuTime() - t0) * 1000
echo output
