from smolagents import CodeAgent
from src.tools.find_words import find_possible_words
from src.tools.validation import evaluate_words_ai, evaluate_words_human
from src.tools.cache_handler import load_cache, save_cache


class PuzzleMasterAgent:
    def __init__(self, model):      
        
        self.model = model
  
        tools = [find_possible_words,
                 evaluate_words_ai,
                 #evaluate_words_human
                 ]

        self.agent = CodeAgent(
            tools=tools,
            model=model,
        )

    def find_words(self, letters_for_puzzle: list):
        prompt = f"""
        Sua tarefa é encontrar todas as palavras possíveis que podem ser formadas com a seguinte lista de letras: {letters_for_puzzle}.
        Para fazer isso, utilize a ferramenta 'find_possible_words' e passe a lista de letras como argumento.
        Retorne o resultado diretamente.
        """
        result = self.agent.run(prompt)
        return result
    
    def validate_word_list(self, word_list: list):
        
        cache = load_cache()       
        approved_words = []     
        new_validation = False
        
        for word_dict in word_list:
            norm_word = word_dict['normalized']
            if norm_word in cache:
                veredito_ai = cache[norm_word]
            
            else:
                new_validation = True              
                veredito_ai = evaluate_words_ai(word_dict, self.model)     
                cache[norm_word] = veredito_ai
                       
            veredito = veredito_ai.get("veredito", "ERRO")
            if veredito == "VALIDA":
                approved_words.append(word_dict)
                
            elif veredito == "DUVIDA":
                pass
            #     justificativa = veredito_ai.get("justificativa", "Sem justificativa.")
            #     if evaluate_words_human(word_dict, justificativa):
            #         approved_words.append(word_dict)                   
            # else:
            #     justificativa = veredito_ai.get("justificativa", "Motivo desconhecido.")

        if new_validation:
            save_cache(cache)
        
        return approved_words

        

