import java.util.*;
import java.io.*;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Represents a B+ Tree data structure with basic search utilities.
 */
public class BPlusTree {
    /**
     * Fields
     */
    int m;
    InternalNode root;
    LeafNode firstLeaf;

    /**
     * Constructs a new B+ Tree with the specified order (maximum number of child pointers per internal node).
     *
     * @param m The order of the B+ tree.
     */
    public BPlusTree(int m) {
        this.m = m;
        this.root = null;
    }

    /**
     * Performs binary search on an array of DictionaryPair objects.
     *
     * @param dps       The array of DictionaryPair to search.
     * @param numPairs  The number of valid elements in the array.
     * @param t         The key to search for.
     * @return The index of the key if found, otherwise a negative value.
     */
    private int binarySearch(DictionaryPair[] dps, int numPairs, int t) {
        Comparator<DictionaryPair> c = new Comparator<DictionaryPair>() {
            @Override
            public int compare(DictionaryPair o1, DictionaryPair o2) {
                Integer a = Integer.valueOf(o1.key);
                Integer b = Integer.valueOf(o2.key);
                return a.compareTo(b);
            }
        };
        return Arrays.binarySearch(dps, 0, numPairs, new DictionaryPair(t, 0), c);
    }

    /**
     * Finds the leaf node where the given key should reside.
     *
     * @param key The key to search for.
     * @return The LeafNode that may contain the key.
     */
    private LeafNode findLeafNode(int key) {
        Integer[] keys = this.root.keys;
        int i;
        writeDotToFile("find_step0_start_root.dot", this.root, "Find Step 0: Start search at root for key = " + key);
        for (i = 0; i < this.root.degree - 1; i++) {
            if (key < keys[i]) {
                break;
            }
        }
        writeDotToFile("find_step1_descend_index" + i + ".dot", this.root, "Find Step 1: Descend to child index " + i + " for key = " + key);
        Node child = this.root.childPointers[i];
        if (child instanceof LeafNode) {
            writeDotToFile("find_step2_leaf_found.dot", this.root, "Find Step 2: Found leaf node for key = " + key);
            return (LeafNode) child;
        } else {
            return findLeafNode((InternalNode) child, key);
        }
    }

    /**
     * Recursively finds the appropriate leaf node for the given key.
     *
     * @param node The internal node to start the search from.
     * @param key  The key to locate.
     * @return The LeafNode that may contain the key.
     */
    private LeafNode findLeafNode(InternalNode node, int key) {
        Integer[] keys = node.keys;
        int i;
        for (i = 0; i < node.degree - 1; i++) {
            if (key < keys[i]) {
                break;
            }
        }
        writeDotToFile(
                "find_recursive_key" + key + "_node" + node.hashCode() + "_descend" + i + ".dot",
                this.root,
                "Find Recursive: At internal node, key = " + key +
                        ", descend index = " + i + ", keys = " + Arrays.toString(keys)
        );

        Node childNode = node.childPointers[i];
        if (childNode instanceof LeafNode) {
            writeDotToFile(
                    "find_recursive_key" + key + "_leaf_found.dot",
                    this.root,
                    "Find Recursive: Found leaf node for key = " + key
            );
            return (LeafNode) childNode;
        } else {
            return findLeafNode((InternalNode) node.childPointers[i], key);
        }
    }

    /**
     * Finds the index of a given LeafNode in the array of node pointers.
     *
     * @param pointers The array of child pointers.
     * @param node     The leaf node to find.
     * @return The index of the leaf node in the pointer array.
     */
    private int findIndexOfPointer(Node[] pointers, LeafNode node) {
        int i;
        for (i = 0; i < pointers.length; i++) {
            if (pointers[i] == node) {
                break;
            }
        }
        return i;
    }

