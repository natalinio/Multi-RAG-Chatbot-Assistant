# Token Management Testing Guide

## Overview
This guide explains how to test the 3-level token protection system implemented to prevent context length overflow errors.

## System Architecture

### 🛡️ 3-Level Protection System

#### **Level 1: Plugin Result Limitation**
- **Location**: `app/plugins/CosmosDbPlugin/CosmosDbPlugin.py`
- **Parameter**: `MAX_RESULTS = 50`
- **Behavior**: Limits query results to maximum 50 configurations
- **Warning**: Shows `⚠️ Results truncated from X to 50 configurations`
- **Suggestion**: "Refine your query with more specific filters"

#### **Level 2: Chat History Truncation**
- **Location**: `app/api/router.py`
- **Parameter**: `MAX_CHAT_HISTORY_MESSAGES = 3`
- **Behavior**: Keeps only last 3 user/assistant message pairs
- **Function**: `truncate_chat_history()`
- **Logs**: "Truncating chat history from X to 4 messages"

#### **Level 3: Fresh Session Creation**
- **Location**: `app/api/router.py`
- **Parameter**: `MAX_TOTAL_TOKENS = 80000`
- **Behavior**: Creates fresh session if total tokens > 80K
- **Function**: Automatic reset with only current message
- **Logs**: "Token count too high (X), creating fresh session"

---

## Test Scenarios

### ✅ Scenario A: Normal Query (Expected: No Limitations)

**Test Query**:
```
Show me the configuration for AggregatedData-NielsenGB-Bronze-RTD
```

**Expected Behavior**:
- ✅ Returns 1 configuration
- ✅ Full JSON displayed
- ✅ No warnings
- ✅ Tokens: ~5,000-10,000

**How to Test**:
1. Open http://127.0.0.1:8000
2. Click "Clear" to start fresh
3. Enter the query above
4. Verify response contains complete configuration

**Success Criteria**:
- Complete configuration shown
- No truncation warnings
- Response time < 10 seconds

---

### 🔸 Scenario B: Large Query (Expected: Level 1 Protection)

**Test Query**:
```
Show me all configurations for NielsenGB domain
```

**Expected Behavior**:
- 🔸 **Level 1 Activated**: Results limited to 50 configs
- ⚠️ Warning: "Results truncated from ~110 to 50 configurations"
- 💡 Suggestion shown to refine query
- ✅ Tokens: ~30,000-50,000 (safe range)

**How to Test**:
1. Click "Clear"
2. Enter the query above
3. Look for truncation warning in response
4. Verify only 50 configurations shown

**Success Criteria**:
- Response shows exactly 50 configs
- Truncation warning visible
- Suggestion to refine query shown
- No errors, response completes successfully

**Check Logs**:
```
WARNING: Truncating results from 110 to 50 to prevent token overflow
```

---

### 🔸🔄 Scenario C: Multiple Large Queries (Expected: Level 2 Protection)

**Test Queries** (run consecutively without Clear):
1. `Show me all SAPBW Bronze layer configurations`
2. `Show me all NielsenUS configurations`
3. `Show me all Profisee configurations`
4. `Show me all SFAsseco configurations`
5. `What was my first question?`

**Expected Behavior**:
- 🔸 **Level 1**: Each query limited to 50 configs
- 🔄 **Level 2**: After query 4, oldest messages dropped
- ❌ AI won't remember query #1 when asked in query #5
- ✅ System continues working without errors

**How to Test**:
1. Click "Clear"
2. Run queries 1-4 **without** clicking Clear between them
3. Run query 5 to test memory
4. If AI says "I don't recall" or "I don't have that information", Level 2 is working

**Success Criteria**:
- All 4 queries complete successfully
- Each returns max 50 configs
- Query 5 shows AI forgot the first question
- No token overflow errors

**Check Logs**:
```
INFO: Truncating chat history from 9 to 4 messages
```

---

### 🔸🔄🔄 Scenario D: Extreme Overflow (Expected: Level 3 Protection)

**Test Queries** (run consecutively without Clear):
1. `Show me all NielsenGB configurations`
2. `Show me all SAPBW configurations`
3. `Show me all Profisee configurations`
4. `Show me all NielsenUS configurations`
5. `Show me all SFAsseco Bronze layer configurations`
6. `Show me all SFAmalia configurations`
7. `Hello, what can you help me with?`

**Expected Behavior**:
- 🔸 **Level 1**: Each query limited to 50 configs
- 🔄 **Level 2**: History truncated multiple times
- 🔄🔄 **Level 3**: Around query 5-6, fresh session created
- ✅ Query 7 works perfectly (fresh start)
- ❌ AI won't remember ANY previous queries

**How to Test**:
1. Click "Clear"
2. Run queries 1-6 rapidly without Clear
3. Run query 7 (simple greeting)
4. If AI responds normally to query 7 and doesn't reference any previous queries, Level 3 worked

**Success Criteria**:
- All queries complete without "context_length_exceeded" error
- Query 7 gets a fresh, normal response
- AI has completely forgotten all previous context
- System recovered automatically

