# -*- coding: utf-8 -*-

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DADOS_FILE = BASE_DIR / "dados_curriculo.json"
README_FILE = BASE_DIR / "README.md"


def carregar_dados():
    """Carrega e valida os dados do currículo."""
    if not DADOS_FILE.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {DADOS_FILE}"
        )

    with DADOS_FILE.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    if not isinstance(dados, dict):
        raise ValueError(
            "dados_curriculo.json deve conter um objeto JSON."
        )

    return dados


def lista_texto(itens):
    """Transforma uma lista em texto separado por vírgulas."""
    if not itens:
        return "—"

    return ", ".join(str(item).strip() for item in itens if str(item).strip())


def gerar_readme(dados):
    """Gera o conteúdo completo do README.md."""

    nome = dados.get("nome", "Nome")
    cargo = dados.get("cargo", "")
    objetivo = dados.get("objetivo", "")
    sobre = dados.get("sobre", "")

    contato = dados.get("contato", {})
    competencias = dados.get("competencias", {})
    educacao = dados.get("educacao", [])
    experiencia = dados.get("experiencia", [])
    certificados = dados.get("certificados", [])

    email = contato.get("email", "")
    cidade = contato.get("cidade", "")
    linkedin = contato.get("linkedin", "")
    github = contato.get("github", "")
    site = contato.get("site", "")
    certificados_link = contato.get("certificados", "")

    front_end = competencias.get("front_end", [])
    back_end_dados = competencias.get("back_end_dados", [])
    ia_aplicada = competencias.get("ia_aplicada", [])
    ferramentas = competencias.get("ferramentas", [])

    linhas = []

    # ---------------------------------------------------------
    # CABEÇALHO
    # ---------------------------------------------------------

    linhas.append(f"# {nome}")
    linhas.append("")

    if cargo:
        linhas.append(f"**{cargo}**")
        linhas.append("")

    links = []

    if linkedin:
        links.append(f"[LinkedIn]({linkedin})")

    if github:
        links.append(f"[GitHub]({github})")

    if site:
        links.append(f"[Portfólio]({site})")

    if email:
        links.append(f"[E-mail](mailto:{email})")

    if links:
        linhas.append(" · ".join(links))
        linhas.append("")

    linhas.append(
        "[![Currículo PDF](https://img.shields.io/badge/Curr%C3%ADculo-PDF-red?style=for-the-badge&logo=adobe-acrobat-reader&logoColor=white)](./curriculo_fabiano.pdf)"
    )
    linhas.append("")

    # ---------------------------------------------------------
    # SOBRE
    # ---------------------------------------------------------

    linhas.append("## Sobre")
    linhas.append("")

    if sobre:
        linhas.append(sobre)
        linhas.append("")

    # ---------------------------------------------------------
    # OBJETIVO
    # ---------------------------------------------------------

    if objetivo:
        linhas.append("## Objetivo")
        linhas.append("")
        linhas.append(objetivo)
        linhas.append("")

    # ---------------------------------------------------------
    # COMPETÊNCIAS
    # ---------------------------------------------------------

    linhas.append("## Competências Técnicas")
    linhas.append("")

    linhas.append(
        f"- **Front-end:** {lista_texto(front_end)}"
    )

    linhas.append(
        f"- **Back-end e Dados:** {lista_texto(back_end_dados)}"
    )

    linhas.append(
        f"- **IA Aplicada:** {lista_texto(ia_aplicada)}"
    )

    linhas.append(
        f"- **Ferramentas:** {lista_texto(ferramentas)}"
    )

    linhas.append("")

    # ---------------------------------------------------------
    # EXPERIÊNCIA
    # ---------------------------------------------------------

    linhas.append("## Experiência Profissional")
    linhas.append("")

    if experiencia:
        for item in experiencia:
            empresa = item.get("empresa", "")
            cargo_exp = item.get("cargo", "")
            periodo = item.get("periodo", "")
            resumo = item.get("resumo", "")

            if empresa:
                linhas.append(f"### {empresa}")
                linhas.append("")

            if cargo_exp:
                linhas.append(f"**{cargo_exp}**")

            if periodo:
                linhas.append(f"*{periodo}*")

            linhas.append("")

            if resumo:
                linhas.append(resumo)
                linhas.append("")
    else:
        linhas.append("Experiência profissional detalhada no currículo PDF.")
        linhas.append("")

    # ---------------------------------------------------------
    # FORMAÇÃO
    # ---------------------------------------------------------

    linhas.append("## Formação Acadêmica")
    linhas.append("")

    if educacao:
        for item in educacao:
            curso = item.get("curso", "")
            instituicao = item.get("instituicao", "")
            periodo = item.get("periodo", "")

            if curso:
                linhas.append(f"### {curso}")

            if instituicao:
                linhas.append(f"**{instituicao}**")

            if periodo:
                linhas.append(f"*{periodo}*")

            linhas.append("")
    else:
        linhas.append("Informações acadêmicas disponíveis no currículo PDF.")
        linhas.append("")

    # ---------------------------------------------------------
    # CERTIFICADOS
    # ---------------------------------------------------------

    linhas.append("## Certificados e Cursos")
    linhas.append("")

    if certificados_link:
        linhas.append(
            f"[📁 Acessar certificados e cursos no Google Drive]({certificados_link})"
        )
        linhas.append("")

    if certificados:
        for cert in certificados:
            nome_cert = cert.get("nome", "")
            instituicao = cert.get("instituicao", "")
            ano = cert.get("ano", "")

            partes = []

            if nome_cert:
                partes.append(f"**{nome_cert}**")

            if instituicao:
                partes.append(instituicao)

            if ano:
                partes.append(ano)

            if partes:
                linhas.append("- " + " — ".join(partes))

        linhas.append("")

    # ---------------------------------------------------------
    # CONTATO
    # ---------------------------------------------------------

    linhas.append("## Contato")
    linhas.append("")

    if cidade:
        linhas.append(f"- 📍 {cidade}")

    if email:
        linhas.append(f"- ✉️ [E-mail](mailto:{email})")

    if linkedin:
        linhas.append(f"- 🔗 [LinkedIn]({linkedin})")

    if github:
        linhas.append(f"- 💻 [GitHub]({github})")

    if site:
        linhas.append(f"- 🌐 [Portfólio]({site})")

    linhas.append("")

    linhas.append("---")
    linhas.append("")
    linhas.append(
        "*README gerado automaticamente a partir de `dados_curriculo.json`.*"
    )
    linhas.append("")

    return "\n".join(linhas)


def salvar_readme(conteudo):
    """Salva o README.md."""
    with README_FILE.open("w", encoding="utf-8", newline="\n") as arquivo:
        arquivo.write(conteudo)


def main():
    dados = carregar_dados()
    conteudo = gerar_readme(dados)
    salvar_readme(conteudo)

    print("README.md atualizado com sucesso.")


if __name__ == "__main__":
    main()
