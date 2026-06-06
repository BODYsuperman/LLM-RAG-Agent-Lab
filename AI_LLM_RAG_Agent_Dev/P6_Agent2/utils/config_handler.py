import yaml
from path_tool import get_abs_path


def load_rag_config(config_path:str = None, encoding:str= "utf-8"):
    if config_path is None:
        config_path = get_abs_path("config/rag.yml")
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.safe_load(f) or {}


def load_chroma_config(config_path:str = None, encoding:str= "utf-8"):
    if config_path is None:
        config_path = get_abs_path("config/chroma.yml")
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.safe_load(f) or {}


def load_prompts_config(config_path:str = None, encoding:str= "utf-8"):
    if config_path is None:
        config_path = get_abs_path("config/prompts.yml")
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.safe_load(f) or {}


def load_agent_config(config_path:str = None, encoding:str= "utf-8"):
    if config_path is None:
        config_path = get_abs_path("config/agent.yml")
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.safe_load(f) or {}
    
rag_conf = load_rag_config()

chroma_conf = load_chroma_config()

prompts_conf = load_prompts_config()

agent_conf = load_agent_config()

if __name__ == '__main__':
    print(agent_conf["chat_model_name"])