**Check Logs**:
```
WARNING: Token count too high (85000), creating fresh session
```

---

### 🧹 Scenario E: Clear Button Test

**Test Steps**:
1. Send query: `Show me SAPBW configurations`
2. Wait for response
3. Click "Clear" button
4. Send query: `What did I just ask you about?`

**Expected Behavior**:
- ✅ First query works normally
- 🧹 Clear button clears session
- ❌ AI responds "I don't have any previous conversation history"
- ✅ Session completely reset

**Success Criteria**:
- AI doesn't remember the previous question
- Response is friendly but indicates no history
- Session ID remains the same but history is empty

**Check Logs**:
```
INFO: Cleared chat session: default
```

---

## Manual Testing Checklist

### Before Testing
- [ ] Application running on http://127.0.0.1:8000
- [ ] Terminal showing logs visible
- [ ] Browser dev tools open (F12) to check network requests

### During Testing
- [ ] Monitor terminal logs for WARNING/ERROR messages
- [ ] Check token count estimates in logs
- [ ] Verify truncation warnings appear in UI
- [ ] Note response times for large queries

### Scenarios to Run
- [ ] Scenario A: Normal query (baseline)
- [ ] Scenario B: Large query (Level 1 test)
- [ ] Scenario C: Multiple queries (Level 2 test)
- [ ] Scenario D: Extreme overflow (Level 3 test)
- [ ] Scenario E: Clear button (functionality test)

### Success Indicators
- [ ] ✅ No "context_length_exceeded" errors
- [ ] ✅ Truncation warnings shown when > 50 results
- [ ] ✅ System auto-recovers from token overflow
- [ ] ✅ Clear button works correctly
- [ ] ✅ All responses complete successfully

---

## Log Monitoring

### Key Log Messages to Watch For

**✅ Good Signs:**
```
INFO: Query executed successfully. Found 110 configurations, returning 50.
WARNING: Truncating results from 110 to 50 to prevent token overflow
INFO: Truncating chat history from 9 to 4 messages
WARNING: Token count too high (85000), creating fresh session
INFO: Estimated tokens before API call: 45000
```

**❌ Bad Signs (Should NOT Appear):**
```
ERROR: context_length_exceeded
ERROR: This model's maximum context length is 128000 tokens
BadRequestError: Error code: 400
```

---

## Expected Token Counts

| Scenario | Estimated Tokens | Protection Level | Status |
|----------|------------------|------------------|--------|
| Single config | 5K - 10K | None | ✅ Normal |
| 10 configs | 20K - 30K | None | ✅ Normal |
| 50 configs (max) | 40K - 60K | Level 1 | ⚠️ Limited |
| 3 conversations | 60K - 80K | Level 2 | 🔄 Truncated |
| > 80K tokens | Fresh session | Level 3 | 🔄🔄 Reset |

---

## Troubleshooting

### Problem: Still getting "context_length_exceeded" errors

**Check**:
1. Verify `MAX_RESULTS = 50` in CosmosDbPlugin
2. Verify `MAX_CHAT_HISTORY_MESSAGES = 3` in router.py
3. Verify `MAX_TOTAL_TOKENS = 80000` in router.py
4. Restart the application to load new settings

### Problem: Not seeing truncation warnings

**Check**:
1. Query returning < 50 results (try NielsenGB domain)
2. Warning message format in plugin response
3. Frontend displaying the warning field

### Problem: AI remembers too much history

**Check**:
1. `truncate_chat_history()` function being called
2. Log shows "Truncating chat history" message
3. `MAX_CHAT_HISTORY_MESSAGES` setting

### Problem: System creates fresh session too early

**Check**:
1. `MAX_TOTAL_TOKENS` might be too low
2. Token estimation might be inaccurate
3. Increase to 100000 if needed

---

## Production Deployment Verification

Before deploying to Azure:

1. **Test all scenarios locally** ✅
2. **Verify logs show expected warnings** ✅
3. **Test with real user queries** ✅
4. **Deploy to Azure**
5. **Test same scenarios in production**
6. **Monitor Azure logs for any issues**
7. **Verify no "context_length_exceeded" errors**

### Post-Deployment Checks

```bash
# Check Azure logs
az webapp log tail --name "app-gda-chatbot-dev" --resource-group "West-EU-Datadistillery-GDA-DEV"

# Look for:
# - "Truncating results from X to 50"
# - "Truncating chat history"
# - "Token count too high, creating fresh session"
# - NO "context_length_exceeded" errors
```

---

## Summary

| Protection Level | Trigger | Action | User Impact |
|------------------|---------|--------|-------------|
| **Level 1** | Query returns > 50 configs | Limit to 50 results | ⚠️ Warning shown, suggest refine query |
| **Level 2** | History > 3 conversations | Keep only last 3 | 🔄 Forgets older questions |
| **Level 3** | Total tokens > 80K | Fresh session | 🔄🔄 Forgets everything, clean start |

**All three levels work together** to ensure the system NEVER hits the 128K token limit and always provides a working experience to users.