    /**
     * Calculates the midpoint index used for splitting nodes.
     *
     * @return The midpoint index based on the order of the tree.
     */
    private int getMidpoint() {
        return (int) Math.ceil((this.m + 1) / 2.0) - 1;
    }
    /**
     * Handles the deficiency (underflow) in an internal node by attempting to:
     * <ul>
     *     <li>Borrow a key from a sibling if possible</li>
     *     <li>Merge with a sibling if borrowing is not possible</li>
     *     <li>Re-assign the root if necessary</li>
     * </ul>
     *
     * @param in The deficient InternalNode that needs to be balanced.
     */
    private void handleDeficiency(InternalNode in) {
        writeDotToFile("deficiency_internal_start_" + in.keys[0] + ".dot", in, "Handle Deficiency: Internal Node");
        InternalNode sibling;
        InternalNode parent = in.parent;

        // If the node is the root, reassign a new root
        if (this.root == in) {
            for (int i = 0; i < in.childPointers.length; i++) {
                if (in.childPointers[i] != null) {
                    if (in.childPointers[i] instanceof InternalNode) {
                        this.root = (InternalNode) in.childPointers[i];
                        this.root.parent = null;
                    } else if (in.childPointers[i] instanceof LeafNode) {
                        this.root = null;
                    }
                }
            }
            writeDotToFile("deficiency_root_reassigned_"+ in.keys[0] + ".dot", this.root, "Root reassigned after deficiency");
        }

        // Try borrowing from left sibling
        else if (in.leftSibling != null && in.leftSibling.isLendable()) {
            sibling = in.leftSibling;

            // Get the index of the key and pointer to borrow
            int borrowedKeyIndex = sibling.degree - 2;
            int borrowedKey = sibling.keys[borrowedKeyIndex];
            Node borrowedPointer = sibling.childPointers[sibling.degree - 1];

            // Shift current node's pointers to the right to make space at the beginning
            shiftDown(in.childPointers, 1);
            in.childPointers[0] = borrowedPointer;

            // Set the key from the parent to the current node
            in.keys[0] = parent.keys[parent.findIndexOfPointer(in) - 1];
            in.degree++;

            // Update the parent's key to the borrowed key
            parent.keys[parent.findIndexOfPointer(in) - 1] = borrowedKey;

            // Update the parent pointer of the borrowed child
            borrowedPointer.parent = in;

            // Remove the borrowed pointer and key from the left sibling
            sibling.removePointer(sibling.degree - 1);
            sibling.removeKey(borrowedKeyIndex);
            writeDotToFile("deficiency_borrow_left_internal"+in.keys[0] +".dot", in, "Borrowed from left sibling");
        }
        // Try borrowing from right sibling
        else if (in.rightSibling != null && in.rightSibling.isLendable()) {
            sibling = in.rightSibling;

            int borrowedKey = sibling.keys[0];
            Node pointer = sibling.childPointers[0];

            in.keys[in.degree - 1] = parent.keys[0];
            in.childPointers[in.degree] = pointer;

            parent.keys[0] = borrowedKey;

            sibling.removePointer(0);
            Arrays.sort(sibling.keys);
            sibling.removePointer(0);
            shiftDown(in.childPointers, 1);
            writeDotToFile("deficiency_borrow_right_internal" + in.keys[0] + ".dot", in, "Borrowed from right sibling");
        }
        // Try merging with left sibling
        else if (in.leftSibling != null && in.leftSibling.isMergeable()) {
            sibling = in.leftSibling;

            // Get parent and index of the separator key between sibling and in
            int separatorIndex = parent.findIndexOfPointer(in) - 1;
            int separatorKey = parent.keys[separatorIndex];

            // Append separator key to sibling's keys
            sibling.keys[sibling.degree - 1] = separatorKey;
            Arrays.sort(sibling.keys, 0, sibling.degree);  // Maintain order

            // Move all child pointers from in to sibling
            for (int i = 0; i < in.childPointers.length; i++) {
                Node pointer = in.childPointers[i];
                if (pointer != null) {
                    sibling.appendChildPointer(pointer);
                    pointer.parent = sibling;
                    in.childPointers[i] = null;
                }
            }

            // Update sibling links
            sibling.rightSibling = in.rightSibling;
            if (in.rightSibling != null) {
                in.rightSibling.leftSibling = sibling;
            }

            // Remove in from parent
            parent.removePointer(in);
            parent.removeKey(separatorIndex);

            writeDotToFile("deficiency_merge_left_internal"+in.keys[0]+".dot", sibling, "Merged with left sibling");

        }
        // Try merging with right sibling
        else if (in.rightSibling != null && in.rightSibling.isMergeable()) {
            sibling = in.rightSibling;
            sibling.keys[sibling.degree - 1] = parent.keys[parent.degree - 2];
            Arrays.sort(sibling.keys, 0, sibling.degree);
            parent.keys[parent.degree - 2] = null;

            for (int i = 0; i < in.childPointers.length; i++) {
                if (in.childPointers[i] != null) {
                    sibling.prependChildPointer(in.childPointers[i]);
                    in.childPointers[i].parent = sibling;
                    in.removePointer(i);
                }
            }

            parent.removePointer(in);
            sibling.leftSibling = in.leftSibling;

            writeDotToFile("deficiency_merge_right_internal"+in.keys[0]+".dot", sibling, "Merged with right sibling");

        }

        // Recurse upward if parent is now deficient
        if (parent != null && parent.isDeficient()) {
            handleDeficiency(parent);
        }
    }
    /**
     * Handles deficiency in a leaf node by borrowing or merging.
     *
     * @param ln The deficient leaf node.
     */
    private void handleDeficiency(LeafNode ln) {
        LeafNode sibling;
        InternalNode parent = ln.parent;

        if (ln.leftSibling != null && ln.leftSibling.isLendable()) {
            writeDotToFile("deficiency_borrow_left.dot", ln.leftSibling, "Borrow from left sibling");
            sibling = ln.leftSibling;
            DictionaryPair borrowed = sibling.dictionary[sibling.numPairs - 1];
            ln.insert(borrowed);
            sibling.delete(sibling.numPairs - 1);
            updateParentKey(parent, ln);
        }
        else if (ln.rightSibling != null && ln.rightSibling.isLendable()) {
            writeDotToFile("deficiency_borrow_right.dot", ln.rightSibling, "Borrow from right sibling");
            sibling = ln.rightSibling;
            DictionaryPair borrowed = sibling.dictionary[0];
            ln.insert(borrowed);
            sibling.delete(0);
            updateParentKey(parent, sibling);
        }
        else if (ln.leftSibling != null && ln.leftSibling.isMergeable()) {
            writeDotToFile("deficiency_merge_left.dot", ln.leftSibling, "Merge with left sibling");
            sibling = ln.leftSibling;
            for (int i = 0; i < ln.numPairs; i++) {
                sibling.insert(ln.dictionary[i]);
            }
            sibling.rightSibling = ln.rightSibling;
            if (ln.rightSibling != null) {
                ln.rightSibling.leftSibling = sibling;
            }
            parent.removePointer(ln);
            updateParentKey(parent, sibling);
        }
        else if (ln.rightSibling != null && ln.rightSibling.isMergeable()) {
            writeDotToFile("deficiency_merge_right.dot", ln.rightSibling, "Merge with right sibling");
            sibling = ln.rightSibling;
            for (int i = 0; i < sibling.numPairs; i++) {
                ln.insert(sibling.dictionary[i]);
            }
            ln.rightSibling = sibling.rightSibling;
            if (sibling.rightSibling != null) {
                sibling.rightSibling.leftSibling = ln;
            }
            parent.removePointer(sibling);
            updateParentKey(parent, ln);
        }
        writeDotToFile("deficiency_leaf_resolved.dot", ln, "Deficiency resolved");
        if (parent != null && parent.isDeficient()) {
            handleDeficiency(parent);
        }
    }

