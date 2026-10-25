package main

import "fmt"

// SOS (Sum of Subsets) - Definition 44
// Checks if there exists a subset of 'w' that sums exactly to 'target'
func SOS(w []int, target int) bool {
	if target < 0 {
		return false
	}
	dp := make([]bool, target+1)
	dp[0] = true

	for _, val := range w {
		for i := target; i >= val; i-- {
			if dp[i-val] {
				dp[i] = true
			}
		}
	}
	return dp[target]
}

// PARTITION - Definition 62
// Checks if there exists a subset I such that sum(elements in I) == sum(elements not in I)
func PARTITION(a []int) bool {
	sum := 0
	for _, v := range a {
		sum += v
	}
	if sum%2 != 0 { // the sum was odd
		return false
	}
	// According to the definition, this is equivalent to finding a subset that sums to total/2
	return SOS(a, sum/2)
}

// Reduction: PARTITION <=p SOS
// Transforms a PARTITION instance into an SOS instance
func PartitionToSOS(a []int) (int, []int) {
	sum := 0
	for _, v := range a {
		sum += v
	}
	// The target for SOS is half of the total sum
	target := sum / 2
	weights := a
	return target, weights
}

// Reduction: SOS <=p PARTITION
// Transforms an SOS instance (w, target) into a PARTITION instance
// To do this, we add two special elements to the set to force the partition
func SOSToPartition(w []int, target int) []int {
	sum := 0
	for _, v := range w {
		sum += v
	}

	// Create a new set A' = {w1, ..., wn, s1, s2}
	// where s1 = sum + 1 - target and s2 = target + 1
	s1 := sum + 1 - target
	s2 := target + 1
	
	newSet := make([]int, len(w))
	copy(newSet, w)
	newSet = append(newSet, s1, s2)
	
	return newSet
}

func main() {
	// --- Example 1: PARTITION to SOS ---
	a := []int{1, 2, 3, 4, 10}
	t, w := PartitionToSOS(a)
	fmt.Printf("PARTITION instance %v reduced to SOS(target: %d, weights: %v)\n", a, t, w)
	fmt.Printf("Result: %v\n\n", SOS(w, t))

	// --- Example 2: SOS to PARTITION ---
	w2 := []int{3, 34, 4, 12, 5, 2}
	target2 := 9
	partitionInstance := SOSToPartition(w2, target2)
	fmt.Printf("SOS instance (w: %v, target: %d) reduced to PARTITION instance: %v\n", w2, target2, partitionInstance)
	fmt.Printf("Result: %v\n", PARTITION(partitionInstance))
}