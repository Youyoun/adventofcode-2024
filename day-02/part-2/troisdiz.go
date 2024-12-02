package main

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
	"time"
)

func signAndAbs(value int) (int, int) {
	if value < 0 {
		return -1, -value
	} else if value > 0 {
		return 1, value
	} else {
		return 0, 0
	}
}

func isReportSafe(levels []int, reportId int) bool {
	//fmt.Printf("isReportSafe(%d): %v, ignore %d)\n", reportId+1, levels)
	diffSignSoFar := 0
	safe := true
loop:
	for i := 0; i < len(levels)-1; i++ {
		diff := levels[i+1] - levels[i]
		sign, absValue := signAndAbs(diff)
		if absValue < 1 || absValue > 3 {
			//fmt.Printf("    Line %d is Unsafe: absDiff(%d)=%d\n", reportId+1, i, absValue)
			safe = false
			break loop
		}
		if diffSignSoFar == 0 {
			diffSignSoFar = sign
		} else if (diffSignSoFar * sign) == -1 {
			//fmt.Printf("    Line %d is Unsafe: Diff(%d) sign (%d) is different from origin (%d)\n", reportId+1, i, diff, diffSignSoFar)
			safe = false
			break loop
		}
	}
	/*
		if safe {
			fmt.Printf("    Line %d is safe\n", reportId+1)
		}
	*/
	return safe
}

func run(s string) interface{} {
	// Your code goes here
	lines := strings.Split(s, "\n")
	safeCount := 0
	for lineIdx, line := range lines {
		items := strings.Split(line, " ")
		levels := make([]int, len(items))
		for i, item := range items {
			level, _ := strconv.Atoi(item)
			levels[i] = level
		}

		if isReportSafe(levels, lineIdx) {
			safeCount++
		} else {
			for i := 0; i < len(levels); i++ {
				newLevels := make([]int, len(levels)-1)
				idx := 0
				for j, value := range levels {
					if j != i {
						newLevels[idx] = value
						idx++
					}
				}
				if isReportSafe(newLevels, lineIdx) {
					safeCount++
					break
				}
			}
		}
	}
	return safeCount
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
