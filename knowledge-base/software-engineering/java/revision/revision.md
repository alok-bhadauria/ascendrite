Java revision Quick Cheat Sheet
Core JVM Revision Checklist
* JIT vs Interpreter: Interpreter reads line-by-line; JIT compiles hot methods to native code.
* Metaspace: Moved out of JVM Heap in Java 8 into native OS memory to avoid PermGen OutOfMemoryError.
* String Constant Pool: Stored in Heap. String literal creations are cached to save memory.
Advanced OOP & Collections Revision
* Comparable vs Comparator: Comparable defines natural ordering (compareTo); Comparator defines custom sort orders (compare).
* PECS: Producer Extends (read-only), Consumer Super (write-only).
* HashMap: Java 8 converts linked list to Red-Black Tree when nodes > 8 and capacity >= 64.
Concurrency Revision
* Volatile Keyword: Guarantees memory visibility (bypasses CPU registers, reads/writes directly to main memory), but does not guarantee atomicity.
* Happens-Before Relationship: Java memory model rule guaranteeing one write action is visible to another read action.