import os
from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel
from src.agent.puzzle_master import PuzzleMasterAgent


if __name__ == '__main__':

    model = LiteLLMModel(model_id="gemini/gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY"))
    solver = PuzzleMasterAgent(model=model)    

    letras_do_dia=["a","a","a","c","g","i","j","l","l","n","o","o","o","o","r","r","t"],
    
    found_words = solver.find_words(letras_do_dia)
    print(f"quantidade de palavras encontradas {len(found_words)}")
    
    solver.validate_word_list(found_words)
    
    