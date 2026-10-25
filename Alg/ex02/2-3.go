package main

import (
	"fmt"
	"math/bits"
)

// SOS2 checks if a subset of 'a' sums to 'b', given '2^b' in the input.
func SOS2(a []int, twoToTheB uint64) bool {
	// Extract the target value 'b' from '2^b'.
	// This operation is O(1) or proportional to the bit length.
	b := bits.TrailingZeros64(twoToTheB)
	m := len(a)

	// Initialize DP table of size b+1.
	// Since 2^b is part of the input, b is polynomial relative to input length n.
	possible := make([]bool, b+1)
	possible[0] = true // 0 can be formed by an empty subset.??


	// Time complexity: O(m * b), which is O(n^2) because b <= n.
	for i := 0; i < m; i++ {
		for j := b; j >= a[i]; j-- {
			if possible[j-a[i]] {
				possible[j] = true // possible[j - a[i]] + possible[j] can form j.
			}
		}
	}

	return possible[b]
}

func main() {
	a := []int{2, 3, 5}
	// b = 6, so 2^b = 64 is given as input.
	var twoToTheB uint64 = 64 
	// create [0-T,1,2-T,3-T,4,5-T,6]

	result := SOS2(a, twoToTheB)
	fmt.Printf("Result: %v\n", result)
}