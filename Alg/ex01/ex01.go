package main

import (
	"fmt"
)

func cA(x, y, z uint64) bool {
	// Handle edge cases ( 4 ?)
	if z == 0 {
		return false
	}
	if y == 0 {
		return z == 1 // x^0 is always 1
	}
	if x == 0 {
		return z == 0 // 0^y is always 0
	}
	if x == 1 {
		return z == 1 // 1^y is always 1
	}

	// Binary Exponentiation
	var res uint64 = 1
	base := x
	// l(y) loops
    for y > 0 {
        if y%2 == 1 {
            res = res * base
        }

        y = y / 2
        if y > 0 {
            base = base * base
        }
    }
    return res == z

}

func main() {
	fmt.Printf("3^8 == 6561: %v\n", cA(3, 8, 6561))   // true
}