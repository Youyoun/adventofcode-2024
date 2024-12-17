package main

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
	"time"
)

func run(s string) interface{} {
	// Your code goes here
	total := 0
	s = strings.ReplaceAll(s, "\n", "")
	for _, line := range strings.Split(s, "\n") {

		//fmt.Printf("Line: %s\n\n", line)
		remainingMemory := line
		for {
			nextDont := strings.Index(remainingMemory, "don't()")
			if nextDont == -1 {
				// no more don't
				break
			}
			nextDo := strings.Index(remainingMemory[nextDont+7:], "do()")
			if nextDo == -1 {
				// no more mul to add
				remainingMemory = remainingMemory[:nextDont]
				break
			}
			remainingMemory = remainingMemory[:nextDont] + remainingMemory[nextDont+7+nextDo+4:]
		}

		startPosition := 0
		for {
			pos := strings.Index(remainingMemory, "mul(")
			if pos == -1 {
				break
			}
			//fmt.Printf("Pos: %d\n", pos+startPosition+1)

			closeParPos := strings.Index(remainingMemory[pos+4:], ")")
			if closeParPos == -1 {
				break
			}
			inside := remainingMemory[pos+4 : pos+4+closeParPos]
			//fmt.Printf("    Inside: #%s#\n", inside)

			startPosition += pos + 4
			remainingMemory = remainingMemory[pos+4:]

			insideParts := strings.Split(inside, ",")
			if len(insideParts) != 2 {
				continue
			}
			leftNumber, err := strconv.Atoi(insideParts[0])
			if err != nil {
				continue
			}
			if leftNumber > 999 || leftNumber < 0 {
				continue
			}
			rightNumber, err := strconv.Atoi(insideParts[1])
			if err != nil {
				continue
			}
			if rightNumber > 999 || rightNumber < 0 {
				continue
			}
			//fmt.Printf("    Left: %d, Right: %d\n", leftNumber, rightNumber)
			total += leftNumber * rightNumber

		}
	}
	return total
}

func main() {
	// Uncomment this line to disable garbage collection
	// debug.SetGCPercent(-1)

	var input []byte
	var err error
	if len(os.Args) > 1 {
		// Read input from file for local debugging
		input, err = os.ReadFile(os.Args[1])
		if err != nil {
			panic(err)
		}
		// Remove extra newline
		input = input[:len(input)-1]
	} else {
		// Read input from stdin
		input, err = io.ReadAll(os.Stdin)
		if err != nil {
			panic(err)
		}
	}

	// Start resolution
	start := time.Now()
	result := run(string(input))

	// Print result
	fmt.Printf("_duration:%f\n", time.Since(start).Seconds()*1000)
	fmt.Println(result)
}
