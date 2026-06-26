TypeScript Revision Cheat Sheet
Core Type System Summary
* any vs unknown: 'any' disables type checks; 'unknown' requires type narrowing/casting before operations.
* never: Represents values that never occur, such as a function returning an infinite loop or throw exception, and exhaustive checks.
* ReadOnly: Prevents mutating properties at compile-time.
Common Utility Signatures
* Partial<T>: Makes all object keys optional.
* Omit<T, K>: Removes keys K from object type T.
* Record<K, V>: Creates map signatures with keys K and values V.