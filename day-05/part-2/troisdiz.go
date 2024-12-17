package main

import (
	"fmt"
	"io"
	"os"
	"slices"
	"strconv"
	"strings"
	"time"
)

func run(s string) interface{} {
	// Your code goes here
	totalValidMiddles := 0

	rules := make(map[int]map[int]bool)
	inRules := true

	orderingFunc := func(a int, b int) int {
		numbersAfterA, foundRulesStartingWithA := rules[a]
		if foundRulesStartingWithA {
			foundBAfterA := numbersAfterA[b]
			if foundBAfterA {
				return -1
			}
		}
		numbersAfterB, foundRulesStartingWithB := rules[b]
		if foundRulesStartingWithB {
			foundAAfterB := numbersAfterB[a]
			if foundAAfterB {
				return 1
			}
		}
		return 0
	}
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
			selectedArray := make([]int, 0, len(selectedAsStr))
			for i, selectedNbStr := range selectedAsStr {
				selectedNb, err := strconv.Atoi(selectedNbStr)
				if err != nil {
					panic("Conversion issue")
				}
				selectedToPos[selectedNb] = i
				selectedArray = append(selectedArray, selectedNb)
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
			if !orderOK {
				//fmt.Printf("Not Valid: %v\n", selectedAsStr)

				// order correctly
				orderedArray := slices.SortedStableFunc(slices.Values(selectedArray), orderingFunc)
				//fmt.Printf("=> Sorted %v, middle = %d\n", orderedArray, orderedArray[len(orderedArray)/2])
				totalValidMiddles += orderedArray[len(orderedArray)/2]
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
