from times import cpuTime
from os import paramStr

proc run(s: var string): string =
    # Your code here
    return ""


var input: string = paramStr(1)

let t0 = cpuTime()
let output = run(input)

echo "_duration:", (cpuTime() - t0) * 1000
echo output
