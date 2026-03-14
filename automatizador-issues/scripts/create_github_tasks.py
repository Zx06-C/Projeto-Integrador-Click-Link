
import os
import json
from openai import OpenAI

def create_github_tasks(repo_name, feature_description):
    client = OpenAI()

    # Step 1: Generate sub-tasks using LLM
    prompt = f"""Dado a seguinte feature, gere uma lista de sub-tarefas detalhadas e acionáveis para o desenvolvimento. Cada sub-tarefa deve ser um item separado na lista. O formato de saída deve ser um JSON array de strings, onde cada string é o título de uma sub-tarefa.

Feature: {feature_description}

Exemplo de saída:
[
    "Configurar ambiente de desenvolvimento inicial",
    "Criar estrutura básica do projeto",
    "Implementar autenticação de usuário",
    "Desenvolver interface de usuário para o dashboard"
]
"""

    try:
        response = client.chat.completions.create(
            model="gemini-2.5-flash", # Using gemini-2.5-flash as it's a good balance for this task
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "Você é um assistente útil que gera sub-tarefas para desenvolvimento de software em formato JSON."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Assuming the response content is a JSON string with a key like 'sub_tasks'
        # or directly a JSON array. Let's try to parse it flexibly.
        raw_content = response.choices[0].message.content
        

        
        # Clean the response if it contains markdown code blocks
        clean_content = raw_content.strip()
        if clean_content.startswith("```json"):
            clean_content = clean_content[7:-3].strip()
        elif clean_content.startswith("```"):
            clean_content = clean_content[3:-3].strip()

        try:
            parsed_data = json.loads(clean_content)
            if isinstance(parsed_data, list):
                sub_tasks = parsed_data
            elif isinstance(parsed_data, dict):
                # Look for common keys
                for key in ['sub_tasks', 'tasks', 'items', 'subtarefas']:
                    if key in parsed_data and isinstance(parsed_data[key], list):
                        sub_tasks = parsed_data[key]
                        break
                else:
                    # If no list found, maybe the values are the tasks
                    sub_tasks = [str(v) for v in parsed_data.values() if isinstance(v, (str, list))]
            else:
                sub_tasks = [str(parsed_data)]
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            # Fallback: simple split by lines if JSON fails
            sub_tasks = [line.strip("- ").strip() for line in raw_content.split("\n") if line.strip()]

    except Exception as e:
        print(f"Erro ao gerar sub-tarefas: {e}")
        return

    if not sub_tasks:
        print("Nenhuma sub-tarefa gerada.")
        return

    print(f"Sub-tarefas geradas para a feature '{feature_description}':")
    for i, task in enumerate(sub_tasks):
        print(f"  {i+1}. {task}")

    # Step 2: Create GitHub Issues
    print("\nCriando issues no GitHub...")
    for task in sub_tasks:
        try:
            # Using gh CLI to create an issue
            command = f'gh issue create --repo {repo_name} --title "{task}" --body "Automatizado via Manus AI Skill: github-task-automator"'
            os.system(command)
            print(f"Issue criada: '{task}'")
        except Exception as e:
            print(f"Erro ao criar issue para '{task}': {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Automatiza a criação de sub-tarefas no GitHub.")
    parser.add_argument("--repo", required=True, help="Nome do repositório GitHub (ex: usuario/projeto).")
    parser.add_argument("--feature", required=True, help="Descrição da feature a ser implementada.")

    args = parser.parse_args()
    create_github_tasks(args.repo, args.feature)
