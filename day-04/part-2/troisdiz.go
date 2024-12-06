package main

import (
	"fmt"
	"io"
	"os"
	"strings"
	"time"
)

func findXmas(grid []string, initLine int, initCol int) int {
	if grid[initLine][initCol] != 'A' {
		return 0
	}
	topLeft := grid[initLine-1][initCol-1]
	topRight := grid[initLine+1][initCol-1]
	bottomLeft := grid[initLine-1][initCol+1]
	bottomRight := grid[initLine+1][initCol+1]
	if (topLeft != 'M') && (topLeft != 'S') {
		return 0
	}
	if (topRight != 'M') && (topRight != 'S') {
		return 0
	}
	if (bottomLeft != 'M') && (bottomLeft != 'S') {
		return 0
	}
	if (bottomRight != 'M') && (bottomRight != 'S') {
		return 0
	}
	if topLeft == bottomRight {
		return 0
	}
	if bottomLeft == topRight {
		return 0
	}
	return 1
}

func run(s string) interface{} {
	// Your code goes here
	xmasCount := 0
	grid := strings.Split(s, "\n")
	/*
		for idx, line := range grid {
			fmt.Printf("[%d] %s\n", idx, line)
		}*/

	for i := 1; i < len(grid)-1; i++ {
		for j := 1; j < len(grid[i])-1; j++ {
			if grid[i][j] == 'A' {
				// search XMAS
				xmasCount += findXmas(grid, i, j)
			}
		}
	}
	return xmasCount
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
