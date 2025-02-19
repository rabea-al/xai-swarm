from xai_components.base import InArg, OutArg, InCompArg, Component, xai_component
from swarm import Agent, Swarm
import os
import json
import time
import deepl
from dotenv import load_dotenv

load_dotenv()
@xai_component
class SwarmAgentComponent(Component):
    name: InArg[str]
    instructions: InArg[str]
    toolbelt_spec: InArg[dict]
    agent: OutArg[any]

    def execute(self, ctx) -> None:
        agent_name = self.name.value
        agent_instructions = self.instructions.value
        agent_tools = self.toolbelt_spec.value if self.toolbelt_spec.value else {}

        new_agent = Agent(
            name=agent_name,
            instructions=agent_instructions,
            functions=list(agent_tools.values())
        )

        self.agent.value = new_agent

@xai_component
class SwarmRunComponent(Component):
    agent: InCompArg[any]
    task: InCompArg[str]
    result: OutArg[any]
    task_stats_file: OutArg[str]

    def execute(self, ctx) -> None:
        swarm = Swarm()
        agent_instance = self.agent.value
        task_description = self.task.value
        task_stats_path = "task_stats.json"

        if not agent_instance or not task_description:
            raise ValueError("Invalid agent or task.")

        start_time = time.time()
        messages = [{"role": "user", "content": task_description}]
        response = swarm.run(agent=agent_instance, messages=messages)
        elapsed_time = time.time() - start_time

        task_result = {
            "task_description": task_description,
            "result": response.messages if hasattr(response, "messages") else str(response),
            "execution_time_seconds": elapsed_time,
            "tool_calls": [
                {
                    "tool_name": call["function"]["name"],
                    "arguments": json.loads(call["function"]["arguments"])
                }
                for msg in response.messages if msg.get("tool_calls")
                for call in msg["tool_calls"]
            ]
        }

        if os.path.exists(task_stats_path):
            with open(task_stats_path, "r", encoding="utf-8") as f:
                try:
                    task_stats = json.load(f)
                except json.JSONDecodeError:
                    task_stats = {}
        else:
            task_stats = {}

        task_id = f"task_{len(task_stats) + 1}"
        task_stats[task_id] = task_result

        with open(task_stats_path, "w", encoding="utf-8") as f:
            json.dump(task_stats, f, indent=4, ensure_ascii=False)

        self.result.value = task_result["result"]
        self.task_stats_file.value = task_stats_path

@xai_component
class SwarmMakeToolbeltComponent(Component):
    name: InArg[str]
    toolbelt_spec: OutArg[dict]

    def execute(self, ctx) -> None:
        toolbelt_name = self.name.value if self.name.value is not None else "default"
        toolbelt_key = f"toolbelt_{toolbelt_name}"
        tools = ctx.setdefault(toolbelt_key, {})
        self.toolbelt_spec.value = {tool_name: tool_ref for tool_name, tool_ref in tools.items()}

@xai_component
class SwarmTranslateTextToolComponent(Component):
    tool_name: InArg[str]
    toolbelt: InArg[str]
    tool: OutArg[any]

    def execute(self, ctx) -> None:
        tool_name = self.tool_name.value
        toolbelt_name = self.toolbelt.value if self.toolbelt.value is not None else "default"
        toolbelt_key = f"toolbelt_{toolbelt_name}"

        def translate_text(input_file: str, target_language: str) -> str:
            try:
                with open(input_file, 'r', encoding='utf-8') as f:
                    text = f.read()
                auth_key = os.getenv("DEEPL_API_KEY")
                if not auth_key:
                    return "Missing API key."
                translator = deepl.Translator(auth_key)
                result = translator.translate_text(text, target_lang=target_language.upper())
                return result.text
            except Exception as e:
                return f"Error: {str(e)}"

        ctx.setdefault(toolbelt_key, {})[tool_name] = translate_text
        self.tool.value = translate_text

@xai_component
class SwarmWriteFileToolComponent(Component):
    tool_name: InArg[str]
    toolbelt: InArg[str]
    tool: OutArg[any]

    def execute(self, ctx) -> None:
        tool_name = self.tool_name.value if self.tool_name.value else "write_file"
        toolbelt_name = self.toolbelt.value if self.toolbelt.value is not None else "default"
        toolbelt_key = f"toolbelt_{toolbelt_name}"

        def write_file_content(file_path: str, content: str) -> str:
            try:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                return f"File saved: {file_path}"
            except Exception as e:
                return f"Error saving file {file_path}: {str(e)}"

        ctx.setdefault(toolbelt_key, {})[tool_name] = write_file_content
        self.tool.value = write_file_content
