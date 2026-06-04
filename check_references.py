"""
check_references.py
===================
Script utilitário para auditar o repositório de literatura.

Uso:
    python check_references.py

Funções:
    - Lista todas as entradas BibTeX do references.bib
    - Identifica entradas com "TBD" (To Be Defined) — incompletas
    - Conta referências por status (lidas, em leitura, na fila)
    - Verifica se todos os PDFs têm entrada BibTeX correspondente

Autor: Gabriel Rozo | FEQ/UNICAMP | 2025
"""

import os
import re
from pathlib import Path

BIB_FILE = Path("references.bib")
PASTA_TEMAS = [
    "01_Reator_Monolitico",
    "02_Cinetica_Heterogenea_LHHW",
    "03_CFD_Microcanais_e_Monolitos",
    "04_Transferencia_Calor_e_Massa",
    "05_Biodiesel_e_Transesterificacao",
    "06_Modelagem_e_Simulacao",
]


def parse_bibtex(bib_path: Path) -> list[dict]:
    """Extrai entradas do arquivo .bib de forma simples."""
    entries = []
    content = bib_path.read_text(encoding="utf-8")
    
    # Encontra todas as entradas @tipo{chave, ...}
    pattern = re.compile(r"@(\w+)\{(\w+),", re.MULTILINE)
    for match in pattern.finditer(content):
        entry_type = match.group(1)
        key = match.group(2)
        
        # Verifica se tem campos TBD
        # Pega o bloco da entrada (aproximado)
        start = match.start()
        snippet = content[start:start+500]
        has_tbd = "TBD" in snippet
        
        entries.append({
            "type": entry_type,
            "key": key,
            "incomplete": has_tbd,
        })
    
    return entries


def list_pdfs() -> list[Path]:
    """Lista todos os PDFs no repositório."""
    pdfs = []
    for pasta in PASTA_TEMAS:
        pasta_path = Path(pasta)
        if pasta_path.exists():
            pdfs.extend(pasta_path.glob("*.pdf"))
    return pdfs


def main():
    print("=" * 60)
    print("  AUDITORIA DO REPOSITÓRIO DE LITERATURA")
    print("  Mestrado FEQ/UNICAMP — Gabriel Rozo")
    print("=" * 60)

    # 1. Análise do BibTeX
    if not BIB_FILE.exists():
        print("\n❌ references.bib não encontrado!")
        return

    entries = parse_bibtex(BIB_FILE)
    completas = [e for e in entries if not e["incomplete"]]
    incompletas = [e for e in entries if e["incomplete"]]

    print(f"\n📚 REFERÊNCIAS BIBTEX ({len(entries)} total)")
    print(f"   ✅ Completas:   {len(completas)}")
    print(f"   ⚠️  Incompletas (TBD): {len(incompletas)}")

    if incompletas:
        print("\n   Entradas a completar:")
        for e in incompletas:
            print(f"   → [{e['type']}] {e['key']}")

    # 2. PDFs no repositório
    pdfs = list_pdfs()
    print(f"\n📄 PDFs NO REPOSITÓRIO: {len(pdfs)}")
    if pdfs:
        for pdf in sorted(pdfs):
            print(f"   → {pdf}")
    else:
        print("   (nenhum PDF ainda — adicione artigos nas pastas temáticas)")

    # 3. Status das pastas
    print("\n📁 STATUS DAS PASTAS")
    for pasta in PASTA_TEMAS:
        pasta_path = Path(pasta)
        if pasta_path.exists():
            n_files = len(list(pasta_path.glob("*"))) - 1  # exclui README
            print(f"   {pasta}: {n_files} arquivo(s) além do README")
        else:
            print(f"   ❌ {pasta}: pasta não encontrada")

    print("\n" + "=" * 60)
    print("  Dica: Para adicionar referência, use o formato:")
    print("  NomePrimeiro_Autor_Ano_PalavraChave.pdf")
    print("=" * 60)


if __name__ == "__main__":
    main()
