# Fix for "Failed to parse invalid URL" Error

## Problem Description

Users were encountering the following error:
```
Uncaught (in promise) Error: Failed to parse invalid URL ""
```

This error occurred when the Google Generative AI library tried to make API calls with improperly configured or empty API keys.

## Root Cause

The `AIAssistant` class in `ai_assistant.py` had insufficient validation for:
1. Empty or whitespace-only API keys
2. Empty or whitespace-only model names
3. Attempts to call `generate_async()` when the model was not properly initialized

When an empty string was passed as the API key or model name, the validation didn't catch it, and the Google Generative AI SDK would attempt to make requests with invalid configuration, resulting in URL parsing errors.

## Fix Applied

### Changes to `ai_assistant.py`

1. **Improved API Key Validation**:
   - API key is now normalized: `self.api_key = (api_key or "").strip()`
   - This handles `None` values and strips whitespace

2. **Model Name Validation**:
   - Model name is validated and defaults to "gemini-pro" if empty:
   ```python
   self.model_name = model_name.strip() if isinstance(model_name, str) and model_name.strip() else "gemini-pro"
   ```

3. **Added Readiness Check in generate_async()**:
   - Before attempting to generate content, the method now checks if the assistant is ready:
   ```python
   if not self.is_ready():
       error_msg = "AI Assistant is not properly configured"
       logger.error(error_msg)
       callback("", error_msg)
       return
   ```

4. **Enhanced Logging**:
   - Added warning log when API key is invalid or missing

## Testing

To verify the fix works correctly:

1. **Empty API Key**: The assistant gracefully handles empty API keys without throwing errors
2. **Whitespace API Key**: Whitespace-only keys are treated as empty
3. **None API Key**: `None` values are safely handled
4. **Default Placeholder**: The placeholder `"YOUR_GEMINI_API_KEY_HERE"` is recognized and rejected
5. **Early Failure**: Attempts to use AI features without proper configuration fail gracefully with clear error messages

## User Impact

- **Before**: Application would crash with cryptic "Failed to parse invalid URL" errors
- **After**: Application handles invalid configurations gracefully with clear error messages in the UI and logs

## For Developers

If you're extending this code, remember to:
- Always check `is_ready()` before calling AI methods
- Normalize and validate all string inputs
- Use proper error callbacks instead of throwing exceptions in async contexts
- Log configuration issues clearly for debugging

## Related Files

- `ai_assistant.py` - Main fix location
- `editor.py` - Uses AIAssistant, benefits from improved error handling
- `config.ini` / `config.example.ini` - Configuration source

---

**Fixed in**: Branch `fix-invalid-empty-url-parse-uncaught-promise`
**Date**: 2024
