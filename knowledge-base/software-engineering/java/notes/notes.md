Java Architecture & Advanced Development Notes
Deep technical notes containing JVM execution, Memory spaces, Multi-threading, and Collections
Module 1: JVM Mechanics & Platform Independence
Platform independence in Java is achieved via compilation of source code (.java) to bytecode (.class) which runs on the Java Virtual Machine (JVM). The JVM acts as a virtual runtime environment that abstracts hardware architectures.
1.1 compilation & Execution Flow
* javac Compiler: Transpiles human-readable Java code to stack-based intermediate bytecode instructions.
* JVM Execution Engine: Contains Class Loader, Bytecode Verifier (secures runtime against buffer overflows), Interpreter, and JIT Compiler.
* JIT (Just-In-Time) Compiler: Profiles running code. Identifies 'Hot Spots' (frequently executed methods) and compiles them directly into native machine instructions to skip interpreter overhead.
1.2 JVM Memory Architecture

|Memory Area|Access Scope|Content Stored|Lifecycle Scope|
|---|---|---|---|
|Heap Memory|All Threads Shared|Objects and Instance Variables, String Constant Pool|JVM Shutdown / GC|
|Stack Memory|Thread Private|Method Stack Frames, Local variables, Primitive variables|Method execution exit|
|Method Area (Metaspace)|All Threads Shared|Class schemas, method structures, static fields|Class unloading / JVM close|
|PC Register|Thread Private|Instruction pointer addresses of next execution bytecode|Thread termination|

Module 2: Advanced OOP, Generics & Collections
Collections and OOP relationships are highly interview-tested. Specifically, memory structures under HashMap collisions and Java Generics PECS rule.
2.1 Generics: Producer Extends Consumer Super (PECS)
* ? extends T (Upper Bound): Represents a Producer. You can read elements from it, but cannot add elements because the exact subclass subtype is unknown.
* ? super T (Lower Bound): Represents a Consumer. You can add elements of type T or its subclasses to it, but you can only read objects of type Object.
2.2 HashMap Collision Mechanics
When two different keys generate the same hash index, they are stored in the same bucket:
* Java 7: Stored as a singly linked list. Worst case search complexity is O(N).
* Java 8+: Stored as a linked list initially. Once a bucket exceeds TREEIFY_THRESHOLD (8 nodes) AND total table capacity >= 64, the bucket is transformed (treeified) into a Red-Black Tree. Search complexity improves to O(log N).

|⚠️ INTERVIEW TRAP: HashMap Keys Immutability If you use a mutable object as a HashMap key, and change its state after insertion, the hashCode() changes. The key cannot be retrieved because it hashes to a different bucket! Always use immutable types like String or Integer as keys.|
|---|

Module 3: Exception Handling & Serialization
3.1 Try-with-resources Mechanics
Any class implementing AutoCloseable can be declared within the try resource block. The compiler automatically inserts a finally block containing close() executions, eliminating memory/socket leaks.

|try (BufferedReader br = new BufferedReader(new FileReader("data.txt"))) {     System.out.println(br.readLine()); } // close() runs automatically even if exceptions occur!|
|---|

Module 4: Functional Interfaces & Streams API
Streams process pipeline items lazily. Intermediate operations (filter, map) return another Stream and are not executed until a terminal operation (collect, count) is invoked.
Module 5: Concurrency & Garbage Collection
5.1 GC Algorithms: G1GC vs ZGC
G1GC splits Heap into equal-sized regions, targeting user-specified pause times. ZGC is a concurrent, low-latency garbage collector using colored pointers and load barriers, keeping pause times under 10ms regardless of heap sizes (up to Terabytes).