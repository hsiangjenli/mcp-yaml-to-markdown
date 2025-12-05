# API Endpoints
Version: 0.1.0
A template for creating MCP-compliant FastAPI

## /create_this_is_an_demo

### POST

**Summary:** 🤖 This is an demo

**Description:** A demo markdown template

**Request Body:**

Content-Type: `application/json`

Schema:
[CreateThisIsAnDemoInput](models.md#createthisisandemoinput)

**Responses:**

**200**: Successful Response

Content-Type: `application/json`

Schema:
string

**422**: Validation Error

Content-Type: `application/json`

Schema:
[HTTPValidationError](models.md#httpvalidationerror)

---
