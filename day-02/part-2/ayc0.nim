from times import cpuTime
from os import paramStr

import strutils, sequtils

proc sign(x: int): int =
  (x > 0).int - (x < 0).int

proc verifyLine(numbers: var seq[int], indexToSkip: int): bool =
    var lastNb = 0
    var lastSign = 0
    var currentSign = 0

    for i, currentNb in pairs(numbers):
        if i == indexToSkip:
            continue
        if lastNb == 0:
            lastNb = currentNb
            continue
        let diff = abs(currentNb - lastNb)
        currentSign = sign(currentNb - lastNb)
        if lastSign == 0:
            lastSign = currentSign
        lastNb = currentNb
        if diff > 3 or diff < 1 or lastSign != currentSign:
            return false

    return true

proc run(s: var string): int =
    let lines = splitLines(s)

    var total = 0
    var numbers: seq[int]

    for line in lines:
        if line.len == 0:
            continue
        numbers = line.split(' ').map(parseInt)

        for i in -1 ..< numbers.len:
            if verifyLine(numbers, i):
                total += 1
                break

    return total


var input: string = paramStr(1)

let t0 = cpuTime()
let output = run(input)

echo "_duration:", (cpuTime() - t0) * 1000
echo output
