from __future__ import annotations
import logging
import traceback

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.prompts import load_mcp_prompt
from langchain_mcp_adapters.resources import load_mcp_resources
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage
from sqlalchemy.orm import Session

from src.agent.config import get_llm
from src.agent.db_checkpointer import get_checkpointer, make_thread_id
from src.settings import config
from src.utils.error_logger import log_error
from src.utils.exceptions.custom_exceptions import AgentException

logger = logging.getLogger(__name__)
FILE_NAME = "agent.py"

SYSTEM_PROMPT = """You are BeanBrew's friendly coffee shop assistant. 
You help customers browse the menu, place orders, and check order status.
Always be warm, helpful, and enthusiastic about coffee! 
Use emojis occasionally to make the conversation feel cozy and welcoming. ☕
When a customer wants to place an order, use the create_order tool.
Always confirm order details before and after placing them."""


async def run(
    customer_id: int,
    customer_name: str,
    user_message: str,
    db: Session,
) -> str:
    try:
        async with MultiServerMCPClient(
            {
                "beanbrew": {
                    "url": config.MCP_SERVER_URL,
                    "transport": "streamable_http",
                }
            }
        ).session("beanbrew") as session:

            # Load tools
            tools = await load_mcp_tools(session)
            logger.info(f"[agent] Loaded {len(tools)} tools: {[t.name for t in tools]}")

            # Load prompt
            try:
                prompt_messages = await load_mcp_prompt(
                    session,
                    "order_assistant",
                    arguments={"customer_name": customer_name},
                )
            except Exception:
                prompt_messages = [
                    SystemMessage(content=f"You are helping {customer_name}. " + SYSTEM_PROMPT)
                ]

            # Load resources
            try:
                blobs = await load_mcp_resources(session)
                resource_context = ""
                for blob in blobs:
                    try:
                        uri = blob.metadata.get("uri", "resource")
                        text = blob.as_bytes().decode("utf-8", errors="replace")
                        resource_context += f"\n[{uri}]\n{text}\n"
                    except Exception:
                        pass
            except Exception:
                resource_context = ""

            # Build messages
            messages = list(prompt_messages)
            if resource_context:
                messages.append(
                    HumanMessage(
                        content=(
                            "Current shop data (menu & info):\n" + resource_context
                        )
                    )
                )
            messages.append(
                HumanMessage(
                    content=f"[Customer: {customer_name}, ID: {customer_id}]\n{user_message}"
                )
            )

            llm = get_llm(max_tokens=1000, temperature=0.1)

            async with get_checkpointer() as checkpointer:
                agent = create_react_agent(
                    model=llm,
                    tools=tools,
                    checkpointer=checkpointer,
                    state_modifier=SYSTEM_PROMPT,
                )

                thread_id = make_thread_id(customer_id)
                agent_config = {"configurable": {"thread_id": thread_id}}

                result = await agent.ainvoke(
                    {"messages": messages},
                    config=agent_config,
                )

                all_messages = result.get("messages", [])
                if not all_messages:
                    return "I'm sorry, I couldn't process your request. Please try again."

                final_message = all_messages[-1]
                content = final_message.content

                if isinstance(content, list):
                    full_response = "".join(
                        block["text"]
                        for block in content
                        if isinstance(block, dict) and "text" in block
                    )
                elif isinstance(content, str):
                    full_response = content
                else:
                    full_response = str(content)

                return full_response.strip() or "I'm sorry, I couldn't process your request."

    except Exception as exc:
        logger.error(f"[agent.run] ERROR:\n{traceback.format_exc()}")
        log_error(
            db=db,
            function_name="run",
            file_name=FILE_NAME,
            error_message=str(exc),
            stack_trace=traceback.format_exc(),
        )
        raise AgentException(f"Agent failed: {str(exc)}")
