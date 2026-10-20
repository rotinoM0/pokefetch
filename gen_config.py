#!/usr/bin/env python3
"""Gera ~/.config/fastfetch/config.jsonc (box de 38 colunas) — pokefetch."""
import json, os, sys

# ---- paleta (256 cores) ----
BORDER = "\x1b[38;5;240m"   # $1 molduras
BLUE   = "\x1b[38;5;111m"   # $2 sistema
LABEL  = "\x1b[38;5;245m"   # $3 rotulos
MAUVE  = "\x1b[38;5;183m"   # $4 titulo (usuario)
GREEN  = "\x1b[38;5;114m"   # $5 hardware
PEACH  = "\x1b[38;5;216m"   # $6 ambiente
RESET  = "\x1b[0m"          # $7 reset
VALUE_HEX = "38;5;252"      # cor dos valores (display.color.output)

# ---- icones: todos presentes em JetBrainsMono Nerd Font, advance 1 celula ----
I_ARCH, I_KERNEL, I_CLOCK = "\uf303", "\uf31a", "\uf017"
I_CPU, I_GPU, I_MEM       = "\uf2db", "\U000f08e6", "\U000f035b"
I_DISK, I_WM, I_SHELL     = "\uf0a0", "\uf2d0", "\uf121"
I_TERM, I_PKGS, I_NET     = "\uf120", "\uf1b2", "\uf0ac"

W        = 38     # largura total do box
LABEL_W  = 9
VALUE_W  = 22     # 1 + 1 + 1 + 9 + 1 + 22 + 1 + 1 = 38
INNER    = W - 2  # 36 colunas entre as duas bordas

C1, C2, C3, C4, C5, C6, C7 = (f"{{${i}}}" for i in range(1, 8))


def build_section(name):
    # ├ ─ ' ' name ' ' ─… ┤  -> W
    dashes = W - 5 - len(name)
    return f"{C1}├─{C3} {name} {C1}" + "─" * dashes + "┤"


def data_row(icon, label, accent, mod):
    key = f"{C1}│ {accent}{icon}{C3} {label:<{LABEL_W}} "
    return {"type": mod["type"], "key": key,
            "format": f"{{{mod['field']}<{VALUE_W}}}{C1} │", **mod.get("extra", {})}


def cmd_row(icon, label, accent, text):
    key = f"{C1}│ {accent}{icon}{C3} {label:<{LABEL_W}} "
    return {"type": "command", "key": key, "text": text,
            "format": f"{{<{VALUE_W}}}{C1} │"}


title_cmd = (
    "H=$(hostname); "
    f"printf '{BORDER}│ {MAUVE}%s{BORDER}@{BLUE}%s{RESET}"
    f"%*s{BORDER}│' \"$USER\" \"$H\" $(( {W} - 4 - ${{#USER}} - ${{#H}} )) ''"
)

modules = [
    {"type": "custom", "key": f"{C1}╭" + "─" * INNER + "╮"},
    {"type": "command", "key": " ", "text": title_cmd},
    {"type": "custom", "key": build_section("sistema")},
    data_row(I_ARCH,   "distro", BLUE, {"type": "os",     "field": "pretty-name"}),
    data_row(I_KERNEL, "kernel", BLUE, {"type": "kernel", "field": "release"}),
    cmd_row(I_CLOCK, "uptime", BLUE,
            "awk '{printf \"%dh %dm\", $1/3600, ($1%3600)/60}' /proc/uptime"),
    {"type": "custom", "key": build_section("hardware")},
    data_row(I_CPU, "cpu", GREEN, {"type": "cpu", "field": "name"}),
    data_row(I_GPU, "gpu", GREEN, {"type": "gpu", "field": "name"}),
    cmd_row(I_MEM, "memory", GREEN,
            "free -b | awk 'NR==2{printf \"%.2f / %.2f GiB\", $3/1073741824, $2/1073741824}'"),
    cmd_row(I_DISK, "disk", GREEN, "df -h / | awk 'NR==2{print $3\" / \"$2}'"),
    {"type": "custom", "key": build_section("ambiente")},
    data_row(I_WM,    "wm",       PEACH, {"type": "wm",       "field": "pretty-name"}),
    data_row(I_SHELL, "shell",    PEACH, {"type": "shell",    "field": "pretty-name"}),
    data_row(I_TERM,  "terminal", PEACH, {"type": "terminal", "field": "pretty-name"}),
    data_row(I_PKGS,  "pkgs",     PEACH, {"type": "packages", "field": "all"}),
    cmd_row(I_NET, "ip", PEACH,
            "ip -4 -o addr show scope global 2>/dev/null | awk '{print $4}' | cut -d/ -f1 | head -1"),
    {"type": "custom", "key": f"{C1}╰" + "─" * INNER + "╯"},
    "break",
]

cfg = {
    "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/master/doc/json_schema.json",
    "logo": "none",
    "display": {
        "separator": "",
        "color": {"keys": "white", "output": VALUE_HEX},
        "constants": [BORDER, BLUE, LABEL, MAUVE, GREEN, PEACH, RESET],
    },
    "modules": modules,
}

out = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/.config/fastfetch/config.jsonc")
with open(out, "w", encoding="utf-8") as f:
    f.write("// gerado por gen_config.py (pokefetch)\n")
    json.dump(cfg, f, indent=4, ensure_ascii=False)
    f.write("\n")
print(f"escrito: {out} | largura alvo: {W}")
