# agent-imbroglio-solver

Projeto para resolver o quebra-cabeça diário Imbroglio em português do Brasil, usando um agente de IA, busca combinatória de palavras e validação com cache.

## O que o projeto faz

- Lê as letras disponíveis de um puzzle.
- Procura palavras possíveis em uma base local de palavras.
- Monta combinações de até 3 palavras que consumam todas as letras do puzzle.
- Remove soluções repetidas.
- Ordena as soluções por score.
- Valida palavras com IA ou com intervenção humana quando necessário.
- Salva palavras já validadas em cache para evitar retrabalho.

## Funcionalidades principais

### 1. Resolução de puzzles

A função principal de busca está em `app/src/tools/puzzle_solver.py`.

Ela:
- carrega a base `all_words.json`;
- verifica quais palavras podem ser formadas com as letras disponíveis;
- gera combinações recursivas de palavras;
- limita a busca por número máximo de palavras, tempo de execução e quantidade de soluções;
- filtra soluções duplicadas;
- calcula um score para ranquear os melhores resultados.

O score é baseado no tamanho das palavras normalizadas, usando a soma de $len(palavra)^2$ para cada item da solução.

### 2. Validação de palavras

Em `app/src/tools/word_validation.py` existem duas formas de validação:

- `evaluate_words_ai`: valida uma lista de palavras via modelo de IA, em lotes;
- `evaluate_words_human`: pede validação manual ao usuário.

O fluxo da validação retorna um dicionário no formato:

```json
{
  "palavra": {
    "veredito": "VALIDA|INVALIDA|DUVIDA",
    "justificativa": "..."
  }
}
```

### 3. Cache de palavras validadas

Em `app/src/tools/file_handler.py` o projeto mantém um cache local de palavras já avaliadas.

Principais ações:
- carregar palavras validadas;
- salvar novas validações;
- fazer merge automático com o cache existente.

Isso reduz chamadas repetidas ao modelo de IA e acelera execuções futuras.

### 4. Agente de IA

O arquivo `app/main.py` cria um `CodeAgent` com ferramentas específicas para resolver o puzzle.

O agente usa:
- modelo de geração para raciocínio e execução;
- prompts definidos em `app/src/utils/prompts.yaml`;
- configuração em `app/src/utils/config.json`.

### 5. Configuração por arquivos locais

O projeto separa parâmetros de execução em arquivos de configuração:

- `app/src/utils/config.json`: IDs de modelos, parâmetros de geração e caminhos;
- `app/src/utils/prompts.yaml`: instruções do agente, prompt da tarefa e prompt de validação.

## Estrutura resumida

- `app/main.py` — ponto de entrada da aplicação.
- `app/src/tools/puzzle_solver.py` — busca e rankeamento de soluções.
- `app/src/tools/word_validation.py` — validação automática e humana.
- `app/src/tools/file_handler.py` — cache de palavras validadas.
- `app/src/utils/client_utils.py` — cliente para IA.
- `app/src/utils/prompt_manager.py` — carregamento e renderização de prompts.
- `app/src/utils/word_utils.py` — verificação se uma palavra pode ser formada com as letras disponíveis.
- `app/src/data/` — base de palavras e arquivos com puzzles diários.

## Fluxo de uso

1. Carregar o cache de palavras validadas.
2. Buscar combinações de palavras possíveis para as letras do puzzle.
3. Validar palavras que ainda não estão no cache.
4. Salvar as novas validações.
5. Repetir a busca até obter soluções válidas.

## Dados usados pelo projeto

- `app/src/data/all_words.json` — base principal de palavras.
- `app/src/data/daily_puzzles_6.json` — puzzles diários com letras e solução.
- `app/src/data/daily_puzzles_6_with_words.json` — versão enriquecida com palavras.
- `validated_words.json` e `validated_words_cache.json` — cache de validações.

## Observações

- O projeto atual está mais orientado a agente do que a um script simples.
- A pasta `old/` contém uma versão anterior e arquivos históricos.
- As credenciais para IA dependem da variável de ambiente `GEMINI_API_KEY`.

## Resumo

Em termos práticos, este repositório automatiza a descoberta, validação e organização de soluções para o Imbroglio, combinando busca por letras, IA e cache local.