# 🚨 Token Limit Problem & Solution

## Problem Identified
The system exceeded Azure OpenAI's token limit:
```
This model's maximum context length is 128000 tokens. 
However, your messages resulted in 775339 tokens 
(774690 in the messages, 649 in the functions)
```

## Root Causes

### 1. **Chat History Accumulation** (774,690 tokens!)
- The system saved the ENTIRE conversation with every request
- Plugin descriptions were very long (649 tokens just for functions)
- System prompt was very detailed (~2,000+ tokens)

### 2. **Excessive Plugin Descriptions**
- `@kernel_function` descriptions were too verbose
- Every API call included all plugin descriptions

## ✅ Solutions Implemented

### 1. **Chat History Management**
```python
# Configuration to limit tokens
MAX_CHAT_HISTORY_MESSAGES = 10  # Keep only last 10 messages
MAX_TOTAL_TOKENS = 100000  # Safety threshold

def truncate_chat_history(chat_history: ChatHistory) -> ChatHistory:
    # Keeps only: system message + last N user/assistant exchanges
```

### 2. **Reduced System Prompt** 
- Reduced from ~2000 tokens to ~300 tokens
- Keeps essential rules
- Removes redundant examples

### 3. **Compact Plugin Descriptions**
Before:
```python
description="""Searches ETL configuration documentation to provide guidance on:
- ETL pipeline configuration parameters and schemas
- Best practices for Bronze, Silver, and Gold data layers
- Data transformation patterns and techniques
[...molto altro testo...]"""
```

After:
```python
description="Search ETL documentation for configuration guidance, examples, and best practices."
```

### 4. **New Endpoint for Complete JSON Examples**
```python
@router.get("/json-examples/{layer}")
async def get_json_examples(layer: str, process_type: str = "all"):
    # Dedicated endpoint for JSON examples without chat history
```

### 5. **Token Monitoring**
```python
def estimate_token_count(text: str) -> int:
    return len(text) // 4  # Approximate estimation

# Log token count before each API call
estimated_tokens = estimate_token_count(total_text)
logger.info(f"Estimated tokens before API call: {estimated_tokens}")
```

## How to Use the Solution

### For General Questions
Use the normal chat - it now handles tokens automatically:
```
POST /api/chat
{
  "message": "How to configure transformation?",
  "session_id": "user123"
}
```

### For Complete JSON Examples
Use the dedicated endpoint:
```
GET /api/json-examples/silver?process_type=upsert
```

### To Clear the Session
```
POST /api/clear-session
```

## New Behavior

1. **Auto-truncation**: If the conversation exceeds 10 messages, keeps only the most recent ones
2. **Automatic reset**: If tokens exceed 100K, creates a fresh session
3. **Detailed logging**: Shows estimated token count before each call
4. **Shorter responses**: Reduced settings for more concise responses

## Testing the Solution

Try the same question that caused the error:
```
"give me an example of full json config for a silver job, with upsert in data load process"
```

The system should now:
✅ Handle the request without token errors
✅ Provide the complete JSON configuration
✅ Keep the history under control

## Monitoring

Check the logs to see:
```
INFO:app.api.router:Estimated tokens before API call: 15000
INFO:app.api.router:Truncating chat history from 25 to 11 messages
```

This confirms that the system is properly managing tokens.