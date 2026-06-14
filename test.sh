#!/bin/bash

# 1. Roda os testes usando o Poetry e captura a saída
echo "Running tests..."
OUTPUT=$(poetry run pytest tests/test_relativedelta.py 2>&1)
EXIT_CODE=$?

# Exibe o resultado na tela para o desenvolvedor ou IA lerem
echo "$OUTPUT"

# 2. Prepara o commit automático
git add .

# 3. Define a mensagem com base no resultado do teste
if [ $EXIT_CODE -eq 0 ]; then
    MSG="Iteration Status: PASSED"
else
    # Extrai a última linha do erro ou do traceback para dar contexto à mensagem do commit
    SHORT_ERROR=$(echo "$OUTPUT" | grep -E "E   |FAIL|ERROR" | tail -n 1 | cut -c1-50)
    if [ -z "$SHORT_ERROR" ]; then
        SHORT_ERROR="Tests failing"
    fi
    MSG="Iteration Status: FAILED - $SHORT_ERROR"
fi

# 4. Faz o commit (se houver alterações no código)
git commit -m "$MSG" --allow-empty

# Retorna o código de saída original do pytest para o Cursor Agent entender se deu erro ou não
exit $EXIT_CODE