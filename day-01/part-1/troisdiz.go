package main

import (
	"fmt"
	"io"
	"os"
	"sort"
	"strconv"
	"strings"
	"time"
)

func run(s string) interface{} {
	// Your code goes here
	leftSlice := []int{}
	rightSlice := []int{}
	lines := strings.Split(s, "\n")
	for _, line := range lines {
		items := strings.Split(line, "   ")
		leftInt, _ := strconv.Atoi(items[0])
		leftSlice = append(leftSlice, leftInt)
		rightInt, _ := strconv.Atoi(items[1])
		rightSlice = append(rightSlice, rightInt)
	}
	sort.Ints(leftSlice)
	sort.Ints(rightSlice)
	totalDiff := 0
	for i := 0; i < len(leftSlice); i++ {
		diff := leftSlice[i] - rightSlice[i]
		if diff < 0 {
			diff = -diff
		}
		totalDiff += diff
	}
	return totalDiff
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
