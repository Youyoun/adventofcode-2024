import strutils, tables

from times import cpuTime

from os import paramStr

proc run(s: var string): int =
    # Your code here
    let lines = splitLines(s)

    var lefts = newSeq[string](lines.len)
    lefts.setLen(0)

    var rights = initCountTable[string]()

    for line in lines:
        let sepPos = line.find("   ")
        let leftStr = line[0 ..< sepPos]
        let rightStr = line[sepPos + 3 .. ^1]
        lefts.add(leftStr)
        rights.inc(rightStr)

    var total = 0

    for left in lefts:
        total += parseInt(left) * rights.getOrDefault(left)

    return total


var input: string = paramStr(1)

let t0 = cpuTime()
let output = run(input)

echo "_duration:", (cpuTime() - t0) * 1000
echo output
