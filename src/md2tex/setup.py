from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys


def check_dependencies() -> dict[str, dict[str, str | bool]]:
    """Verifica a presença das ferramentas no sistema."""
    pandoc_path = shutil.which("pandoc")
    latex_path = shutil.which("xelatex") or shutil.which("pdflatex") or shutil.which("lualatex")
    mermaid_path = shutil.which("mmdc")

    return {
        "pandoc": {
            "name": "Pandoc (Conversor AST)",
            "installed": pandoc_path is not None,
            "path": pandoc_path or "Não encontrado",
            "required": True,
        },
        "latex": {
            "name": "Motor LaTeX (xelatex/pdflatex)",
            "installed": latex_path is not None,
            "path": latex_path or "Não encontrado",
            "required": False,
            "description": "Necessário apenas para compilar PDFs via --pdf",
        },
        "mermaid": {
            "name": "Mermaid CLI (mmdc)",
            "installed": mermaid_path is not None,
            "path": mermaid_path or "Não encontrado",
            "required": False,
            "description": "Necessário apenas para renderizar diagramas ```mermaid",
        },
    }


def print_dependency_report() -> None:
    """Imprime relatório amigável das dependências no terminal."""
    deps = check_dependencies()
    print("\n🔍 Relatório de Dependências do md2tex:\n" + "-" * 50)
    for key, info in deps.items():
        status = "✓ [OK]" if info["installed"] else "✗ [AUSENTE]"
        req = "Obrigatório" if info["required"] else "Opcional"
        print(f"{status:13} {info['name']} ({req})")
        if info["installed"]:
            print(f"              Caminho: {info['path']}")
        else:
            print(f"              Nota: {info.get('description', 'Necessário para funcionamento')}")
    print("-" * 50 + "\n")


def install_tinytex() -> bool:
    """Baixa e instala o TinyTeX automaticamente."""
    system = platform.system().lower()
    print("⏳ Iniciando download e instalação do TinyTeX (distribuição leve do TeX)...")
    try:
        if system in ["linux", "darwin"]:
            cmd = "wget -qO- 'https://yihui.org/tinytex/install-unx.sh' | sh"
            subprocess.run(cmd, shell=True, check=True)
        elif system == "windows":
            cmd = "powershell -Command \"iwr -useb https://yihui.org/tinytex/install-binzip.ps1 | iex\""
            subprocess.run(cmd, shell=True, check=True)
        else:
            print(f"Sistema {system} não suportado para instalação automática do TinyTeX.")
            return False
        print("✅ TinyTeX instalado com sucesso!")
        return True
    except Exception as exc:
        print(f"❌ Falha ao instalar TinyTeX: {exc}")
        return False


def install_mermaid() -> bool:
    """Instala o Mermaid CLI via npm."""
    npm_path = shutil.which("npm")
    if not npm_path:
        print("❌ Node.js/npm não encontrado no sistema. Por favor, instale o Node.js primeiro.")
        return False

    print("⏳ Instalando @mermaid-js/mermaid-cli globalmente via npm...")
    try:
        subprocess.run([npm_path, "install", "-g", "@mermaid-js/mermaid-cli"], check=True)
        print("✅ Mermaid CLI instalado com sucesso!")
        return True
    except Exception as exc:
        print(f"❌ Falha ao instalar Mermaid CLI: {exc}")
        return False


def run_interactive_setup() -> None:
    """Executa o wizard interativo de setup e verificação de dependências."""
    print_dependency_report()
    deps = check_dependencies()

    # Checa TeX
    if not deps["latex"]["installed"]:
        response = input("👉 O motor LaTeX não foi encontrado. Deseja baixar e instalar o TinyTeX agora? [S/n]: ").strip().lower()
        if response in ["s", "sim", "y", "yes", ""]:
            install_tinytex()

    # Checa Mermaid
    if not deps["mermaid"]["installed"]:
        response = input("👉 O Mermaid CLI (mmdc) não foi encontrado. Deseja instalar via npm agora? [S/n]: ").strip().lower()
        if response in ["s", "sim", "y", "yes", ""]:
            install_mermaid()

    print("\n✨ Setup de dependências concluído!")
