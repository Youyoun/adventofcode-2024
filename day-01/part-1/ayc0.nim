import algorithm, strutils

from times import cpuTime

from os import paramStr

proc run(s: var string): int =
    # Your code here
    let lines = splitLines(s)

    var lefts = newSeq[int](lines.len)
    var rights = newSeq[int](lines.len)
    lefts.setLen(0)
    rights.setLen(0)

    for line in lines:
        let sepPos = line.find("   ")
        let leftStr = line[0 ..< sepPos]
        let rightStr = line[sepPos + 3 .. ^1]
        lefts.add(parseInt(leftStr))
        rights.add(parseInt(rightStr))

    lefts.sort()
    rights.sort()

    var total = 0

    for i in 0..<lefts.len:
        total += abs(lefts[i] - rights[i])

    return total


var input: string = paramStr(1)

let t0 = cpuTime()
let output = run(input)

echo "_duration:", (cpuTime() - t0) * 1000
echo output
