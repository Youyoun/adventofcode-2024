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
	totalValidMiddles := 0

	rules := make(map[int]map[int]bool)
	inRules := true
	for _, line := range strings.Split(s, "\n") {
		//fmt.Printf("Line: %s\n", line)
		if inRules {
			if line == "" {
				inRules = false
				/*
					for ruleLeft, ruleRight := range rules {
						fmt.Printf("%d -> %v\n", ruleLeft, ruleRight)
					}*/

				continue
			}
			numbers := strings.Split(line, "|")
			first, _ := strconv.Atoi(numbers[0])
			second, _ := strconv.Atoi(numbers[1])
			rulesStartingWithFirst, ok := rules[first]
			if !ok {
				rulesStartingWithFirst = make(map[int]bool)
				rules[first] = rulesStartingWithFirst
			}
			rulesStartingWithFirst[second] = true
		} else {
			selectedAsStr := strings.Split(line, ",")
			if len(selectedAsStr)%2 != 1 {
				fmt.Printf("%v = %d values!!!\n", selectedAsStr, len(selectedAsStr))
			}
			selectedToPos := make(map[int]int, len(selectedAsStr))
			middleNb := 0
			for i, selectedNbStr := range selectedAsStr {
				selectedNb, err := strconv.Atoi(selectedNbStr)
				if err != nil {
					panic("Conversion issue")
				}
				selectedToPos[selectedNb] = i
				if i == len(selectedAsStr)/2 {
					middleNb = selectedNb
				}
			}
			orderOK := true
		loop:
			for nb, pos := range selectedToPos {

				furtherNumbersInRules, furtherNbInRuleFound := rules[nb]
				if !furtherNbInRuleFound {
					// No rule starting with nb
					continue
				}
				for furtherNumberInRules, _ := range furtherNumbersInRules {
					furtherNbInRulePos, furtherNbFound := selectedToPos[furtherNumberInRules]
					if !furtherNbFound {
						// this second part of the rule is not in the selected pages
						continue
					}
					if pos > furtherNbInRulePos {
						orderOK = false
						break loop
					}
				}

			}
			if orderOK {
				//fmt.Printf("Valid: %v, middle = %d\n", selectedAsStr, middleNb)
				totalValidMiddles += middleNb
			}
		}
	}

	return totalValidMiddles
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
