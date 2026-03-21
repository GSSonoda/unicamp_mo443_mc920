# Trabalho 1 - MC920 / MO443

Este repositório contém o Trabalho 1 de Introdução ao Processamento Digital de Imagens.

O projeto foi organizado para suportar vários exercícios com a mesma estrutura de código, entradas, saídas e relatório.

No momento, apenas o exercício 1 está implementado, mas a organização abaixo vale para os demais.

## 1. Montar o ambiente

Use os comandos abaixo na raiz do repositório:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

Se você já tiver um ambiente virtual ativo, basta instalar o `requirements.txt`.

## 2. Executar os exercícios

Para executar um exercício específico:

```bash
python main.py NUMERO_DO_EXERCICIO
```

Para executar tudo que já está implementado no repositório:

```bash
python run_all.py
```

Hoje, esse comando executa apenas o exercício 1.

Se quiser refazer os arquivos gerados, use:

```bash
python main.py NUMERO_DO_EXERCICIO --overwrite
```

## 3. Onde estão os arquivos

- Entradas locais de cada exercício: `data/input/exercicio_XX/`
- Resultados locais de cada exercício: `results/exercicio_XX/`
- Figuras usadas no relatório: `docs/relatorio/figuras/exercicio_XX/`
- Relatório pronto em PDF: `docs/relatorio/relatorio.pdf`
- Fonte do relatório em LaTeX: `docs/relatorio/relatorio.tex`

As pastas `data/input/` e `results/` são geradas localmente durante a execução e não ficam versionadas no Git.

As figuras copiadas para `docs/relatorio/figuras/` são mantidas no repositório porque fazem parte do material usado pelo LaTeX.

## 4. Relatório

O PDF já está pronto em:

```text
docs/relatorio/relatorio.pdf
```

Se quiser apenas consultar o trabalho, esse é o arquivo principal.

## 5. Gerar o relatório novamente (opcional)

Se quiser atualizar o PDF a partir do LaTeX:

```bash
python build_report.py
```

Esse passo é opcional. Ele só é necessário se você alterar `docs/relatorio/relatorio.tex` e quiser gerar um novo PDF.

Para esse comando funcionar, o sistema precisa ter LaTeX com `latexmk` instalado.

## 6. Observação sobre implementação atual

Atualmente, o exercício 1 é o único exercício implementado no código.
