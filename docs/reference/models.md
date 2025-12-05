# Data Models

This page contains all the data models used in the API.

## CreateThisIsAnDemoInput

**Schema:**
```json
{
  "title": string (required)  // Issue title
  "current_behavior": string (required)  // Current Behavior: A concise description of what you're experiencing.
  "expected_behavior": string (required)  // Expected Behavior: A concise description of what you expected to happen.
  "steps_to_reproduce": string (required)  // Steps To Reproduce

Example:
steps to reproduce the behavior:
1. In this environment...
1. With this config...
1. Run '...'
1. See error...
  "environment": string (required)  // Environment

Example:
- OS: Ubuntu 20.04
- Node: 13.14.0
- npm: 7.6.3
  "anything_else": string (required)  // Anything else: Links? References? Anything that will give us more context about the issue that you are encountering!
}
```

**Properties:**

- **title** *(required)*: `string`
  - Description: Issue title

- **current_behavior** *(required)*: `string`
  - Description: Current Behavior: A concise description of what you're experiencing.

- **expected_behavior** *(required)*: `string`
  - Description: Expected Behavior: A concise description of what you expected to happen.

- **steps_to_reproduce** *(required)*: `string`
  - Description: Steps To Reproduce

Example:
steps to reproduce the behavior:
1. In this environment...
1. With this config...
1. Run '...'
1. See error...

- **environment** *(required)*: `string`
  - Description: Environment

Example:
- OS: Ubuntu 20.04
- Node: 13.14.0
- npm: 7.6.3

- **anything_else** *(required)*: `string`
  - Description: Anything else: Links? References? Anything that will give us more context about the issue that you are encountering!

---

## HTTPValidationError

**Schema:**
```json
{
  "detail": [ValidationError]  // 
}
```

**Properties:**

- **detail**: `[ValidationError]`

---

## ValidationError

**Schema:**
```json
{
  "loc": [unknown] (required)  // 
  "msg": string (required)  // 
  "type": string (required)  // 
}
```

**Properties:**

- **loc** *(required)*: `[unknown]`

- **msg** *(required)*: `string`

- **type** *(required)*: `string`

---
