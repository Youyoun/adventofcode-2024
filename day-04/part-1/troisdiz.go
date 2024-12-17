package main

import (
	"fmt"
	"io"
	"os"
	"strings"
	"time"
)

func inGrid(lineCount int, colCount int, line int, col int) bool {
	if (line < 0) || (line >= lineCount) {
		return false
	}
	if (col < 0) || (col >= colCount) {
		return false
	}
	return true
}

func findXmas(grid []string, dirLine int, dirCol int, initLine int, initCol int) int {
	lineCount := len(grid)
	colCount := len(grid[0])
	expected := "XMAS"

	for n := 0; n < len(expected); n++ {
		charLine := initLine + n*dirLine
		charCol := initCol + n*dirCol
		if inGrid(lineCount, colCount, charLine, charCol) {
			if grid[charLine][charCol] != expected[n] {
				return 0
			}
		} else {
			return 0
		}
	}
	//fmt.Printf("[%d, %d] (%d, %d): %s\n", initLine, initCol, dirLine, dirCol, string(grid[initLine][initCol]))
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

	for i := 0; i < len(grid); i++ {
		for j := 0; j < len(grid[i]); j++ {
			if grid[i][j] == 'X' {
				// search XMAS
				// left
				xmasCount += findXmas(grid, -1, 0, i, j)
				// right
				xmasCount += findXmas(grid, 1, 0, i, j)
				// up
				xmasCount += findXmas(grid, 0, -1, i, j)
				// bottom
				xmasCount += findXmas(grid, 0, 1, i, j)

				//left - top
				xmasCount += findXmas(grid, -1, -1, i, j)
				// left - bottom
				xmasCount += findXmas(grid, -1, 1, i, j)
				// right - bottom
				xmasCount += findXmas(grid, 1, 1, i, j)
				// right - up
				xmasCount += findXmas(grid, 1, -1, i, j)
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