    /**
     * Updates the key in the parent that separates the two given leaf nodes.
     *
     * @param parent The parent internal node.
     * @param node   The node whose key needs updating.
     */
    private void updateParentKey(InternalNode parent, LeafNode node) {
        if (parent == null) return;
        int pointerIndex = parent.findIndexOfPointer(node);
        if (pointerIndex > 0) {
            parent.keys[pointerIndex - 1] = node.dictionary[0].key;
        }
    }


    /**
     * Checks whether the B+ tree is empty.
     *
     * @return {@code true} if the tree has no data, otherwise {@code false}.
     */
    private boolean isEmpty() {
        return firstLeaf == null;
    }

    /**
     * Searches for the first {@code null} element in an array of DictionaryPair.
     *
     * @param dps The array of DictionaryPair to search.
     * @return The index of the first {@code null} element, or -1 if none found.
     */
    private int linearNullSearch(DictionaryPair[] dps) {
        for (int i = 0; i < dps.length; i++) {
            if (dps[i] == null) {
                return i;
            }
        }
        return -1;
    }
    /**
     * Searches for the first {@code null} entry in an array of Node pointers.
     *
     * @param pointers The array of Node pointers to search.
     * @return The index of the first {@code null} entry, or -1 if none found.
     */
    private int linearNullSearch(Node[] pointers) {
        for (int i = 0; i < pointers.length; i++) {
            if (pointers[i] == null) {
                return i;
            }
        }
        return -1;
    }

    /**
     * Shifts all non-null Node pointers down by the specified amount.
     *
     * @param pointers The array of Node pointers to shift.
     * @param amount   The number of positions to shift down.
     */
    private void shiftDown(Node[] pointers, int amount) {
        Node[] newPointers = new Node[this.m + 1];
        for (int i = amount; i < pointers.length; i++) {
            newPointers[i - amount] = pointers[i];
        }
        pointers = newPointers;
    }

    /**
     * Sorts a DictionaryPair array using a custom comparator that handles nulls.
     *
     * @param dictionary The array of DictionaryPair to sort.
     */
    private void sortDictionary(DictionaryPair[] dictionary) {
        Arrays.sort(dictionary, new Comparator<DictionaryPair>() {
            @Override
            public int compare(DictionaryPair o1, DictionaryPair o2) {
                if (o1 == null && o2 == null) {
                    return 0;
                }
                if (o1 == null) {
                    return 1;
                }
                if (o2 == null) {
                    return -1;
                }
                return o1.compareTo(o2);
            }
        });
    }

