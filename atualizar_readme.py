import json

def gerar_readme():
    with open('dados_curriculo.json', 'r', encoding='utf-8') as f:
        dados = json.load(f)

    badges = {
        "HTML": "[![HTML](https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white)]",
        "CSS": "[![CSS](https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white)]",
        "JavaScript": "[![JavaScript](https://img.shields.io/badge/javascript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)]",
        "Python": "[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)]",
        "SQL": "[![SQL](https://img.shields.io/badge/SQL-025E8C?style=for-the-badge&logo=postgresql&logoColor=white)]",
        "Git & GitHub": "[![Git](https://img.shields.io/badge/git-121013?style=for-the-badge&logo=git&logoColor=white)]",
        "Linux": "[![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)]"
    }

    nome = dados.get('nome', 'Nome')
    cargo = dados.get('cargo', '')
    foco = dados.get('foco', '')
    sobre = dados.get('sobre', '')
    contato = dados.get('contato', {})
    competencias = dados.get('competencias', {})
    projetos = dados.get('projetos', [])
    experiencia = dados.get('experiencia', [])

    linguagens = competencias.get('linguagens', [])
    banco_de_dados = competencias.get('banco_de_dados', [])
    ferramentas = competencias.get('ferramentas', [])
    sistemas = competencias.get('sistemas', [])

    # Monta badges de linguagens disponíveis
    badges_tecnicas = ' '.join([badges.get(t, f"({t})") for t in linguagens])

    conteudo = ""
    conteudo += f"# {nome}\n\n"
    if cargo:
        conteudo += f"**{cargo}**  \n"
    if foco:
        conteudo += f"{foco}\n\n"

    conteudo += "[![Baixar PDF](https://img.shields.io/badge/Download-Curr%C3%ADculo_PDF-red?style=for-the-badge&logo=adobe-acrobat-reader&logoColor=white)](./curriculo_fabiano.pdf)\n\n"

    conteudo += "## Sobre\n"
    conteudo += f"{sobre}\n\n"

    conteudo += "## Competências Técnicas\n\n"
    conteudo += f"{badges_tecnicas}\n\n"

    conteudo += f"- **Linguagens:** {', '.join(linguagens) if linguagens else '—'}\n"
    conteudo += f"- **Banco de Dados:** {', '.join(banco_de_dados) if banco_de_dados else '—'}\n"
    conteudo += f"- **Ferramentas:** {', '.join(ferramentas) if ferramentas else '—'}\n"
    conteudo += f"- **Sistemas:** {', '.join(sistemas) if sistemas else '—'}\n\n"

    conteudo += "## Projetos\n\n"
    if projetos:
        for proj in projetos:
            nome_proj = proj.get('nome', 'Projeto')
            descricao = proj.get('descricao', '')
            conteudo += f"### {nome_proj}\n"
            conteudo += f"{descricao}\n\n"
    else:
        conteudo += "Projetos listados no repositório GitHub.\n\n"

    conteudo += "## Experiência Profissional\n\n"
    if experiencia:
        for exp in experiencia:
            empresa = exp.get('empresa', '')
            cargo_exp = exp.get('cargo', '')
            periodo = exp.get('periodo', '')
            resumo = exp.get('resumo', '')
            conteudo += f"### {empresa}\n"
            conteudo += f"**{cargo_exp}**  \n"
            conteudo += f"{periodo}  \n"
            conteudo += f"{resumo}\n\n"
    else:
        conteudo += "Experiência profissional detalhada no PDF.\n\n"

    conteudo += "## Contato\n\n"
    cidade = contato.get('cidade', '')
    email = contato.get('email', '')
    linkedin = contato.get('linkedin', '')
    github = contato.get('github', '')

    conteudo += f"- 📍 {cidade}\n" if cidade else ""
    conteudo += f"- ✉️ {email}\n" if email else ""
    conteudo += f"- 🔗 [LinkedIn]({linkedin})\n" if linkedin else ""
    conteudo += f"- 💻 [GitHub]({github})\n" if github else ""

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(conteudo)
    print("README.md atualizado com sucesso.")

if __name__ == "__main__":
    gerar_readme()
