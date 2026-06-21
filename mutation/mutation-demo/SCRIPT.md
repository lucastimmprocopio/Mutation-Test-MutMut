# Roteiro do Vídeo — Testes de Mutação com mutmut

Tempo total estimado: ~12-13 minutos. Ajuste o ritmo de fala conforme
necessário, mas tente não passar de 15min no total.

Dica de produção: grave em blocos (uma seção por vez) e corte os tempos
mortos de instalação/carregamento na edição. Não precisa gravar tudo de
uma vez.

---

## 1. Introdução (1:30 - 2:00 min)

**Fala sugerida:**

> "Olá! Hoje vou mostrar uma prática avançada de qualidade de software
> chamada **Teste de Mutação**, ou *Mutation Testing*.
>
> A pergunta que ela responde é simples, mas incômoda: **a cobertura de
> testes do seu projeto realmente significa alguma coisa?**
>
> É muito comum vermos pipelines de CI exibindo orgulhosamente '100% de
> cobertura de código' — mas cobertura de linha só diz que aquela linha
> foi EXECUTADA durante os testes. Ela não diz nada sobre se o teste
> verificou o RESULTADO certo.
>
> É aqui que entra o teste de mutação. A ferramenta — no nosso caso, o
> **mutmut**, para Python — pega o seu código de produção e introduz
> pequenas alterações de propósito: troca um `>` por `>=`, um `+` por
> `-`, muda um valor de `0.10` para `1.0`, etc. Essas alterações são
> chamadas de **mutantes**.
>
> Depois, ele roda a sua suite de testes contra cada mutante. Se algum
> teste FALHAR, dizemos que o mutante foi **morto** — ótimo, significa
> que seu teste detectaria esse bug. Mas se TODOS os testes continuarem
> passando mesmo com o código alterado, o mutante **sobreviveu** — e
> isso é um sinal de que seus testes têm um buraco.
>
> Vamos ver isso na prática com um projeto bem simples: uma função que
> calcula o total de um pedido com desconto e frete."

---

## 2. O Problema (1:30 - 2:00 min)

**Ação na tela:** Mostre o arquivo `shipping.py` e explique rapidamente
as regras de negócio (desconto por quantidade, cupom, cap de 30%, frete
grátis acima de R$200).

**Fala sugerida:**

> "Aqui está a nossa função `calculate_order_total`. As regras são:
> desconto por quantidade de itens, desconto por cupom, um limite máximo
> de 30% de desconto total, e frete grátis para pedidos a partir de
> R$200.
>
> Agora olha a suite de testes que já existe."

**Ação na tela:** Mostre `tests/test_shipping.py` (versão fraca).

> "Esses testes... parecem ok, né? Eles chamam a função com vários
> parâmetros e verificam coisas como 'o resultado não é None', 'o
> resultado é um float', 'o resultado é maior que zero'. Vamos rodar."

**Ação na tela:** Rode no terminal:
```bash
python -m pytest -v --cov=shipping --cov-report=term-missing
```

> "Olha aí: 6 testes passando, **100% de cobertura**. Se você olhasse só
> esse número no seu pipeline de CI, diria 'ótimo, esse código está bem
> testado'. Mas será que está mesmo? Vamos descobrir com o mutmut."

---

## 3. O Passo a Passo (6 - 10 min)

### 3.1 Rodando o mutmut na suite fraca (~2 min)

**Ação na tela:** Rode:
```bash
mutmut run
```

> "O mutmut vai gerar várias versões 'mutantes' do nosso `shipping.py` —
> cada uma com uma pequena alteração — e rodar nossa suite de testes
> contra cada uma. Isso pode demorar um pouquinho, vou acelerar aqui."

**(corte o tempo de espera na edição)**

> "Pronto! Olha o resultado: geramos 48 mutantes. Desses, apenas **8
> foram mortos** — ou seja, só 8 vezes nossos testes detectaram que o
> código estava 'errado'. **40 mutantes sobreviveram.**
>
> Em outras palavras: nosso *mutation score* é de aproximadamente **17%**
> — apesar dos 100% de cobertura de linha!"

### 3.2 Inspecionando um mutante sobrevivente (~1-2 min)

**Ação na tela:** Rode:
```bash
mutmut show 7
```