    /**
     * Splits the child pointers of an InternalNode at the given split index.
     *
     * @param in    The internal node whose children are to be split.
     * @param split The index at which to split.
     * @return An array containing the right-half pointers after the split.
     */
    private Node[] splitChildPointers(InternalNode in, int split) {
        Node[] pointers = in.childPointers;
        Node[] halfPointers = new Node[this.m + 1];

        for (int i = split + 1; i < pointers.length; i++) {
            halfPointers[i - split - 1] = pointers[i];
            in.removePointer(i);
        }

        return halfPointers;
    }

    /**
     * Splits the dictionary of a LeafNode at the given index.
     *
     * @param ln    The leaf node whose dictionary is to be split.
     * @param split The index at which to split.
     * @return An array containing the right-half dictionary pairs after the split.
     */
    private DictionaryPair[] splitDictionary(LeafNode ln, int split) {
        DictionaryPair[] dictionary = ln.dictionary;
        DictionaryPair[] halfDict = new DictionaryPair[this.m];

        for (int i = split; i < dictionary.length; i++) {
            halfDict[i - split] = dictionary[i];
            ln.delete(i);
        }

        return halfDict;
    }

    /**
     * Splits an InternalNode into two and promotes the middle key to the parent.
     * If the node is the root, creates a new root.
     *
     * @param in The internal node to be split.
     */
    private void splitInternalNode(InternalNode in) {
        InternalNode parent = in.parent;
        int midpoint = getMidpoint();
        int newParentKey = in.keys[midpoint];

        writeDotToFile("split_step0_before_split.dot", this.root, "Split Step 0: Before splitting internal node");

        Integer[] halfKeys = splitKeys(in.keys, midpoint);
        Node[] halfPointers = splitChildPointers(in, midpoint);

        in.degree = linearNullSearch(in.childPointers);

        InternalNode sibling = new InternalNode(this.m, halfKeys, halfPointers);
        for (Node pointer : halfPointers) {
            if (pointer != null) {
                pointer.parent = sibling;
            }
        }

        sibling.rightSibling = in.rightSibling;
        if (sibling.rightSibling != null) {
            sibling.rightSibling.leftSibling = sibling;
        }
        in.rightSibling = sibling;
        sibling.leftSibling = in;

        writeDotToFile("split_step1_after_sibling.dot", this.root, "Split Step 1: After creating sibling internal node");

        if (parent == null) {
            Integer[] keys = new Integer[this.m];
            keys[0] = newParentKey;
            InternalNode newRoot = new InternalNode(this.m, keys);
            newRoot.appendChildPointer(in);
            newRoot.appendChildPointer(sibling);
            this.root = newRoot;

            in.parent = newRoot;
            sibling.parent = newRoot;
            writeDotToFile("split_step2_new_root.dot", this.root, "Split Step 2: Created new root after internal split");
        } else {
            parent.keys[parent.degree - 1] = newParentKey;
            Arrays.sort(parent.keys, 0, parent.degree);

            int pointerIndex = parent.findIndexOfPointer(in) + 1;
            parent.insertChildPointer(sibling, pointerIndex);
            sibling.parent = parent;
            writeDotToFile("split_step2_promote_key.dot", this.root, "Split Step 2: Promoted key to parent after internal split");
        }

    }

