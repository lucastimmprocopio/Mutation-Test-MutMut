# Demo: Testes de Mutação com mutmut (Python)

Projeto de demonstração para o vídeo sobre **Testes de Mutação**.

## O que tem aqui

```
mutation-demo/
├── shipping.py              -> Código de produção (cálculo de total de pedido)
├── tests/
│   └── test_shipping.py     -> Suite de testes ATUAL (começa como "fraca")
├── reference/
│   └── test_shipping_weak.py.txt  -> Versão fraca (cópia de referência)
├── requirements.txt
├── setup.cfg                -> Configuração do mutmut
└── SCRIPT.md                 -> Roteiro de narração do vídeo
```

## Setup (rodar fora da gravação, ou cortar na edição)

```bash
python -m venv venv
source venv/bin/activate        # no Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Passo a passo da demo

### 1. Estado inicial (suite "fraca")

O arquivo `tests/test_shipping.py` JÁ ESTÁ na versão fraca (esses testes
existem em `reference/test_shipping_weak.py.txt` também, caso precise
restaurar).

Rode os testes normalmente, mostrando que passam com 100% de cobertura:

```bash
python -m pytest -v --cov=shipping --cov-report=term-missing
```

Resultado esperado: **6 testes passam, 100% de cobertura**.

> Aqui é o momento de falar: "Olha, 100% de cobertura! Os testes estão
> ótimos, certo?" — e então introduzir a pergunta que o teste de mutação
> responde: **"Mas será que esses testes REALMENTE verificam o
> comportamento certo?"**

### 2. Rodando o mutmut na suite fraca

```bash
mutmut run
```

Isso demora alguns segundos (gera ~48 mutantes e roda a suite contra
cada um). Resultado esperado:

- 🎉 **8 mutantes mortos** (Killed)
- 🙁 **40 mutantes sobreviveram** (Survived)

Para ver um exemplo de mutante sobrevivente:

```bash
mutmut show 7
```

Isso mostra um diff tipo:
```diff
-    discount = 0.0
+    discount = 1.0
```

E o teste continuou passando! Ou seja: a lógica de negócio podia estar
**completamente quebrada** (desconto de 100% em todo pedido) e nenhum
teste detectaria isso.

### 3. Melhorando os testes (a "solução")

O arquivo `tests/test_shipping.py` já está pronto com a versão FORTE
dos testes (veja o conteúdo do arquivo — ele tem comentários explicando
cada caso de borda).

Se quiser demonstrar a transição "ao vivo" durante a gravação, você pode:
1. Antes da gravação, copiar a versão forte para um arquivo separado
   (`tests/test_shipping_strong.py.txt`, por exemplo).
2. Durante a gravação, mostrar o conteúdo da suite fraca, explicar os
   problemas, e então colar/digitar a suite forte no lugar.

A suite forte testa:
- Casos sem desconto
- Limites exatos de cada faixa de desconto (3, 5, 10 itens)
- Cupons válidos e inválidos
- O *cap* de desconto máximo (30%)
- A fronteira exata do frete grátis (R$ 200)
- Validação de entradas inválidas (negativos)

### 4. Rodando o mutmut de novo (a "validação")

```bash
rm -rf .mutmut-cache   # limpa o cache para rodar do zero
mutmut run
```

Resultado esperado:

- 🎉 **37 mutantes mortos**
- 🙁 **11 mutantes sobreviveram** (de 48)

Isso já é uma evolução de **8/48 (16,7%) para 37/48 (77%)** de mutantes
mortos — com a MESMA suite de 100% de cobertura de linha!

### 5. Bônus: analisando os sobreviventes restantes

```bash
mutmut results
mutmut show <id>
```

Os 11 sobreviventes restantes são, em sua maioria, **mutantes
equivalentes** ou pequenas oportunidades extras de melhoria:

- Mutações dentro do docstring/comentários (não afetam comportamento)
- Mudança na mensagem de erro do `ValueError` (texto não testado, e
  normalmente não importa)
- `discount += 0.10` vs `discount = 0.10` quando combinado com desconto
  de quantidade (ex: quantity=5 + cupom PROMO10 — bom desafio para o
  aluno expandir!)
- `round(..., 2)` vs `round(..., 3)` — só seria pego com um valor que
  tenha 3 casas decimais relevantes

Esse é um ótimo gancho para encerrar o vídeo: **"Testes de mutação não
pedem 100% de mutation score sempre — eles mostram ONDE focar esforço de
teste, e nos ajudam a identificar mutantes equivalentes (que não importam)
vs. lacunas reais."**

## Comandos de referência rápida

| Comando | O que faz |
|---|---|
| `python -m pytest -v --cov=shipping --cov-report=term-missing` | Roda os testes com cobertura |
| `mutmut run` | Roda o teste de mutação |
| `mutmut results` | Lista os mutantes e seus status |
| `mutmut show <id>` | Mostra o diff de um mutante específico |
| `rm -rf .mutmut-cache` | Limpa o cache do mutmut (rodar do zero) |
