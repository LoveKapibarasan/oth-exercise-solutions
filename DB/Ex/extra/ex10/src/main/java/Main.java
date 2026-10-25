import java.util.List;
import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        List<Integer> orders = Arrays.asList(4, 6, 8); // n = max pointers per node
        List<Integer> initialKeys = Arrays.asList(2, 3, 5, 7, 11, 17, 19, 23, 29, 31);
        List<Integer> deletes = Arrays.asList(23, 19);
        List<Integer> inserts = Arrays.asList(9, 10, 8);

        for (Integer n : orders) {
            System.out.println("Building B+ tree with order n = " + n);
            BPlusTree bpt = new BPlusTree(n);

            // Step a) Insert initial keys
            for (Integer key : initialKeys) {
                bpt.insert(key, key); // value = same as key for simplicity
                if (inserts.contains(key)) {
                    String baseName = "n-" + n + "_insert" + key;
                    bpt.writeDotToFile(baseName + ".dot", null, "Initial tree (n=" + n + ")");
                }
            }
            String baseName = "n" + n + "_initial";
            bpt.writeDotToFile(baseName + ".dot", null, "Initial tree (n=" + n + ")");
            if (n == 4){
                bpt.search(11);
                bpt.search(6,20);
            }
            for (Integer key : deletes) {
                bpt.delete(key);
                bpt.writeDotToFile("n-" + n + "_delete" + key + ".dot", null, "After deleting " + key);
            }
        }
    }
}