    /**
     * Splits a key array by removing the middle key and returning the right half.
     *
     * @param keys  The original key array.
     * @param split The index at which to split and remove the key.
     * @return The right-half key array after splitting.
     */
    private Integer[] splitKeys(Integer[] keys, int split) {
        Integer[] halfKeys = new Integer[this.m];

        keys[split] = null;

        for (int i = split + 1; i < keys.length; i++) {
            halfKeys[i - split - 1] = keys[i];
            keys[i] = null;
        }

        return halfKeys;
    }
    /**
     * Inserts a key-value pair into the B+ tree.
     * If the appropriate leaf node becomes overfull, a split is triggered,
     * and internal nodes may also be split and rebalanced accordingly.
     *
     * @param key   The integer key to insert.
     * @param value The double value associated with the key.
     */
    public void insert(int key, double value) {
        // if B+- tree is null
        if (isEmpty()) {
            this.firstLeaf = new LeafNode(this.m, new DictionaryPair(key, value));
            writeDotToFile("insert_" + key + "_step0_firstLeaf.dot", this.firstLeaf, "Insert Step 0: Create first leaf with key = " + key);
        } else {
            // 1. Step 1: Search
            LeafNode ln = (this.root == null) ? this.firstLeaf : findLeafNode(key);
            writeDotToFile("insert_" + key + "_step1_foundLeaf.dot", ln, "Insert Step 1: Found leaf for key = " + key);

            // Step 2: Insert into Leaf Node
            if (!ln.insert(new DictionaryPair(key, value))) {
                //Step 3: Overflow → Split
                ln.dictionary[ln.numPairs] = new DictionaryPair(key, value);
                ln.numPairs++;
                sortDictionary(ln.dictionary);
                writeDotToFile("insert_" + key + "_step2_leaf_overflow.dot", ln, "Insert Step 2: Overflow leaf before split");
                // → Split
                int midpoint = getMidpoint();
                DictionaryPair[] rightHalfDict = splitDictionary(ln, midpoint);
                writeDotToFile("insert_" + key + "_step3_leaf_split.dot", ln, "Insert Step 3: Left leaf after split");
                // Step 4: Insert into Parent Node
                // parent exist ??
                if (ln.parent == null) {
                    Integer[] parent_keys = new Integer[this.m];
                    parent_keys[0] = rightHalfDict[0].key;
                    InternalNode parent = new InternalNode(this.m, parent_keys);
                    ln.parent = parent;
                    parent.appendChildPointer(ln);
                    writeDotToFile("insert_" + key + "_step4_new_root.dot", root, "Insert Step 4: New root created");
                } else {
                    int newParentKey = rightHalfDict[0].key;
                    ln.parent.keys[ln.parent.degree - 1] = newParentKey;
                    Arrays.sort(ln.parent.keys, 0, ln.parent.degree);
                    writeDotToFile("insert_" + key + "_step4_update_parent.dot", ln.parent, "Insert Step 4: Updated parent with new key");
                }
                // ln → newLeafNode → next node
                LeafNode newLeafNode = new LeafNode(this.m, rightHalfDict, ln.parent);

                int pointerIndex = ln.parent.findIndexOfPointer(ln) + 1;
                ln.parent.insertChildPointer(newLeafNode, pointerIndex);

                newLeafNode.rightSibling = ln.rightSibling;
                if (newLeafNode.rightSibling != null) {
                    newLeafNode.rightSibling.leftSibling = newLeafNode;
                }
                ln.rightSibling = newLeafNode;
                newLeafNode.leftSibling = ln;

                // root is null ?
                if (this.root == null) {
                    this.root = ln.parent;
                } else {
                    InternalNode in = ln.parent;
                    // Step 5: Recursive Splitting
                    while (in != null) {
                        if (in.isOverfull()) {
                            writeDotToFile("insert_" + key + "_step5_overfull_internal.dot", in, "Insert Step 5: Internal node overfull");
                            splitInternalNode(in);
                        } else {
                            break;
                        }
                        in = in.parent;
                    }
                }
            }
        }
    }

    /**
     * Searches for a key in the B+ tree and returns its corresponding value.
     *
     * @param key The key to search for.
     * @return The associated value if found; otherwise, {@code null}.
     */
    public Double search(int key) {
        // Step 1: Check if the tree is empty
        if (isEmpty()) {
            writeDotToFile("search_" + key + "_step0_empty.dot", null, "Search Step 0: Tree is empty");
            return null;
        }
        // Step 2: Find the appropriate leaf node (either directly or via the root)
        LeafNode ln = (this.root == null) ? this.firstLeaf : findLeafNode(key);
        writeDotToFile("search_" + key + "_step1_found_leaf.dot", ln, "Search Step 1: Found LeafNode for key = " + key);
        // Step 3: Perform binary search within the dictionary array of the leaf
        DictionaryPair[] dps = ln.dictionary;
        int index = binarySearch(dps, ln.numPairs, key);
        writeDotToFile("search_" + key + "_step2_result.dot", ln,
                (index >= 0 ? "Search Step 2: Key found" : "Search Step 2: Key not found"));
        // Step 4: Return the value if found, otherwise null
        if (index < 0) {
            return null;
        } else {
            return dps[index].value;
        }
    }

