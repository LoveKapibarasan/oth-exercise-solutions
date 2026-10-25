package main

import (
	"fmt"
	"time"
)

type State struct {
	id int // 0-11
	h  int // 1: heavy, -1: light
}

type Node struct {
	left, right []int
	children    map[int]*Node
	answer      *State
}

func main() {
    start := time.Now()
    bulletsCount := 12
    maxDepth := 3

    states := make([]State, 0, bulletsCount*2)
    for i := 0; i < bulletsCount; i++ {
        states = append(states, State{i, 1}, State{i, -1})
    }

    allBulletIDs := make([]int, bulletsCount)
    for i := 0; i < bulletsCount; i++ {
        allBulletIDs[i] = i
    }

    fmt.Printf("Starting Brute-force search for the %d-bullet puzzle...\n", bulletsCount)
    success, tree := solve(states, maxDepth, allBulletIDs)

    if success {
        fmt.Printf("\nStrategy found in %v\n", time.Since(start))
        printTree(tree, 0, "Initial")
    } else {
        fmt.Printf("No strategy exists for %d bullets with %d weighings.\n", bulletsCount, maxDepth)
    }
}

func solve(currentStates []State, depth int, allBulletIDs []int) (bool, *Node) {
    if len(currentStates) == 1 {
        return true, &Node{answer: &currentStates[0]}
    }
    if depth == 0 {
        return false, nil
    }

    maxAllowed := 1
    for i := 0; i < depth; i++ { maxAllowed *= 3 }
    if len(currentStates) > maxAllowed {
        return false, nil
    }

    // BRUTE FORCE !!: Try all possible ways to put 'n' bullets on each pan (1vs1 to max possible).
    for size := 1; size <= len(allBulletIDs)/2; size++ {
        weighings := generateAllWeighings(size, allBulletIDs)
        for _, w := range weighings {
            // Partition current suspect states based on the weighing result.
            groups := [3][]State{} // 0:Balanced, 1:LeftHeavy, 2:RightHeavy
            for _, s := range currentStates {
                res := getOutcome(s, w.left, w.right)
                groups[res] = append(groups[res], s)
            }

            // Pruning: Every branch must be <= 3^(depth-1).
            nextMax := maxAllowed / 3
            if len(groups[0]) > nextMax || len(groups[1]) > nextMax || len(groups[2]) > nextMax {
                continue
            }
            // Skip weighings that provide zero information.
            if len(groups[0]) == len(currentStates) {
                continue
            }

            // Recursively check if this weighing leads to a complete solution.
            node := &Node{left: w.left, right: w.right, children: make(map[int]*Node)}
            allBranchesSolved := true
            for i := 0; i < 3; i++ {
                if len(groups[i]) > 0 {
                    ok, child := solve(groups[i], depth-1, allBulletIDs)
                    if !ok {
                        allBranchesSolved = false
                        break
                    }
                    node.children[i] = child
                }
            }

            if allBranchesSolved {
                return true, node
            }
        }
    }
    return false, nil
}

func generateAllWeighings(size int, bullets []int) []struct{ left, right []int } {
    var result []struct{ left, right []int }
    
    combinations(bullets, size, func(left []int) {
        remaining := sliceDifference(bullets, left)
        combinations(remaining, size, func(right []int) {
            result = append(result, struct{ left, right []int }{
                left:  append([]int(nil), left...),
                right: append([]int(nil), right...),
            })
        })
    })
    return result
}

// combinations is a helper to generate k-size subsets.
func combinations(set []int, k int, f func([]int)) {
	if k == 0 {
		f(nil)
		return
	}
	if len(set) < k { return }
	
	for i := 0; i <= len(set)-k; i++ {
		combinations(set[i+1:], k-1, func(sub []int) {
			f(append([]int{set[i]}, sub...))
		})
	}
}

func sliceDifference(a, b []int) []int {
	m := make(map[int]bool)
	for _, x := range b { m[x] = true }
	var res []int
	for _, x := range a {
		if !m[x] { res = append(res, x) }
	}
	return res
}

func getOutcome(s State, left, right []int) int {
	val := 0
	for _, b := range left { if s.id == b { val = s.h } }
	for _, b := range right { if s.id == b { val = -s.h } }
	if val == 0 { return 0 }
	if val > 0 { return 1 }
	return 2
}

func printTree(n *Node, depth int, path string) {
	padding := ""
	for i := 0; i < depth; i++ { padding += "  " }
	
	if n.answer != nil {
		label := "Heavy"
		if n.answer.h == -1 { label = "Light" }
		fmt.Printf("%s[%s] -> FOUND: Bullet %d is %s\n", padding, path, n.answer.id, label)
		return
	}
	
	fmt.Printf("%s[%s] Weigh Left%v vs Right%v\n", padding, path, n.left, n.right)
	for i, label := range []string{"Balanced", "LeftHeavy", "RightHeavy"} {
		if child, ok := n.children[i]; ok {
			printTree(child, depth+1, label)
		}
	}
}