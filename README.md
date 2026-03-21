# Trabalho 1 - MC920 / MO443

Este repositório contém o Trabalho 1 de Introdução ao Processamento Digital de Imagens.

No momento, apenas o exercício 1 está implementado.

## 1. Montar o ambiente

Use os comandos abaixo na raiz do repositório:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

Se você já tiver um ambiente virtual ativo, basta instalar o `requirements.txt`.

## 2. Executar

Para executar o exercício 1:

```bash
python main.py 1
```

Para executar tudo que já está implementado no repositório:

```bash
python run_all.py
```

Hoje, esse comando executa apenas o exercício 1.

Se quiser refazer os arquivos gerados, use:

```bash
python main.py 1 --overwrite
```

## 3. Onde estão os arquivos

- Entrada do exercício 1: `data/input/exercicio_01/baboon_monocromatica.png`
- Resultados do exercício 1: `results/exercicio_01/`
- Figuras usadas no relatório: `docs/relatorio/figuras/exercicio_01/`
- Relatório pronto em PDF: `docs/relatorio/relatorio.pdf`
- Fonte do relatório em LaTeX: `docs/relatorio/relatorio.tex`

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