    /**
     * Searches for all values in the B+ tree whose keys fall within the given range [lowerBound, upperBound].
     *
     * @param lowerBound The lower bound of the key range (inclusive).
     * @param upperBound The upper bound of the key range (inclusive).
     * @return A list of values corresponding to keys within the specified range.
     */
    public ArrayList<Double> search(int lowerBound, int upperBound) {
        ArrayList<Double> values = new ArrayList<Double>();
        LeafNode currNode = this.firstLeaf;
        int step = 0;
        while (currNode != null) {
            writeDotToFile("range_search_" + lowerBound + "_" + upperBound + "_step" + step + ".dot", currNode,
                    "Range Search Step " + step + ": Scanning leaf");
            DictionaryPair[] dps = currNode.dictionary;
            ArrayList<Integer> hits = new ArrayList<>();
            for (DictionaryPair dp : dps) {
                if (dp == null) break;
                if (lowerBound <= dp.key && dp.key <= upperBound) {
                    values.add(dp.value);
                    hits.add(dp.key);
                }
            }
            writeDotToFile(
                    "range_search_" + lowerBound + "_" + upperBound + "_step" + step + ".dot",
                    currNode,
                    "Range Search Step " + step +
                            ": Scanning leaf (Range: [" + lowerBound + ", " + upperBound + "], Hits: " + hits + ")"
            );

            currNode = currNode.rightSibling;
            step++;
        }
        writeDotToFile(
                "range_search_" + lowerBound + "_" + upperBound + "_complete.dot",
                null,
                "Range Search Complete: Range [" + lowerBound + ", " + upperBound + "], Found " + values.size() + " result(s)"
        );
        return values;
    }
    /**
     * Deletes a key from the B+ tree.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (isEmpty()) return;

        LeafNode leaf = (this.root == null) ? this.firstLeaf : findLeafNode(key);
        writeDotToFile("delete_" + key + "_step0_foundLeaf.dot", leaf, "Delete Step 0: Found leaf for key = " + key);
        DictionaryPair[] dps = leaf.dictionary;
        int index = binarySearch(dps, leaf.numPairs, key);

        if (index < 0) return; // key not found

        leaf.delete(index);
        sortDictionary(leaf.dictionary);
        writeDotToFile("delete_" + key + "_step1_deletedKey.dot", leaf, "Delete Step 1: Key deleted from leaf");

        if (leaf == this.firstLeaf && leaf.numPairs == 0) {
            this.firstLeaf = null;
            writeDotToFile("delete_" + key + "_step2_empty_tree.dot", null, "Delete Step 2: Tree is now empty");
            return;
        }

        if (leaf.isDeficient()) {
            writeDotToFile("delete_" + key + "_step3_deficient.dot", leaf, "Delete Step 3: Leaf is deficient");
            handleDeficiency(leaf);
        }
    }

    /**
     * Abstract base class for all nodes in the B+ tree.
     */
    public class Node {
        /** Parent internal node of this node. */
        InternalNode parent;
    }

    /**
     * Represents an internal (non-leaf) node in the B+ tree.
     */
    private class InternalNode extends Node {
        int maxDegree;
        int minDegree;
        int degree;
        InternalNode leftSibling;
        InternalNode rightSibling;
        Integer[] keys;
        Node[] childPointers;

        /**
         * Appends a child pointer to the end of the child pointer array.
         *
         * @param pointer The child node to append.
         */
        private void appendChildPointer(Node pointer) {
            this.childPointers[degree] = pointer;
            this.degree++;
        }

        /**
         * Finds the index of a given child pointer.
         *
         * @param pointer The child node to locate.
         * @return Index of the pointer, or -1 if not found.
         */
        private int findIndexOfPointer(Node pointer) {
            for (int i = 0; i < childPointers.length; i++) {
                if (childPointers[i] == pointer) {
                    return i;
                }
            }
            return -1;
        }

        /**
         * Inserts a child pointer at the specified index and shifts the rest.
         *
         * @param pointer The child node to insert.
         * @param index   The position to insert the pointer.
         */
        private void insertChildPointer(Node pointer, int index) {
            for (int i = degree - 1; i >= index; i--) {
                childPointers[i + 1] = childPointers[i];
            }
            this.childPointers[index] = pointer;
            this.degree++;
        }

        /** @return {@code true} if this node is deficient (under minimum degree). */
        private boolean isDeficient() {
            return this.degree < this.minDegree;
        }

        /** @return {@code true} if this node can lend a child to a sibling. */
        private boolean isLendable() {
            return this.degree > this.minDegree;
        }

        /** @return {@code true} if this node is exactly at the mergeable threshold. */
        private boolean isMergeable() {
            return this.degree == this.minDegree;
        }

        /** @return {@code true} if this node exceeds the maximum degree. */
        private boolean isOverfull() {
            return this.degree == maxDegree + 1;
        }

        /**
         * Prepends a child pointer to the beginning of the child pointer array.
         *
         * @param pointer The child node to prepend.
         */
        private void prependChildPointer(Node pointer) {
            for (int i = degree - 1; i >= 0; i--) {
                childPointers[i + 1] = childPointers[i];
            }
            this.childPointers[0] = pointer;
            this.degree++;
        }

        /**
         * Removes the key at the specified index by setting it to {@code null}.
         *
         * @param index Index of the key to remove.
         */
        private void removeKey(int index) {
            this.keys[index] = null;
        }

        /**
         * Removes the child pointer at the specified index.
         *
         * @param index Index of the pointer to remove.
         */
        private void removePointer(int index) {
            this.childPointers[index] = null;
            this.degree--;
        }

        /**
         * Removes a specific pointer from the childPointers array.
         *
         * @param pointer The node pointer to remove.
         */
        private void removePointer(Node pointer) {
            for (int i = 0; i < childPointers.length; i++) {
                if (childPointers[i] == pointer) {
                    this.childPointers[i] = null;
                }
            }
            this.degree--;
        }

        /**
         * Constructs an internal node with only keys initialized.
         *
         * @param m    The maximum degree.
         * @param keys The key array to assign.
         */
        private InternalNode(int m, Integer[] keys) {
            this.maxDegree = m;
            this.minDegree = (int) Math.ceil(m / 2.0);
            this.degree = 0;
            this.keys = keys;
            this.childPointers = new Node[this.maxDegree + 1];
        }

