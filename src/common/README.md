# Código Compartilhado

Esta pasta concentra utilitários simples reutilizados entre os exercícios.

## Arquivos

- `paths.py`: caminhos padrão do repositório.
- `inputs.py`: download ou cópia de arquivos de entrada para cada exercício.
- `image_io.py`: leitura e escrita de imagens PNG.
- `runner.py`: fluxo comum para preparar entradas, executar o processamento e registrar saídas.

## Ideia

Cada exercício define:

- quais entradas ele precisa;
- a função de processamento;
- como salvar suas saídas.

O restante fica centralizado aqui para evitar duplicação.
