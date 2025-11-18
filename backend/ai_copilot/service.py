"""
AI Copilot service - DeepSeek R1 integration with tool calling
"""
import httpx
import os
import json
from typing import Dict, List, Optional
from backend.utils.logger import logger
from backend.ai_copilot.tools import get_tools_schema, call_tool
from backend.ai_copilot.prompt import SYSTEM_PROMPT

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

async def chat_with_copilot(
    messages: List[Dict],
    user_id: Optional[str] = None,
    db_session = None
) -> Dict:
    """Chat with AI Copilot with tool calling support"""
    if not OPENROUTER_API_KEY:
        return {
            "error": "OPENROUTER_API_KEY not configured",
            "message": "AI Copilot is not available. Please configure OPENROUTER_API_KEY."
        }
    
    # Prepare messages with system prompt
    chat_messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + messages
    
    # Get tools schema
    tools = get_tools_schema()
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                OPENROUTER_URL,
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek/deepseek-r1:free",
                    "messages": chat_messages,
                    "tools": tools,
                    "temperature": 0.2,
                    "max_tokens": 4096
                }
            )
            response.raise_for_status()
            data = response.json()
            
            choice = data["choices"][0]
            message = choice["message"]
            
            # Check if tool calls are requested
            if "tool_calls" in message and message["tool_calls"]:
                tool_results = []
                
                for tool_call in message["tool_calls"]:
                    tool_name = tool_call["function"]["name"]
                    tool_args = json.loads(tool_call["function"]["arguments"])
                    
                    try:
                        # Inject db_session if tool needs it
                        if db_session and "db" in inspect.signature(call_tool).parameters:
                            tool_args["db"] = db_session
                        
                        result = await call_tool(tool_name, tool_args)
                        tool_results.append({
                            "tool_call_id": tool_call["id"],
                            "role": "tool",
                            "name": tool_name,
                            "content": json.dumps(result)
                        })
                    except Exception as e:
                        logger.error(f"Error calling tool {tool_name}: {e}")
                        tool_results.append({
                            "tool_call_id": tool_call["id"],
                            "role": "tool",
                            "name": tool_name,
                            "content": json.dumps({"error": str(e)})
                        })
                
                # Make follow-up call with tool results
                follow_up_messages = chat_messages + [
                    message,
                    *tool_results
                ]
                
                follow_up_response = await client.post(
                    OPENROUTER_URL,
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "deepseek/deepseek-r1:free",
                        "messages": follow_up_messages,
                        "temperature": 0.2,
                        "max_tokens": 4096
                    }
                )
                follow_up_response.raise_for_status()
                follow_up_data = follow_up_response.json()
                
                return {
                    "message": follow_up_data["choices"][0]["message"]["content"],
                    "tool_calls": [tc["function"]["name"] for tc in message.get("tool_calls", [])]
                }
            
            return {
                "message": message["content"],
                "tool_calls": []
            }
    
    except Exception as e:
        logger.error(f"Error in AI Copilot: {e}")
        return {
            "error": str(e),
            "message": "Sorry, I encountered an error. Please try again."
        }

import inspect
