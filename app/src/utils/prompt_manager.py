import yaml
from pathlib import Path
from typing import Dict, Any
from jinja2 import Template


def load_prompts(prompt_name) -> Dict[str, str]:

    prompts_path = Path(__file__).parent / "prompts.yaml"

    with open(prompts_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return data.get("prompts", {}).get(prompt_name, {})


def fill_prompt(prompt_template: str, **variables) -> str:
    template = Template(prompt_template)
    return template.render(**variables)


x = load_prompts("task_prompt")
print(x)
y = fill_prompt(x, letters=["a", "b", "c"], solver_settings_str="settings")

print(y)
