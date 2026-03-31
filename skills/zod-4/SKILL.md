---
name: zod-4
description: >
  Zod 4 schema validation patterns, parsing, and type inference.
  Trigger: When using Zod for validation - schema creation, parsing.
license: Apache-2.0
metadata:
  author: NickEsColR
  version: "1.0"
---

## When to Use

- Creating or modifying Zod schemas for validation
- Validating API request/response data
- Defining TypeScript types inferred from Zod schemas
- Handling parsing errors and custom error messages

## Critical Patterns

### Pattern 1: Use top-level validators

Common validators like `z.email()`, `z.uuid()`, and `z.url()` are top-level functions in Zod 4. Prefer them over `z.string().email()`.

### Pattern 2: Use `error` param for custom messages

The `error` parameter replaces `message` for custom error messages. It also accepts a function for dynamic errors.

### Pattern 3: Prefer `safeParse` over `parse` in application code

Use `parse` only when you want exceptions to bubble up. In most application code, `safeParse` gives you a clean `{ success, data/error }` result to handle explicitly.

### Pattern 4: Infer types from schemas

Always use `z.infer<typeof schema>` instead of manually defining matching interfaces. The schema is the single source of truth.

### Pattern 5: Use discriminated unions for polymorphic data

When objects share a common discriminant field (like `status` or `type`), use `z.discriminatedUnion()` for more efficient parsing and better TypeScript narrowing.

### Pattern 6: Coerce input types

Use `z.coerce` for form inputs and query params that arrive as strings but should be numbers or dates. Don't manually parse — let Zod handle it.

## Code Examples

### Example 1: Basic schemas with Zod 4 syntax

```ts
import { z } from "zod";

// ✅ Zod 4 top-level validators
const emailSchema = z.email({ error: "Invalid email address" });
const uuidSchema = z.uuid();
const urlSchema = z.url();

// Primitives with constraints
const nameSchema = z.string().min(1).max(100);
const ageSchema = z.number().int().positive().max(150);
const priceSchema = z.number().min(0).multipleOf(0.01);
```

### Example 2: Object schema with inferred type

```ts
import { z } from "zod";

const userSchema = z.object({
  id: z.uuid(),
  email: z.email({ error: "Invalid email address" }),
  name: z.string().min(1, { error: "Name is required" }),
  age: z.number().int().positive().optional(),
  role: z.enum(["admin", "user", "guest"]),
  metadata: z.record(z.string(), z.unknown()).optional(),
});

type User = z.infer<typeof userSchema>;

// Parsing
const result = userSchema.safeParse(data);
if (result.success) {
  console.log(result.data); // User type
} else {
  console.log(result.error.issues);
}
```

### Example 3: Discriminated union

```ts
import { z } from "zod";

const resultSchema = z.discriminatedUnion("status", [
  z.object({ status: z.literal("success"), data: z.unknown() }),
  z.object({ status: z.literal("error"), error: z.string() }),
]);

// TypeScript narrows based on status
const result = resultSchema.parse(data);
if (result.status === "success") {
  console.log(result.data);
} else {
  console.log(result.error);
}
```

### Example 4: Coercion and transforms

```ts
import { z } from "zod";

// Coerce from form/query string inputs
const pageNumber = z.coerce.number().int().positive().default(1);
const dateParam = z.coerce.date();

// Transform during parsing
const lowercaseEmail = z.email().transform(email => email.toLowerCase());
const trimmedString = z.preprocess(
  val => (typeof val === "string" ? val.trim() : val),
  z.string()
);
```

### Example 5: Refinements and custom validation

```ts
import { z } from "zod";

const passwordSchema = z
  .string()
  .min(8)
  .refine((val) => /[A-Z]/.test(val), {
    message: "Must contain uppercase letter",
  })
  .refine((val) => /[0-9]/.test(val), {
    message: "Must contain number",
  });

// superRefine for cross-field validation
const formSchema = z
  .object({
    password: z.string(),
    confirmPassword: z.string(),
  })
  .superRefine((data, ctx) => {
    if (data.password !== data.confirmPassword) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "Passwords don't match",
        path: ["confirmPassword"],
      });
    }
  });
```

## Commands

```bash
cd web
pnpm add zod
```

## Resources

- **Skills**: See [tailwind-4](../tailwind-4/SKILL.md) for styling patterns in web components
- **Skills**: See [preact-ui](../preact-ui/SKILL.md) for Preact form component patterns
