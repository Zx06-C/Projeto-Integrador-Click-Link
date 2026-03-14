---
name: automatizador-issues
description: "Automatiza a criação de sub-tarefas (issues) no GitHub a partir de uma descrição de feature. Use para: gerar e enviar sub-tarefas detalhadas para um repositório GitHub."
---

# GitHub Task Automator

Esta skill permite automatizar a criação de sub-tarefas no GitHub. Você fornece uma descrição de uma feature, e a skill gera uma lista de sub-tarefas acionáveis e as cria como issues no repositório especificado.

## Como usar

Para utilizar esta skill, você precisará fornecer o nome do repositório GitHub (no formato `usuario/projeto`) e a descrição da feature.

**Exemplo de uso:**

```python
import os

repo = "Zx06-C/Projeto-Integrador-Click-Link"
feature = "Implementar um sistema de login e registro de usuários com autenticação via e-mail e senha."

# Chamar o script para criar as tarefas
os.system(f"python /home/ubuntu/skills/github-task-automator/scripts/create_github_tasks.py --repo {repo} --feature \"{feature}\"")
```

## Recursos

- `scripts/create_github_tasks.py`: Script Python que utiliza um modelo de linguagem para gerar sub-tarefas e a CLI do GitHub para criar as issues no repositório.