> "Vamos ver um exemplo concreto. Esse mutante mudou a linha
> `discount = 0.0` para `discount = 1.0` — ou seja, o código mutante
> aplicaria **100% de desconto em TODO pedido**. Isso é um bug
> gigantesco, uma empresa daria todo o estoque de graça.
>
> E mesmo assim, nossa suite de testes continuou passando! Por quê?
> Porque nossos testes só checavam 'o resultado não é None' ou 'é maior
> que zero' — e mesmo com 100% de desconto mais frete, o resultado ainda
> é um número maior que zero. O teste não verifica o VALOR CORRETO."

### 3.3 Escrevendo testes melhores (~3-4 min)

> "Agora vamos resolver isso. A estratégia é: em vez de testar 'rodou
> sem erro' ou 'retornou algo', vamos testar **valores exatos**, com
> contas feitas na mão, e principalmente vamos testar os **limites
> (boundaries)** de cada regra."

**Ação na tela:** Abra `tests/test_shipping.py` e mostre/escreva os
novos testes, explicando alguns deles em voz alta. Sugestão de quais
explicar com mais calma (não precisa ler todos):

- `test_no_discount_pays_shipping` — caso base, sem desconto, com frete.
- `test_quantity_three_items_gets_5_percent` e
  `test_quantity_below_discount_threshold` — testando exatamente a
  fronteira de 3 itens (2 itens não tem desconto, 3 itens tem 5%).
- `test_discount_cap_is_30_percent` — testando que 15% (quantidade) +
  20% (cupom) = 35%, mas o sistema limita a 30%.
- `test_free_shipping_exact_threshold` e
  `test_shipping_charged_just_below_threshold` — testando a fronteira
  exata de R$200 (R$200 = frete grátis, R$199 = paga frete).
- `test_negative_subtotal_raises_value_error` — testando validação de
  entrada inválida.

> "Reparem no padrão: para cada regra de negócio, eu calculei o valor
> esperado NA MÃO e testei o limite exato — não só 'um valor qualquer
> dentro da faixa', mas o ponto exato onde o comportamento muda."

### 3.4 Confirmando que a cobertura continua 100% (~1 min)

**Ação na tela:** Rode:
```bash
python -m pytest -v --cov=shipping --cov-report=term-missing
```

> "Os 14 novos testes passam, e a cobertura continua em 100% — igual
> antes. Só que agora cada teste verifica um valor exato, não só 'rodou
> sem erro'."

---

## 4. A Validação (1:30 - 2 min)

**Ação na tela:** Limpe o cache e rode o mutmut novamente:
```bash
rm -rf .mutmut-cache
mutmut run
```

**(corte o tempo de espera)**

> "E aqui está o resultado final: de 48 mutantes, agora **37 foram
> mortos** — contra apenas 8 antes. Nosso mutation score saltou de **17%
> para 77%**, com a MESMA suite de 100% de cobertura de linha.
>
> Isso é a prova de que nossos testes agora realmente validam o
> COMPORTAMENTO da função, não só se ela 'roda sem erro'."

**Ação na tela:** Rode `mutmut results` e mostre rapidamente os 11
sobreviventes restantes.

> "Ainda sobraram 11 mutantes. Vale dar uma olhada neles também — alguns
> são **mutantes equivalentes**, tipo mudanças dentro de comentários, ou
> na mensagem de erro de uma exceção, que não afetam o comportamento real
> e por isso são considerados 'aceitáveis'. Outros, porém, são
> oportunidades reais de melhorar ainda mais a suite — por exemplo,
> testar um cenário onde desconto de quantidade E cupom se somam.
>
> E é exatamente esse o valor do teste de mutação: ele não te diz
> 'escreva mais testes' de forma vaga — ele aponta o **ponto exato** do
> código que não está sendo validado de verdade.
>
> Na próxima vez que você ver '100% de cobertura' num projeto, lembra:
> isso não significa 'testes perfeitos'. Significa só que o código foi
> executado. Para saber se os testes são bons de fato, roda um teste de
> mutação.
>
> É isso! Até a próxima."

---

## Checklist de gravação

- [ ] Áudio testado (sem ruído de fundo, volume consistente)
- [ ] Fonte do terminal grande o suficiente para gravação
- [ ] Cortar tempo de instalação de dependências (`pip install`)
- [ ] Cortar tempo de espera do `mutmut run` (acelerar ou cortar)
- [ ] Garantir que os números mostrados batem com os do README
      (48 mutantes / 8 mortos antes / 37 mortos depois)
- [ ] Vídeo entre 10 e 15 minutos
