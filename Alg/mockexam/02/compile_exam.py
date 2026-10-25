import os
import subprocess

# Define directory and paths
mockexam_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(mockexam_dir, exist_ok=True)

latex_code_template = """\\documentclass[12pt,addpoints]{exam}
\\usepackage{amsmath,amssymb,amsthm}
\\usepackage{geometry}
\\geometry{a4paper, margin=1in}
\\usepackage{listings}
\\usepackage{graphicx}
\\usepackage{tikz}
\\lstset{basicstyle=\\small\\ttfamily, breaklines=true, breakatwhitespace=false, columns=fullflexible}

% SOLUTION_SWITCH_PLACEHOLDER

\\title{Mock Examination (Advanced Level): Advanced Algorithms --- Round 2}
\\author{Course: Advanced Algorithms (EX01--EX15)}
\\date{Time Allowed: 120 minutes \\\\ Total Points: 100}

\\begin{document}

\\maketitle

\\begin{center}
\\fbox{\\fbox{\\parbox{5.5in}{\\centering
\\textbf{Instructions to Candidates:}
\\begin{itemize}
    \\item This exam contains 6 questions covering NP-Completeness, Engineering Game AIs, and Algorithmic Number Theory \\& Cryptography.
    \\item Answer all questions in English.
    \\item Show all working out and proofs clearly.
    \\item No calculators or external materials are permitted.
\\end{itemize}
}}}
\\end{center}

\\vspace{0.2in}
\\gradetable[v][questions]
\\newpage

\\begin{questions}

%=============================================================================
% QUESTION 1
%=============================================================================
\\question[15] \\textbf{NP-Completeness: Concepts and Membership in NP}

\\begin{parts}
\\part[6] \\textbf{Prove or refute} each of the following statements. A correct verdict without justification receives no credit.
\\begin{subparts}
    \\subpart[2] If $B$ is NP-hard and $A \\le_p B$, then $A$ is NP-complete.
    \\subpart[1] $\\text{NP} \\subseteq \\text{EXP}$.
    \\subpart[2] If some NP-complete problem is decidable in polynomial time, then $\\text{P} = \\text{NP}$.
    \\subpart[1] Given ciphertexts $c_1 \\equiv m^{e_1} \\pmod n$ and $c_2 \\equiv m^{e_2} \\pmod n$ with $\\gcd(e_1,e_2)=1$, the Common Modulus Attack can recover $m$ only after first factoring $n$ into its prime components $p,q$.
\\end{subparts}

\\begin{solution}
\\begin{subparts}
    \\subpart \\textbf{Refuted (False).} The direction of the reduction only shows that $A$ is \\emph{no harder than} $B$; it gives no lower bound on the hardness of $A$. Counterexample: let $A := \\emptyset \\in \\text{P}$ and $B := \\text{SAT}$ (NP-hard). By Theorem 1.55.1 ($A \\in \\text{P}, B \\ne \\emptyset \\implies A \\le_p B$), we have $\\emptyset \\le_p \\text{SAT}$. But $\\emptyset$ is not NP-hard (unless $\\text{P}=\\text{NP}$), so $A$ is not NP-complete.

    \\subpart \\textbf{True.} This is Theorem 1.38: every non-deterministic polynomial-time computation can be simulated deterministically by exhaustively trying all polynomially-many-bit certificates, which takes at most exponential time. Hence $\\text{NP} \\subseteq \\text{EXP}$.

    \\subpart \\textbf{True.} If an NP-complete problem $B$ is in P, then by Theorem 1.54.1, every $A \\in \\text{NP}$ satisfies $A \\le_p B$ and $B \\in \\text{P}$, hence $A \\in \\text{P}$. Thus $\\text{NP} \\subseteq \\text{P}$, and combined with $\\text{P} \\subseteq \\text{NP}$ (Theorem 1.36), we get $\\text{P} = \\text{NP}$.

    \\subpart \\textbf{Refuted (False).} The Common Modulus Attack (as shown on the previous mock exam) computes Bézout coefficients $a,b$ with $a e_1 + b e_2 = 1$ via the Extended Euclidean Algorithm, and then recovers $m \\equiv c_1^a \\cdot (c_2^{-1})^{-b} \\pmod n$ --- entirely without factoring $n$. Factoring $n$ is not required (and, in fact, if it were easy to factor $n$, there would be no need for this attack at all, since $\\varphi(n)$ and hence the private key could be computed directly).
\\end{subparts}
\\end{solution}

\\part[9] Recall the Hamiltonian Cycle problem, $\\text{HC}$: the set of (encodings of) undirected graphs $G=(V,E)$ that have a Hamiltonian cycle. Prove that $\\text{HC} \\in \\text{NP}$ \\textbf{directly from Definition 1.34}: specify a certificate encoding, a polynomial bound on its length, and a polynomial-time verifier set $B$, and prove the required equivalence. Then, in the style of Example 1.49 (the non-deterministic algorithm for BP), sketch a non-deterministic polynomial-time algorithm that accepts $\\text{HC}$.

\\begin{solution}
Let $x = \\langle G \\rangle$ with $G = (V,E)$ and $n := |V|$ (identify $V = \\{1,\\dots,n\\}$).

\\textbf{Certificate:} A potential solution is a sequence $(v_1,\\dots,v_n)$ representing the order in which the Hamiltonian cycle visits the vertices. We encode it as the natural number $y := \\langle v_1,\\dots,v_n \\rangle$ using the standard list encoding.

\\textbf{Length bound:} Each $v_i \\in \\{1,\\dots,n\\}$ requires $O(\\log n)$ bits, and the list encoding of $n$ such numbers requires $|y| = O(n \\log n)$ bits (Definition on Input Lengths and Encodings). Since encoding a graph on $n$ vertices requires at least $|x| \\ge n$ bits, we have $|y| \\le p(|x|)$ for the polynomial $p(k) := k \\log k + k$.

\\textbf{Verifier:} Define $B$ to contain pairs $(x,y)$ where $x = \\langle G \\rangle$ with $G=(V,E)$, $|V|=n$, and $y = \\langle v_1,\\dots,v_n \\rangle$ decodes to a permutation of $\\{1,\\dots,n\\}$ forming a Hamiltonian cycle:
$$B := \\Big\\{ (x,y) \\;\\Big|\\; \\{v_1,\\dots,v_n\\} = \\{1,\\dots,n\\},$$
$$\\forall i \\in \\{1,\\dots,n-1\\}: \\{v_i,v_{i+1}\\} \\in E, \\;\\text{ and }\\; \\{v_n,v_1\\} \\in E \\Big\\}$$
Given $(x,y)$, we can check in polynomial time $O(n^2)$: (i) that $y$ decodes to a sequence of length $n$ that is a permutation of $\\{1,\\dots,n\\}$ (e.g.\\ sort the sequence and check it equals $(1,\\dots,n)$), and (ii) that each of the $n$ pairs of cyclically-consecutive vertices is an edge of $G$ (a single lookup in the adjacency matrix per pair, $O(1)$ each). Hence $B \\in \\text{P}$.

\\textbf{Equivalence:}
$$x \\in \\text{HC} \\iff G \\text{ has a Hamiltonian cycle}$$
$$\\iff \\exists \\text{ permutation } v_1,\\dots,v_n \\text{ of } V \\text{ with all cyclically-consecutive pairs in } E$$
$$\\iff \\exists y \\, (|y| \\le p(|x|) \\land (x,y) \\in B)$$
Since $B \\in \\text{P}$ and $|y| \\le p(|x|)$ for a polynomial $p$, by Definition 1.34, $\\text{HC} \\in \\text{NP}$.

\\textbf{Non-deterministic algorithm (Example 1.49 style):}
\\begin{lstlisting}[language=Python]
def HC(G):                        # G given e.g. as adjacency matrix, V = {1,...,n}
    n = number_of_vertices(G)
    # Part A: non-deterministically guess a candidate ordering v[1..n]
    v = n * [1]
    for i in range(0, n):
        for j in range(1, n+1):
            v[i] = v[i] | v[i] = j          # split into n parallel paths per position
    # Part B: verify v is a permutation and forms a Hamiltonian cycle
    if sorted(v) != list(range(1, n+1)):
        return 0
    for i in range(0, n-1):
        if not edge(G, v[i], v[i+1]):
            return 0
    if not edge(G, v[n-1], v[0]):
        return 0
    return 1
\\end{lstlisting}
\\textbf{Running time:} Part A performs $n$ non-deterministic choices among $n$ options each, taking $O(n^2)$ total (as in Example 1.49's Part A for BP). Part B checks the permutation property and the $n$ edges in $O(n^2)$. Hence every computation path runs in $O(n^2)$, a polynomial. By Theorem 1.47, this shows $\\text{HC} \\in \\text{NP}$.
\\end{solution}
\\end{parts}

%=============================================================================
% QUESTION 2
%=============================================================================
\\question[15] \\textbf{NP-Completeness: A Polynomial-Time Reduction for Vertex Cover}

Recall that a \\textbf{vertex cover} of an undirected graph $G = (V,E)$ is a set $C \\subseteq V$ such that every edge has at least one endpoint in $C$. Define $\\text{VC}$ to be the set of pairs $\\langle G,k \\rangle$ such that $G$ is an undirected graph with a vertex cover of size $\\le k$:
$$\\text{VC} := \\{\\langle G, k \\rangle \\mid G = (V,E), \\; G \\text{ has a vertex cover of size} \\le k\\}$$
You may use that $\\text{CLIQUE}$ is NP-complete without reproving it.

\\begin{parts}
\\part[4] Prove that $\\text{VC} \\in \\text{NP}$.

\\begin{solution}
A certificate is a set $C \\subseteq V$ with $|C| \\le k$, encoded as a list of vertex labels; its length is $O(|C| \\log |V|) \\le O(|V| \\log |V|)$, polynomial in $|\\langle G,k\\rangle|$. The certifier checks, for every edge $\\{u,v\\} \\in E$, whether $u \\in C$ or $v \\in C$; this takes polynomial time $O(|V| \\cdot |E|)$. Thus $\\text{VC} \\in \\text{NP}$.
\\end{solution}

\\part[4] Prove the following \\textbf{Key Lemma}: for an undirected graph $G = (V,E)$ and $S \\subseteq V$, $S$ is an independent set in $G$ (no edge of $E$ has both endpoints in $S$) if and only if $V \\setminus S$ is a vertex cover of $G$.

\\begin{solution}
($\\Rightarrow$) Suppose $S$ is independent. Let $\\{u,v\\} \\in E$. Since $S$ is independent, not both $u,v \\in S$, so at least one of $u,v$ lies in $V \\setminus S$. Hence $V \\setminus S$ covers every edge, i.e., it is a vertex cover.

($\\Leftarrow$) Suppose $V \\setminus S$ is a vertex cover. If $S$ were not independent, some edge $\\{u,v\\} \\in E$ would have both $u,v \\in S$, i.e., neither endpoint in $V \\setminus S$ --- contradicting that $V \\setminus S$ covers $\\{u,v\\}$. Hence $S$ is independent.
\\end{solution}

\\part[7] Using the Key Lemma (and noting that $S$ is independent in $G$ if and only if $S$ is a clique in the complement graph $\\overline{G} = (V,\\overline{E})$ with $\\overline{E} := \\{\\{u,v\\} \\mid u \\ne v, \\{u,v\\} \\notin E\\}$), prove that $\\text{VC}$ is NP-complete via a reduction $\\text{CLIQUE} \\le_p \\text{VC}$.

\\begin{solution}
\\textbf{Reduction:} Given a CLIQUE-instance $\\langle G,k \\rangle$ with $G=(V,E)$, $n=|V|$, define
$$f(\\langle G,k\\rangle) := \\langle \\overline{G}, \\, n-k \\rangle$$
where $\\overline{G}=(V,\\overline{E})$ is the complement graph. This is computable in polynomial time $O(n^2)$ (enumerate all $\\binom{n}{2}$ vertex pairs and flip edge/non-edge).

\\textbf{Proof of equivalence:} Let $\\langle G,k\\rangle$ be a CLIQUE-instance with $G=(V,E)$, $n=|V|$.
$$\\langle G,k\\rangle \\in \\text{CLIQUE} \\iff G \\text{ has a clique } S \\text{ of size } k$$
Since a clique in $G$ is, by definition, an independent set in the complement graph $\\overline{G}$:
$$\\iff S \\text{ is an independent set of size } k \\text{ in } \\overline{G}$$
By the Key Lemma, applied to $\\overline{G}$, $S$ is independent in $\\overline{G}$ iff $V \\setminus S$ is a vertex cover of $\\overline{G}$:
$$\\iff V \\setminus S \\text{ is a vertex cover of } \\overline{G} \\text{ of size } n-k$$
$$\\iff \\langle \\overline{G}, n-k \\rangle \\in \\text{VC} \\iff f(\\langle G,k\\rangle) \\in \\text{VC}$$
Thus $\\text{CLIQUE} \\le_p \\text{VC}$. Since $\\text{CLIQUE}$ is NP-hard and $f \\in \\text{FP}$, every $A \\in \\text{NP}$ satisfies $A \\le_p \\text{CLIQUE} \\le_p \\text{VC}$, so by transitivity of $\\le_p$ (Property 1.53.2), $A \\le_p \\text{VC}$; hence $\\text{VC}$ is NP-hard. Combined with part (a), $\\text{VC} \\in \\text{NP}$, so $\\text{VC}$ is NP-complete.
\\end{solution}
\\end{parts}

%=============================================================================
% QUESTION 3
%=============================================================================
\\question[15] \\textbf{Engineering Game AIs: Connect Four Bitboards (C Programming)}

Throughout this question, use the standard \\textbf{column-major} bitboard layout for Connect Four (6 rows, 7 columns): each column is padded with one extra sentinel bit, so column $c$ occupies bits $7c, 7c+1,\\dots,7c+6$ (bit $7c+r$ represents row $r$ of column $c$, for $r=0,\\dots,5$; bit $7c+6$ is the always-zero sentinel), giving $49$ used bits within the \\texttt{uint64\\_t}.

\\begin{parts}
\\part[6] Derive the shift value $S$ used to detect a 4-in-a-row along the \\textbf{main diagonal} (bottom-left to top-right, i.e., both the row index and the column index increase together along the line). Give the complete C/C++ code snippet for this check.

\\begin{solution}
Moving from one cell to its neighbor along the main diagonal (bottom-left to top-right) means moving one column to the right (column index $+1$) \\emph{and} one row up (row index $+1$).
In the column-major padded layout:
\\begin{itemize}
    \\item Moving one column to the right increases the bit index by $7$ (the padded column height).
    \\item Moving one row up increases the bit index by $1$.
\\end{itemize}
Thus, the net change in bit index for a main-diagonal step is $7+1=8$. A shift of $S=8$ aligns every cell with its bottom-left neighbor.

\\textbf{Code Snippet:}
\\begin{lstlisting}[language=C]
uint64_t d1 = board & (board >> 8);
if (d1 & (d1 >> 16)) return true;
\\end{lstlisting}
\\end{solution}

\\part[4] Explain why each column must be padded with at least one unused sentinel bit in this representation, referencing the wrap-around problem that would otherwise occur.

\\begin{solution}
Without padding, a column of exactly $6$ bits packed directly against the next column would place the top cell of column $c$ (bit index $6c+5$) immediately adjacent, in bit-index terms, to the bottom cell of column $c+1$ (bit index $6(c+1)=6c+6=(6c+5)+1$).

Consequently, a \\textbf{vertical} win-check of the form \\texttt{board \\& (board >> 1)} would incorrectly treat the top cell of column $c$ and the bottom cell of column $c+1$ as vertically adjacent, even though they belong to entirely different, non-adjacent columns --- a wrap-around error analogous to the one for horizontal shifts in row-major layouts, but here affecting vertical shifts in a tightly packed column-major layout.

By padding each column with one extra always-zero sentinel bit (column height $7$ instead of $6$), the top real cell of column $c$ (bit $7c+5$) is separated from the bottom real cell of column $c+1$ (bit $7(c+1)=7c+7$) by a gap of $2$ bit positions (the sentinel bit $7c+6$ lies in between). A shift by $1$ or $2$ can therefore never spuriously connect cells across a column boundary, since the intervening sentinel bit is always $0$ and breaks the chain of four consecutive set bits required for a false-positive win.
\\end{solution}

\\part[5] Write a C/C++ function \\texttt{uint64\\_t mirror(uint64\\_t board)} that computes the horizontal mirror image of a bitboard in this column-major representation (column $c$ swapped with column $6-c$), and briefly explain how maintaining a mirrored copy of the board incrementally (rather than recomputing \\texttt{mirror()} at every node) supports symmetry pruning at $O(1)$ cost per move.

\\begin{solution}
\\textbf{Implementation:} Each column occupies a contiguous block of $7$ bits, so mirroring moves the $7$-bit block of column $c$ to the position of column $6-c$ (column $3$ maps to itself):
\\begin{lstlisting}[language=C]
uint64_t mirror(uint64_t board) {
    uint64_t result = 0;
    for (int c = 0; c < 7; c++) {
        uint64_t column_bits = (board >> (7 * c)) & 0x7F; // 7 bits
        result |= column_bits << (7 * (6 - c));            // place at mirrored column
    }
    return result;
}
\\end{lstlisting}

\\textbf{Incremental maintenance:} Rather than recomputing \\texttt{mirror(board)} in full at every search node, we maintain a second pair of bitboards (\\texttt{board\\_mirrored}, \\texttt{opponent\\_mirrored}) alongside the real ones. When a move is made in column $c$ at row $r$ (setting bit $7c+r$), the mirrored move is simply setting bit $7(6-c)+r$ in the mirrored board --- one shift and one OR, with no loop and no recomputation of the rest of the board. The same applies symmetrically to \\texttt{undo\\_move}. This keeps the incremental cost at $O(1)$ per move, after which a symmetry check (is the position equal to its own mirror?) is just two 64-bit integer comparisons, e.g.\\ to restrict the root search to columns $0,1,2,3$ only.
\\end{solution}
\\end{parts}

%=============================================================================
% QUESTION 4
%=============================================================================
\\question[15] \\textbf{Engineering Game AIs: Alpha-Beta Pruning --- Trace and Proof}

\\begin{parts}
\\part[8] Consider the following depth-3 game tree with branching factor $2$: the root is a \\textbf{Max} node, its two children are \\textbf{Min} nodes, their children are \\textbf{Max} nodes, and the leaves (static evaluation values) are as shown below.

\\begin{center}
\\begin{tikzpicture}[level distance=1.6cm,
    level 1/.style={sibling distance=4.4cm},
    level 2/.style={sibling distance=2.2cm},
    level 3/.style={sibling distance=1.1cm},
    every node/.style={draw,circle,minimum size=0.75cm,inner sep=0pt,font=\\small}]
\\node {Max}
  child { node {Min}
    child { node {Max}
      child { node {3} }
      child { node {5} }
    }
    child { node {Max}
      child { node {6} }
      child { node {9} }
    }
  }
  child { node {Min}
    child { node {Max}
      child { node {1} }
      child { node {2} }
    }
    child { node {Max}
      child { node {0} }
      child { node {$-1$} }
    }
  };
\\end{tikzpicture}
\\end{center}

Trace the execution of Alpha-Beta pruning, exploring children strictly left-to-right, showing the $\\alpha/\\beta$ values maintained at each internal node and identifying every leaf that is \\textbf{pruned} (never evaluated). State the final value returned at the root.

\\begin{solution}
We label the nodes $L$ (left Min), $LL,LR$ (its Max children), $R$ (right Min), $RL,RR$ (its Max children). The leaves are:
$$LLL{=}3,\\ LLR{=}5,\\ LRL{=}6,\\ LRR{=}9$$
$$RLL{=}1,\\ RLR{=}2,\\ RRL{=}0,\\ RRR{=}{-1}$$

\\textbf{At Root (Max), $[\\alpha{=}{-\\infty},\\beta{=}{+\\infty}]$:} explore $L$ with window $[-\\infty,+\\infty]$.
\\begin{itemize}
\\item \\textbf{At $L$ (Min), $[-\\infty,+\\infty]$:} explore $LL$ with window $[-\\infty,+\\infty]$.
    \\begin{itemize}
    \\item \\textbf{At $LL$ (Max):} evaluate $LLL{=}3$ ($\\alpha{=}3$); evaluate $LLR{=}5$ ($\\alpha{=}5$); no cutoff. $LL$ returns $5$.
    \\end{itemize}
    Back at $L$: best $=5$, so $\\beta = 5$. Since $\\alpha(-\\infty) < \\beta(5)$, no cutoff; explore $LR$ with window $[-\\infty, 5]$.
    \\begin{itemize}
    \\item \\textbf{At $LR$ (Max), $[-\\infty,5]$:} evaluate $LRL{=}6$: local best $=6 \\ge \\beta(5)$ $\\implies$ \\textbf{cutoff}. \\textbf{$LRR=9$ is pruned (never evaluated).} $LR$ returns $6$.
    \\end{itemize}
    Back at $L$: candidate from $LR$ is $6$; best $=\\min(5,6)=5$ (unchanged). $L$ returns $\\mathbf{5}$ (exact, since $-\\infty < 5 < +\\infty$).
\\end{itemize}
Back at Root: best $=5$, so $\\alpha = 5$. Explore $R$ with window $[5,+\\infty]$.
\\begin{itemize}
\\item \\textbf{At $R$ (Min), $[5,+\\infty]$:} explore $RL$ with window $[5,+\\infty]$.
    \\begin{itemize}
    \\item \\textbf{At $RL$ (Max), $[5,+\\infty]$:} evaluate $RLL{=}1$ (best$=1$, local $\\alpha$ stays $5$, since $1<5$); evaluate $RLR{=}2$ (best$=2$, still $<5$); no cutoff (best never reaches $+\\infty$). $RL$ returns $2$.
    \\end{itemize}
    Back at $R$: candidate $=2$, so $\\beta=\\min(+\\infty,2)=2$. Since $\\alpha(5) \\ge \\beta(2)$ $\\implies$ \\textbf{cutoff}. \\textbf{$RR$'s entire subtree ($RRL=0$, $RRR=-1$) is pruned (never evaluated).} $R$ returns $2$ (a Fail-Low bound: the true value of $R$ is $\\le 2$, but since $2 < \\alpha = 5$ this cannot change the root's decision).
\\end{itemize}
Back at Root: candidate from $R$ is $2 \\le 5$, so best remains $\\max(5,2)=5$.

\\textbf{Final value returned at the root: $\\mathbf{5}$.}
\\textbf{Leaves pruned:} $LRR=9$, $RRL=0$, $RRR=-1$ (three of the eight leaves are never evaluated). This matches the value $5$ obtained by a full (unpruned) minimax evaluation of the tree, confirming that Alpha-Beta pruning never changes the result, only the amount of work needed to obtain it.
\\end{solution}

\\part[7] Recall that \\texttt{negamax(N, depth, alpha, beta)} returns a value $v$, and that the following two properties are already established:
\\begin{enumerate}
    \\item \\textbf{Fail-Low:} If $v \\le \\alpha$, then $S(N) \\le v$.
    \\item \\textbf{Exact-Value:} If $\\alpha < v < \\beta$, then $S(N) = v$.
\\end{enumerate}
Prove the remaining \\textbf{Fail-High} property: if $v \\ge \\beta$, then $S(N) \\ge v$.

\\begin{solution}
We prove this by induction on the depth of the search, using the Fail-Low property (already established) applied to a child.

\\textbf{Base Case (depth $=0$):} $N$ is a leaf, and negamax returns $v = S(N)$. If $v \\ge \\beta$, trivially $S(N) = v \\ge v$.

\\textbf{Inductive Step:} Assume Fail-Low, Exact-Value, and Fail-High hold for all calls at depth $d-1$. Let $N$ have depth $d$ with children $C_1,\\dots,C_k$, and negamax calls $v_i = -\\texttt{negamax}(C_i, d-1, -\\beta, -\\alpha_i)$, where $\\alpha_i$ is the running best score ($\\alpha_1=\\alpha$; $\\alpha_i = \\max(\\alpha,v_1,\\dots,v_{i-1})$ for $i>1$), so that $S(N)=\\max_i(-S(C_i))$.

Suppose negamax returns $v \\ge \\beta$. This happens exactly when some child $C_j$'s recursive call, made with window $(-\\beta,-\\alpha_j)$, returns $v_j$ with $-v_j \\ge \\beta$ (i.e.\\ $v_j \\le -\\beta$), triggering an immediate cutoff so that negamax returns $v=-v_j\\ge\\beta$ without examining $C_{j+1},\\dots,C_k$.

Since $-\\beta$ is precisely the alpha-bound of that child's call, and $v_j \\le -\\beta$, the induction hypothesis (Fail-Low, applied to $C_j$'s call with its alpha-bound $-\\beta$) gives:
$$S(C_j) \\le v_j$$
Negating: $-S(C_j) \\ge -v_j = v$. Since $S(N)=\\max_i(-S(C_i)) \\ge -S(C_j)$, we conclude:
$$S(N) \\ge -S(C_j) \\ge v$$
This proves $S(N) \\ge v$, completing the induction.
\\end{solution}
\\end{parts}

%=============================================================================
% QUESTION 5
%=============================================================================
\\question[15] \\textbf{Engineering Game AIs: Comparing Search Algorithms}

\\begin{parts}
\\part[6] Complete the following comparison table for uninformed and informed search algorithms on a search tree/graph with branching factor $b$, solution depth $d$, maximum depth $m$ (possibly infinite), and (where relevant) positive edge costs with minimum edge cost $\\varepsilon$ and optimal solution cost $C^*$. State, for each algorithm: (i) \\textbf{Completeness} (does it always find a solution if one exists?), (ii) \\textbf{Optimality} (does it always find a least-cost solution, and under what condition?), (iii) \\textbf{Time complexity}, (iv) \\textbf{Space complexity}.
Consider: DFS, BFS, Dijkstra (Uniform-Cost Search), $A^*$, Iterative Deepening Search (IDS), and IDA$^*$.

\\begin{solution}
\\begin{center}
\\renewcommand{\\arraystretch}{1.3}
\\footnotesize
\\setlength{\\tabcolsep}{3pt}
\\begin{tabular}{|p{1.5cm}|p{2.4cm}|p{2.9cm}|p{2.5cm}|p{2.2cm}|}
\\hline
\\textbf{Algorithm} & \\textbf{Complete?} & \\textbf{Optimal?} & \\textbf{Time} & \\textbf{Space} \\\\
\\hline
DFS & No (infinite $m$, cycles) & No & $O(b^m)$ & $O(bm)$ \\\\
\\hline
BFS & Yes (if $b$ finite) & Only if unweighted & $O(b^d)$ & $O(b^d)$ \\\\
\\hline
Dijkstra (UCS) & Yes (costs $\\ge \\varepsilon>0$) & Yes (any non-neg.\\ weights) & $O(b^{1+C^*/\\varepsilon})$ & same as Time \\\\
\\hline
$A^*$ & Yes ($b$ finite, costs $\\ge \\varepsilon$) & Yes, if $h$ admissible (consistent for graphs) & $O(b^d)$ worst case, less with good $h$ & $O(b^d)$ (all nodes kept) \\\\
\\hline
IDS & Yes (if $b$ finite) & Only if unweighted & $O(b^d)$ (same as BFS) & $O(bd)$ \\\\
\\hline
IDA$^*$ & Yes (as $A^*$) & Yes, if $h$ admissible & comparable to $A^*$ & $O(bd)$ \\\\
\\hline
\\end{tabular}
\\end{center}
\\end{solution}

\\part[5] Explain why $A^*$ graph search is optimal whenever the heuristic $h$ is admissible (i.e., $h(n) \\le h^*(n)$, the true cheapest cost from $n$ to a goal, for every node $n$). Sketch the proof idea.

\\begin{solution}
Suppose, for contradiction, that $A^*$ terminates by selecting a suboptimal goal node $G_2$ with $g(G_2) > C^*$ (the true optimal solution cost), while an optimal solution path passes through some node $n$ still in the frontier (not yet expanded) at that time.

Since $h$ is admissible, $h(n) \\le h^*(n)$, so:
$$f(n) = g(n) + h(n) \\le g(n) + h^*(n) = C^*$$
(the last equality holds because $n$ lies on an optimal path, so $g(n) + h^*(n)$ equals the optimal cost $C^*$ exactly).

Since $G_2$ is a goal node, $h(G_2)=0$, so $f(G_2) = g(G_2) > C^*$.

Combining: $f(n) \\le C^* < f(G_2)$. But $A^*$ always expands the frontier node with the smallest $f$-value next; since $n$ was still in the frontier with a strictly smaller $f$-value than $G_2$, $A^*$ would have expanded (and eventually selected) $n$'s path before ever selecting $G_2$ as the returned solution --- contradicting the assumption that $A^*$ terminates by returning $G_2$.

Hence $A^*$ cannot terminate with a suboptimal goal: it must return a solution of cost exactly $C^*$. (For graph search with repeated-state pruning, admissibility must be strengthened to \\textbf{consistency}, $h(n) \\le c(n,n') + h(n')$ for every edge $(n,n')$, so that the first time a node is expanded, its $g$-value is already optimal; otherwise a node might be pruned as ``already visited'' before its optimal cost is discovered.)
\\end{solution}

\\part[4] Explain why IDA$^*$ requires only $O(d)$ (or $O(bd)$) space, in contrast to $A^*$'s $O(b^d)$, and why this comes at the cost of re-expanding nodes across iterations.

\\begin{solution}
IDA$^*$ performs a sequence of depth-first searches, each bounded by an increasing $f$-cost threshold (starting at $h(\\text{start})$, and increasing on each iteration to the smallest $f$-value that exceeded the previous threshold). Because each iteration is literally a depth-first search, it only ever needs to keep the current path from the root to the current node in memory (plus the siblings awaiting exploration along that path), not the entire set of previously generated nodes. This gives space complexity $O(d)$ (path only) or $O(bd)$ (path plus siblings), identical to plain DFS/IDS, and exponentially better than $A^*$'s $O(b^d)$, which must retain every generated node in its frontier/explored set to avoid re-expansion.

The trade-off is that nodes explored in earlier iterations (with a smaller threshold) are entirely forgotten once that iteration ends, and must be regenerated from scratch in later iterations. However, since the number of nodes at depth $d$ grows geometrically in $b$, the total work of all shallower, repeated iterations is dominated by (within a constant factor of) the cost of the final iteration alone --- so IDA$^*$'s asymptotic time complexity remains comparable to a single $A^*$ search, while using drastically less memory.
\\end{solution}
\\end{parts}

%=============================================================================
% QUESTION 6
%=============================================================================
\\question[25] \\textbf{Algorithmic Number Theory and Cryptography}

\\begin{parts}
\\part[6] \\textbf{Extended Euclidean Algorithm.} Execute the Extended Euclidean Algorithm on $a=252$, $b=198$: show every step of the Euclidean algorithm (quotients and remainders), and then back-substitute to express $\\gcd(a,b)$ as an integer linear combination $x \\cdot a + y \\cdot b$.

\\begin{solution}
\\textbf{Euclidean Algorithm (forward pass):}
\\begin{align*}
252 &= 1 \\cdot 198 + 54 \\\\
198 &= 3 \\cdot 54 + 36 \\\\
54 &= 1 \\cdot 36 + 18 \\\\
36 &= 2 \\cdot 18 + 0
\\end{align*}
The last non-zero remainder is $18$, so $\\gcd(252,198) = 18$.

\\textbf{Back-substitution:}
\\begin{align*}
18 &= 54 - 1 \\cdot 36 \\\\
&= 54 - 1 \\cdot (198 - 3 \\cdot 54) = 4 \\cdot 54 - 1 \\cdot 198 \\\\
&= 4 \\cdot (252 - 1 \\cdot 198) - 1 \\cdot 198 = 4 \\cdot 252 - 5 \\cdot 198
\\end{align*}
\\textbf{Check:} $4 \\cdot 252 - 5 \\cdot 198 = 1008 - 990 = 18$. \\checkmark

Thus $\\gcd(252,198) = 18 = 4 \\cdot 252 + (-5) \\cdot 198$, i.e., $x=4$, $y=-5$.
\\end{solution}

\\part[6] \\textbf{Square and Multiply.} Compute $11^{53} \\bmod 17$ using the Square-and-Multiply method. Show the binary representation of the exponent and every intermediate value.

\\begin{solution}
\\textbf{Binary representation:} $\\text{bin}(53) = 110101$ (since $53 = 32+16+4+1$).

Using Horner's method on the exponent (processing bits left-to-right, starting from the leading $1$), we simultaneously track the exponent built so far and the corresponding power of $11$ modulo $17$. Starting value (leading bit $1$): result $= 11^1 \\bmod 17 = 11$.

For each subsequent bit $e_i$: square the result, and additionally multiply by $11$ if $e_i = 1$.

\\begin{center}
\\renewcommand{\\arraystretch}{1.3}
\\small
\\begin{tabular}{|p{1.6cm}|p{2.3cm}|p{6.3cm}|p{1.3cm}|}
\\hline
\\textbf{Bit} & \\textbf{Exponent so far} & \\textbf{Operation} & \\textbf{Result mod 17} \\\\
\\hline
(leading) $1$ & $1$ & --- & $11$ \\\\
\\hline
$1$ & $3$ & $11^2 \\bmod 17 = 2$; then $2 \\cdot 11 \\bmod 17 = 5$ & $5$ \\\\
\\hline
$0$ & $6$ & $5^2 \\bmod 17 = 8$ & $8$ \\\\
\\hline
$1$ & $13$ & $8^2 \\bmod 17 = 13$; then $13 \\cdot 11 \\bmod 17 = 7$ & $7$ \\\\
\\hline
$0$ & $26$ & $7^2 \\bmod 17 = 15$ & $15$ \\\\
\\hline
$1$ & $53$ & $15^2 \\bmod 17 = 4$; then $4 \\cdot 11 \\bmod 17 = 10$ & $10$ \\\\
\\hline
\\end{tabular}
\\end{center}

\\textbf{Result:} $11^{53} \\bmod 17 = 10$.

\\textbf{Check (via Fermat's Little Theorem):} since $17$ is prime, $11^{16} \\equiv 1 \\pmod{17}$, so $11^{53} \\equiv 11^{53 \\bmod 16} = 11^{5} \\pmod{17}$. We have $11^2 \\equiv 2$, $11^4 \\equiv 4$, $11^5 \\equiv 4 \\cdot 11 = 44 \\equiv 10 \\pmod{17}$. \\checkmark
\\end{solution}

\\part[5] \\textbf{Euler's Totient Function.} Compute $\\varphi(315)$.

\\begin{solution}
Factor $315 = 3^2 \\cdot 5 \\cdot 7$ (since $315 = 9 \\cdot 35 = 9 \\cdot 5 \\cdot 7$).

Since $3,5,7$ are pairwise distinct primes, $3^2$, $5$, and $7$ are pairwise coprime, so by the multiplicativity of $\\varphi$ (Theorem 3.20.1):
$$\\varphi(315) = \\varphi(3^2) \\cdot \\varphi(5) \\cdot \\varphi(7)$$
Using the prime-power formula $\\varphi(p^k) = p^k - p^{k-1}$ (Theorem 3.20.2):
$$\\varphi(3^2) = 3^2 - 3^1 = 9 - 3 = 6, \\qquad \\varphi(5) = 5-1 = 4, \\qquad \\varphi(7) = 7-1=6$$
Therefore:
$$\\varphi(315) = 6 \\cdot 4 \\cdot 6 = 144$$
\\end{solution}

\\part[8] \\textbf{Security of RSA: Prove or Refute.} For each statement, decide whether it is true, false, or not known/proven, with brief justification.
\\begin{subparts}
    \\subpart[2] If integer factorization can be solved in polynomial time, then RSA can be broken in polynomial time.
    \\subpart[2] If RSA can be broken in polynomial time, then integer factorization can be solved in polynomial time.
    \\subpart[2] Textbook (deterministic, unpadded) RSA encryption is semantically secure, since without the private key an attacker cannot invert $c = m^e \\bmod n$.
    \\subpart[2] A large-scale quantum computer could break RSA in polynomial time.
\\end{subparts}

\\begin{solution}
\\begin{subparts}
    \\subpart \\textbf{True.} This is Theorem 3.32: given the factorization $n=pq$, an attacker computes $\\varphi(n)=(p-1)(q-1)$ and then the private key $d = e^{-1} \\bmod \\varphi(n)$ via the Extended Euclidean Algorithm, all in polynomial time.

    \\subpart \\textbf{Not known / open.} This is the converse of Theorem 3.32. It is not known whether breaking RSA implies the ability to factor $n$ in polynomial time; the lecture explicitly states this converse is unproven, and it is conjectured that breaking RSA might not be equivalent to factoring.

    \\subpart \\textbf{False.} Textbook RSA is \\emph{deterministic}: identical plaintexts always produce identical ciphertexts. Thus, if an attacker knows the plaintext is drawn from a small known set (e.g., a ``yes''/``no'' answer), they can simply re-encrypt every candidate message with the public key and compare each resulting ciphertext to the intercepted one, recovering $m$ without ever inverting the encryption function. Hence textbook RSA does not achieve semantic security.

    \\subpart \\textbf{True.} Shor's algorithm factors integers in polynomial time on a quantum computer; by Theorem 3.32, this allows an attacker to recover the private key and break RSA in polynomial time.
\\end{subparts}
\\end{solution}
\\end{parts}
\\end{questions}
\\end{document}
"""

def compile_pdf(with_solutions, output_name):
    # Prepare the LaTeX code
    switch = "\\printanswers" if with_solutions else "% \\printanswers"
    code = latex_code_template.replace("% SOLUTION_SWITCH_PLACEHOLDER", switch)

    tex_path = os.path.join(mockexam_dir, f"{output_name}.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"Compiling {output_name}.pdf...")
    # Run pdflatex three times to resolve the exam class's gradetable
    for _ in range(3):
        res = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", f"{output_name}.tex"],
            cwd=mockexam_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if res.returncode != 0:
            print(f"Error compiling {output_name}:")
            print(res.stdout)
            print(res.stderr)
            return False

    # Clean up auxiliary files
    exts = [".aux", ".log", ".out"]
    for ext in exts:
        aux_file = os.path.join(mockexam_dir, f"{output_name}{ext}")
        if os.path.exists(aux_file):
            os.remove(aux_file)

    print(f"Successfully generated {output_name}.pdf")
    return True

# Compile both sheets
compile_pdf(with_solutions=False, output_name="mockexam")
compile_pdf(with_solutions=True, output_name="mockexam_solutions")
