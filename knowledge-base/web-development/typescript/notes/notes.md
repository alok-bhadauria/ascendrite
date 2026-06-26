TypeScript Advanced Architecture Notes
Detailed notes on structural typing, type narrowing, generics, and React integration
Module 1: Structural Typing & Shape validation
TypeScript uses a structural type system (Duck Typing) to compare types. Two objects are type-compatible if they have the same shape, even if declared under different interfaces/classes.
1.1 Types vs Interfaces

|Feature|Interfaces|Types|
|---|---|---|
|Declaration Merging|Supported (multiple declarations merge automatically)|Not supported (causes duplicate identifier error)|
|Extensibility|Extends via 'extends' keyword|Combines via Intersection operators '&'|
|Union/Prims types|Cannot define primitive or union types directly|Can define union, tuple, mapped types directly|
|Performance|Slightly faster compiler lookup indices|Slower in massive recursive combinations|

Module 2: Type Narrowing & Guards
Narrowing changes the broad type of a variable to a more specific type within a code block.
* typeof: Basic checks for primitive types (string, number, boolean, symbol, undefined).
* instanceof: Class-instance checks (checks the prototype chain).
* User-Defined Type Guards: Uses the 'parameter is Type' predicate syntax to return boolean states.

|function isUser(actor: User | Admin): actor is User {     return (actor as User).username !== undefined; }|
|---|

Module 3: Generics & Utility Types
Generics enable code reusability while retaining compile-time type checks.

|interface ApiResponse<T> {     data: T;     status: number; }|
|---|
