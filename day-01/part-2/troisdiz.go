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
	// Your code goes here
	leftSlice := []int{}
	rightSlice := []int{}
	//fmt.Println("Start")
	lines := strings.Split(s, "\n")
	for _, line := range lines {
		items := strings.Split(line, "   ")
		//fmt.Printf("items: #%s# / #%s#\n", items[0], items[1])
		leftInt, _ := strconv.Atoi(items[0])
		leftSlice = append(leftSlice, leftInt)
		rightInt, _ := strconv.Atoi(items[1])
		rightSlice = append(rightSlice, rightInt)
	}
	rightFreqs := make(map[int]int, len(rightSlice))
	for _, right := range rightSlice {
		count := rightFreqs[right]
		rightFreqs[right] = count + 1
	}
	totalScore := 0
	for _, left := range leftSlice {
		count := rightFreqs[left]
		totalScore += left * count
	}
	fmt.Println("Before return")
	return totalScore
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
