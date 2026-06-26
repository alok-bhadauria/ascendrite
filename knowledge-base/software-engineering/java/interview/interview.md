Java Interview Prep & Traps Guide
Q1: Explain String Immutability and its Heap implications.
String immutability prevents thread-safety problems, allows key-hashing security in maps, and enables the String Constant Pool (SCP) caching. If strings were mutable, changing a string variable would corrupt references in other variables or hash indices.

|⚠️ INTERVIEW TRAP: String Concatenation in Loops Interviewer will ask you to optimize a string concatenation loop. Using '+' creates a new StringBuilder object in every iteration. Refactor to use a single StringBuilder instance initialized before the loop to reduce memory allocations.|
|---|

Q2: Difference between checked and unchecked exceptions?
Checked exceptions (e.g. IOException) extend Exception and are verified at compile time. Unchecked exceptions (e.g. NullPointerException) extend RuntimeException and occur at runtime. Never suppress checked exceptions using empty catch blocks.
Q3: Explain the Happens-Before relationship in JMM.
It defines visibility rules for multi-threaded access. For example: A write to a volatile field happens-before every subsequent read of that same volatile field. A thread start() call happens-before any actions in the started thread.