# 📝 Manual do Participante: Experimento de Engenharia de Software
Seja bem-vindo(a) ao nosso estudo empírico! Este experimento faz parte de uma pesquisa que avalia a eficiência e a profundidade na escrita de testes unitários para sistemas backend.  A sua tarefa consiste em escrever uma suíte de testes robusta para um módulo de alta complexidade semântica (cálculos e aritmética de calendário). Leia as instruções abaixo com muita atenção antes de iniciar. 

## 🛑 Regras Restritivas Obrigatórias (Blindagem Científica)
- **Desative Extensões de IA:** É expressamente proibida a utilização de assistentes de IA (como GitHub Copilot, Cursor AI, ChatGPT ou similares) durante o desenvolvimento. O código deve refletir exclusivamente o seu esforço cognitivo.  
- **Sem Ferramentas de Cobertura:** É proibido o uso de qualquer extensão visual ou comandos de cobertura de código (como flags --cov, coverage run ou plugins visuais no editor). O seu desenvolvimento deve ser guiado de forma "cega", baseando-se apenas no feedback de sucesso ou falha do framework de testes.
- **Validação Exclusiva:** Não utilize o comando pytest puro no terminal. Você deve validar o seu progresso utilizando única e exclusivamente o script de automação fornecido localmente.

## 🚀 Instruções de Execução
### 1. Inicialização e Criação da Branch (Marco Zero)
Antes de tocar em qualquer arquivo ou linha de código, você precisa criar a sua branch de trabalho utilizando o padrão de nomenclatura do experimento para que o cronômetro do seu Lead Time comece a contar corretamente.

Abra o terminal na raiz do projeto e execute:
```
# Certifique-se de estar na main limpa
git checkout main

# Crie e mude para a sua branch utilizando seu nome (ex: feature/humano-ester)
git checkout -b feature/humano-SEU_NOME

# Salve o marco zero criando um commit inicial vazio (apenas quando estiver pronto para começar, pois seu tempo será contabilizado a partir desse comando)
git commit --allow-empty -m "Iteration Status: START - Humano SEU_NOME"
```

### 2. Preparação do Ambiente
Ative o ambiente virtual do projeto e certifique-se de que as dependências estão isoladas através do Poetry:
```
# Dá permissão de execução para o script de testes
chmod +x test.sh

# Ativa e instala o ambiente
poetry install
poetry shell
```

### 3. O Desafio
O seu objetivo é escrever uma suíte de testes unitários abrangente dentro do arquivo tests/test_relativedelta.py para cobrir e validar o comportamento do módulo contido em src/relativedelta.py.

Dica: Você pode (e deve) abrir o arquivo src/relativedelta.py para analisar sua estrutura e fluxo lógico, deduzindo os cenários lógicos e casos de borda que precisam ser validados.

### 4. Como Rodar os Testes e Salvar o Progresso
Sempre que desejar executar a sua suíte de testes para validar seu código, execute o comando abaixo na raiz do projeto:

```
./test.sh
```

### 5. Critério de Conclusão
A tarefa estará oficialmente concluída quando:

- Você julgar que mapeou todos os cenários lógicos necessários para garantir a robustez do módulo.
- A execução do comando ./test.sh retornar 100% de sucesso (PASSED).

Ao finalizar, faça o git push da sua branch para o repositório remoto:

```
git push origin feature/humano-SEU_NOME
```
Muito obrigado pela sua colaboração!