        /**
         * Constructs an internal node with both keys and pointers initialized.
         *
         * @param m        The maximum degree.
         * @param keys     The key array.
         * @param pointers The child pointer array.
         */
        private InternalNode(int m, Integer[] keys, Node[] pointers) {
            this.maxDegree = m;
            this.minDegree = (int) Math.ceil(m / 2.0);
            this.degree = linearNullSearch(pointers);
            this.keys = keys;
            this.childPointers = pointers;
        }
    }


    /**
     * Represents a leaf node in the B+ tree.
     */
    public class LeafNode extends Node {
        int maxNumPairs;
        int minNumPairs;
        int numPairs;
        LeafNode leftSibling;
        LeafNode rightSibling;
        DictionaryPair[] dictionary;

        /**
         * Constructs a new leaf node with pre-filled dictionary pairs and parent.
         *
         * @param m        The order of the B+ tree.
         * @param dps      The dictionary pairs to assign.
         * @param parent   The parent internal node.
         */
        public LeafNode(int m, DictionaryPair[] dps, InternalNode parent) {
            this.maxNumPairs = m - 1;
            this.minNumPairs = (int) (Math.ceil(m / 2.0) - 1);
            this.dictionary = dps;
            this.numPairs = linearNullSearch(dps);
            this.parent = parent;
        }
        /**
         * Removes the dictionary pair at the specified index.
         *
         * @param index The index of the pair to delete.
         */
        public void delete(int index) {
            this.dictionary[index] = null;
            numPairs--;
        }

        /**
         * Inserts a dictionary pair if space is available.
         *
         * @param dp The dictionary pair to insert.
         * @return {@code true} if inserted successfully; {@code false} if full.
         */
        public boolean insert(DictionaryPair dp) {
            if (this.isFull()) {
                return false;
            } else {
                this.dictionary[numPairs] = dp;
                numPairs++;
                Arrays.sort(this.dictionary, 0, numPairs);
                return true;
            }
        }

        /** @return {@code true} if the node is deficient (under min pair count). */
        public boolean isDeficient() {
            return numPairs < minNumPairs;
        }

        /** @return {@code true} if the node is full. */
        public boolean isFull() {
            return numPairs == maxNumPairs;
        }

        /** @return {@code true} if the node can lend a pair. */
        public boolean isLendable() {
            return numPairs > minNumPairs;
        }

        /** @return {@code true} if the node is exactly at the merge threshold. */
        public boolean isMergeable() {
            return numPairs == minNumPairs;
        }

        /**
         * Constructs a new leaf node and inserts the initial key-value pair.
         *
         * @param m  The order of the B+ tree.
         * @param dp The dictionary pair to insert initially.
         */
        public LeafNode(int m, DictionaryPair dp) {
            this.maxNumPairs = m - 1;
            this.minNumPairs = (int) (Math.ceil(m / 2.0) - 1);
            this.dictionary = new DictionaryPair[m];
            this.numPairs = 0;
            this.insert(dp);
        }
    }
    /**
     * Represents a key-value pair stored in a leaf node of a B+ tree.
     * Implements {@link Comparable} to allow sorting based on keys.
     */
    public class DictionaryPair implements Comparable<DictionaryPair> {

        /** The integer key used for ordering and lookup. */
        int key;

        /** The double value associated with the key. */
        double value;

        /**
         * Constructs a new DictionaryPair with the specified key and value.
         *
         * @param key   The integer key.
         * @param value The value associated with the key.
         */
        public DictionaryPair(int key, double value) {
            this.key = key;
            this.value = value;
        }

