TypeScript Interview Prep & Traps Guide
Q1: Explain structural typing loopholes in TypeScript.
Because TypeScript types are checked structurally, an object containing excess properties can be assigned to a variable with a simpler shape, but only if passed as a reference. Inline object declarations trigger Excess Property Checking, raising errors.

|interface User { name: string; } const person = { name: 'Alice', age: 30 }; const user: User = person; // PASSES because shape has 'name' const inline: User = { name: 'Alice', age: 30 }; // FAILS! (excess property checking)|
|---|


|⚠️ INTERVIEW TRAP: Overusing the 'any' type Using 'any' turns off TypeScript. Interviewer will inspect if you type responses from APIs. Always use 'unknown' paired with a custom type-guard or Zod validation library schemas to keep code-bases secure.|
|---|
