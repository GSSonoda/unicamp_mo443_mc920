# MC920 / MO443 — Introdução ao Processamento Digital de Imagens

Este repositório contém os Trabalhos 1, 2 e 3 da disciplina.

## 1. Montar o ambiente

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Requer Python 3.10+ e, para gerar PDFs, LaTeX com `latexmk`.

---

## 2. Executar um item específico

```bash
# Trabalho 1 — exercícios 1 a 13 (padrão)
python3 main.py NUMERO

# Trabalho 2 — métodos 1 a 12
python3 main.py NUMERO --trabalho 2

# Trabalho 3 — análises 1 e 2
python3 main.py NUMERO --trabalho 3
```

Para refazer arquivos já gerados, adicione `--overwrite`.

---

## 3. Executar tudo

```bash
python3 run_all.py                # todos os trabalhos (1, 2 e 3)
python3 run_all.py --trabalho 1   # só o trabalho 1
python3 run_all.py --trabalho 2   # só o trabalho 2
python3 run_all.py --trabalho 3   # só o trabalho 3
```

---

## 4. Benchmarks

```bash
# Trabalho 1 — exercício N
python3 benchmark.py N --repeats 30 --warmup 3

# Trabalho 2 — método N
python3 benchmark.py N --trabalho 2 --repeats 30 --warmup 3

# Trabalho 3 — análise N
python3 benchmark.py N --trabalho 3 --repeats 10 --warmup 2
```

Os resultados são salvos em `results/benchmarks/`.

---

## 5. Relatório (PDF)

Gerar o PDF de um trabalho:

```bash
python3 build_report.py --report 1   # trabalho 1
python3 build_report.py --report 2   # trabalho 2
python3 build_report.py --report 3   # trabalho 3
```

Atualizar as figuras a partir dos resultados locais antes de compilar:

```bash
python3 build_report.py --report 1 --sync-figures
python3 build_report.py --report 2 --sync-figures
python3 build_report.py --report 3 --sync-figures
```

> As figuras são copiadas de `results/` para `docs/relatorio_0X/figuras/` pelo `--sync-figures`.
> Rode os exercícios primeiro; depois use `--sync-figures` para preparar o relatório.

---

## 6. Fluxo completo (do zero ao PDF)

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Rodar todos os exercícios (baixa entradas e gera saídas)
python3 run_all.py --trabalho 1
python3 run_all.py --trabalho 2
python3 run_all.py --trabalho 3

# 3. Gerar os PDFs
python3 build_report.py --report 1 --sync-figures
python3 build_report.py --report 2 --sync-figures
python3 build_report.py --report 3 --sync-figures
```

---

## 7. Estrutura de pastas

```
src/
├── common/               # utilitários compartilhados (I/O, paths, runner, benchmark)
├── trabalho_01/          # exercicio_01 … exercicio_13
├── trabalho_02/
│   ├── secao_01/         # metodo_01_global … metodo_09_mediana  (limiarização)
│   └── secao_02/         # metodo_10_pixels … metodo_12_histogramas  (transições em vídeo)
└── trabalho_03/
    ├── analise_01_espectro_histograma/   # FFT + espectro log + histograma angular
    └── analise_02_invariancia/           # invariância sob translação/rotação/escala

docs/
├── relatorio_01/         # LaTeX + PDF do trabalho 1
├── relatorio_02/         # LaTeX + PDF do trabalho 2
└── relatorio_03/         # LaTeX + PDF do trabalho 3

data/input/               # entradas baixadas na primeira execução (não versionadas)
results/                  # saídas geradas na execução (não versionadas)
```

Cada módulo `main.py` expõe três funções públicas:

| Função | O que faz |
|---|---|
| `run(overwrite)` | Baixa entradas e gera as saídas |
| `report_files()` | Retorna os caminhos das figuras para o relatório |
| `run_benchmarks(repeats, warmup, overwrite_inputs)` | Mede tempos e salva JSON em `results/benchmarks/` |