        /**
         * Compares this DictionaryPair with another based on the key.
         *
         * @param o The DictionaryPair to compare to.
         * @return A negative integer, zero, or a positive integer if this key is
         *         less than, equal to, or greater than the specified key.
         */
        @Override
        public int compareTo(DictionaryPair o) {
            if (key == o.key) {
                return 0;
            } else if (key > o.key) {
                return 1;
            } else {
                return -1;
            }
        }
    }
    /**
     * Generates a Graphviz DOT format string representing the current B+ tree structure,
     * highlighting the specified current node and displaying an inline comment label.
     * @return A string in DOT format describing the B+ tree.
     */
    public String generateDot(Node current, String comment) {
        StringBuilder sb = new StringBuilder();
        sb.append("digraph BPlusTree {\n");
        sb.append("    node [shape=record];\n");
        // Optional global label (top annotation)
        if (comment != null && !comment.isEmpty()) {
            sb.append("    label = \"").append(comment).append("\";\n");
            sb.append("    labelloc = \"top\";\n");
            sb.append("    fontsize = 16;\n");
        }

        int[] nodeIdCounter = {0};
        Map<Node, String> nodeIds = new HashMap<>();

        if (root == null && firstLeaf != null) {
            // Only one leaf node exists
            String nodeId = "Leaf0";
            nodeIds.put(firstLeaf, nodeId);

            sb.append("    ").append(nodeId).append(" [label=\"");
            for (int i = 0; i < firstLeaf.numPairs; i++) {
                if (i > 0) sb.append(" | ");
                sb.append("<f").append(i).append("> ").append(firstLeaf.dictionary[i].key)
                        .append(" | ").append(firstLeaf.dictionary[i].value);
            }
            sb.append("\"");

            // 🔴 Highlight the current node
            if (firstLeaf == current) {
                sb.append(", color=red, fontcolor=red");
            }

            sb.append("];\n");
            sb.append("}\n");
            return sb.toString();
        }

        traverseAndBuildDot(root, sb, nodeIds, nodeIdCounter, current);

        // Link leaf nodes from left to right
        LeafNode curr = firstLeaf;
        while (curr != null && curr.rightSibling != null) {
            String currId = nodeIds.get(curr);
            String nextId = nodeIds.get(curr.rightSibling);
            sb.append("    ").append(currId).append(" -> ").append(nextId).append(";\n");
            curr = curr.rightSibling;
        }
        sb.append("    ").append("{ rank = same; ");
        curr = firstLeaf;
        while (curr != null) {
            sb.append(nodeIds.get(curr)).append("; ");
            curr = curr.rightSibling;
        }
        sb.append("}\n");

        sb.append("}\n");
        return sb.toString();
    }
    /**
     * Recursively traverses the B+ tree and builds DOT node definitions and edges.
     *
     * @param node         The current node to process.
     * @param sb           The StringBuilder to append DOT content to.
     * @param nodeIds      A map of node objects to unique DOT node IDs.
     * @param idCounter    An array holding a single counter value to generate unique IDs.
     */
    private void traverseAndBuildDot(Node node, StringBuilder sb, Map<Node, String> nodeIds, int[] idCounter,Node current) {
        switch (node) {
            case LeafNode ln -> {
                String nodeId = "Leaf" + idCounter[0]++;
                nodeIds.put(ln, nodeId);

                sb.append("    ").append(nodeId).append(" [label=\"");
                for (int i = 0; i < ln.numPairs; i++) {
                    if (i > 0) sb.append(" | ");
                    sb.append("<f").append(i).append("> ").append(ln.dictionary[i].key)
                            .append(" | ").append(ln.dictionary[i].value);
                }
                sb.append("\"");

                // 🔴 Highlight if current
                if (ln == current) {
                    sb.append(", color=red, fontcolor=red");
                }

                sb.append("];\n");

            }
            case InternalNode in -> {
                String nodeId = "Node" + idCounter[0]++;
                nodeIds.put(in, nodeId);

                sb.append("    ").append(nodeId).append(" [label=\"");
                for (int i = 0; i < in.degree - 1; i++) {
                    sb.append("<f").append(i).append("> | ").append(in.keys[i]).append(" | ");
                }
                sb.append("<f").append(in.degree - 1).append(">\"");

                // 🔴 Highlight if current
                if (in == current) {
                    sb.append(", color=red, fontcolor=red");
                }

                sb.append("];\n");

                for (int i = 0; i < in.degree; i++) {
                    Node child = in.childPointers[i];
                    if (child != null) {
                        traverseAndBuildDot(child, sb, nodeIds, idCounter,current);
                        String childId = nodeIds.get(child);
                        sb.append("    ").append(nodeId).append(":f").append(i)
                                .append(" -> ").append(childId).append(";\n");
                    }
                }
            }
            case null, default -> {
            }
        }

    }

    /**
     * Writes the B+ tree structure to a DOT file that can be rendered using Graphviz with a time stamp.
     *
     * @param filename The name of the DOT file to create.
     */
    private static final AtomicInteger fileCounter = new AtomicInteger();
    public void writeDotToFile(String filename, Node current, String comment) {
        String timestamp = new java.text.SimpleDateFormat("yyyyMMdd_HHmmss").format(new java.util.Date());
        int index = fileCounter.getAndIncrement();  // Ensures order
        String uniqueId = String.format("%s_%04d", timestamp, index);
        filename = filename.replace(".dot", "") + "_" + uniqueId + ".dot";

        String dotContent = generateDot(current, comment);
        String outputDir = "output";
        File dir = new File(outputDir);
        if (!dir.exists()) {
            dir.mkdirs();
        }
        try (FileWriter writer = new FileWriter(outputDir + "/" + filename)) {
            writer.write(dotContent);
            System.out.println("DOT file successfully written to: " + outputDir + "/" + filename);
        } catch (IOException e) {
            System.err.println("Error writing DOT file: " + e.getMessage());
        }
    }
}