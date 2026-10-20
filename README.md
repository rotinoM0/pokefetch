# pokefetch

Wrapper de shell: mostra um sprite do [`pokeget`](https://github.com/talwat/pokeget) ao lado da
saída do `fastfetch`, usando o `config.jsonc` que você já tem.

Não é um substituto do fastfetch e não desenha caixa própria — quem monta a caixa é o
`~/.config/fastfetch/config.jsonc`. O `pokefetch` só resolve o logo:

```bash
fastfetch --file-raw <(pokeget random --hide-name)
```

## Requisitos

- `bash` 4+
- `fastfetch` com `--file-raw` (testado na **2.70.0**)
- `pokeget` no `PATH` (testado na **1.6.7**)
- Uma fonte **Nerd Font** no terminal, para os ícones do `config.jsonc` aparecerem
  (o Alacritty não faz fallback de glifos; o VS Code precisa de
  `"terminal.integrated.fontFamily": "JetBrainsMono Nerd Font"`)

## Instalação

```bash
# no ~/.zshrc
export PATH="$HOME/Documentos/projetos/pokefetch:$PATH"
```

## Uso

```
pokefetch [pokemon|random] [opções] [flags do fastfetch] [-- flags do fastfetch]
```

| Opção | Efeito |
|---|---|
| `-p, --pokemon NOME` | Pokémon a exibir (padrão: `random`); também aceita posicional |
| `-s, --shiny` | Versão shiny |
| `-m, --mega` (`--mega-x`, `--mega-y`) | Versão mega |
| `-a, --alolan` / `-g, --gmax` | Formas alolan / gigantamax |
| `--hisui` / `-n, --noble` / `--galar` / `--female` | Outras formas |
| `-f, --form FORMA` | Forma específica, repassada ao pokeget |
| `--no-logo` | Só a caixa do fastfetch, sem sprite |
| `--no-color` | Remove todas as sequências ANSI da saída |
| `-h, --help` | Ajuda |
| `-V, --version` | Versões de pokefetch, fastfetch e pokeget |

Qualquer flag desconhecida é repassada para o `fastfetch` (`--logo-position top`,
`--structure kernel:shell`, etc.). Depois da primeira flag do fastfetch, os argumentos
seguintes também vão para ele — por isso passe o Pokémon antes
(`pokefetch pikachu --logo-position top`) ou use `-p`.

## Exemplos

```bash
pokefetch                       # aleatório
pokefetch pikachu               # pelo nome (posicional)
pokefetch -p gengar -s          # shiny
pokefetch -p charizard --mega-x # mega X (ou -f mega-x)
pokefetch --no-logo --no-color  # só a caixa, sem cor
pokefetch --logo-position top   # sprite acima da caixa
```

O `-f/--form` repassa o sufixo usado nos sprites do pokeget: `mega-x`, `mega-y`, `alola`,
`galar`, `gmax`, `hisui`. Valores inexistentes para aquele Pokémon retornam
`pokemon not found`.

## Como funciona

- O sprite é gerado pelo `pokeget --hide-name`, capturado em variável e entregue ao
  fastfetch por process substitution (`--file-raw <(...)`).
- `--file-raw` (e não `--raw`): no fastfetch 2.70 o `--raw` **empilha** o logo acima das
  informações; o `--file-raw` renderiza **ao lado**, que é o objetivo aqui.
- As cores truecolor do pokeget (half-blocks `▄` com `38;2;…`/`48;2;…`) são preservadas
  pelo `--file-raw`.
- `--logo-padding-right 2` evita que o sprite cole na borda da caixa.
- O fastfetch alinha o logo com o primeiro módulo. Se o `config.jsonc` começar com um
  módulo `break`, a caixa desce uma linha; use `--logo-padding-top 1` para compensar.

## Limitações conhecidas

- **`-s` é shiny**, não `--structure`. Para usar o `-s` do fastfetch:
  `pokefetch -- -s kernel:shell`.
- **Ícones**: dependem de Nerd Font no terminal. Os 12 glifos usados no `config.jsonc`
  foram conferidos contra o cmap de `JetBrainsMonoNerdFont-Regular.ttf` (todos presentes e
  com avanço de 1 célula).
- **`--no-color`**: a saída passa por pipe, então o fastfetch deixa de detectar a largura
  do terminal e pode empilhar o sprite. Use para redirecionar para arquivo
  (`pokefetch --no-color > out.txt`), não para uso interativo.
- **Largura**: se sprite + caixa não couberem no terminal, o fastfetch coloca o sprite
  acima. Sprite (≈21-31 colunas) + caixa (38) + padding (2) cabem em 80 colunas.

## Config do fastfetch (caixa de 38 colunas)

O layout fica em `~/.config/fastfetch/config.jsonc`, gerado por `gen_config.py`:

```bash
python3 ~/Documentos/projetos/pokefetch/gen_config.py   # reescreve o config.jsonc
```

O gerador calcula o padding exato de cada linha (largura total 38, rótulo 9, valor 22) e
usa as constantes de cor do `display.constants`. Para mexer no visual:

| Onde | O que muda |
|---|---|
| `W` | largura total da caixa |
| `LABEL_W` / `VALUE_W` | coluna dos rótulos / dos valores |
| `BORDER`, `BLUE`, `GREEN`, `PEACH` | cores da moldura, seções sistema/hardware/ambiente |
| `I_*` | ícones (precisam existir na Nerd Font) |

Atenção ao escrever ícones em Python: `\uXXXX` aceita só 4 dígitos. Para code points
acima de U+FFFF use `\U000XXXXX` — foi assim que `\uf08e6` virou dois caracteres
(`U+F08E` + `6`) e desalinhou duas linhas.

O título (`usuário@host`) é gerado por um módulo `command`, então acompanha mudanças de
usuário/host sem quebrar a moldura.

## Ambiente testado

Arch Linux, `fastfetch 2.70.0`, `pokeget 1.6.7`, Alacritty 0.17 (fonte
`JetBrainsMono Nerd Font`), zsh.
