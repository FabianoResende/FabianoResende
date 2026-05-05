import json

def gerar_readme():
    with open('dados_curriculo.json', 'r', encoding='utf-8') as f:
        dados = json.load(f)

    badges = {
        "Python": "[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)]",
        "SQL": "[![SQL](https://img.shields.io/badge/SQL-025E8C?style=for-the-badge&logo=postgresql&logoColor=white)]",
        "JavaScript": "[![JavaScript](https://img.shields.io/badge/javascript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)]",
        "Git & GitHub": "[![Git](https://img.shields.io/badge/git-121013?style=for-the-badge&logo=git&logoColor=white)]",
        "Linux": "[![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)]"
    }

    # Monta as badges de Linguagens (se não tiver badge, mostra o texto entre parênteses)
    linguagens = dados["competencias"]["linguagens"]
    badges_tecnicas = ' '.join([badges.get(t, f"({t})") for t in linguagens])

    conteudo = ""

    # Cabeçalho
    conteudo += f"# {dados['nome']}\n\n"
    conteudo += f"**{dados['cargo']}**  \n"
    conteudo += f"{dados['foco']}\n\n"

    conteudo += "[![Baixar PDF](https://img.shields.io/badge/Download-Currículo_PDF-red?style=for-the-badge&logo=adobe-acrobat-reader&logoColor=white)](https://github.com/FabianoResende/FabianoResende/blob/main/curriculo_fabiano.pdf)\n\n"

    # Sobre
    conteudo += f"## Sobre\n"
    conteudo += f"{dados['sobre']}\n\n"

    # Competências Técnicas
    conteudo += "## Competências Técnicas\n\n"
    conteudo += f"{badges_tecnicas}\n\n"

    comp = dados["competencias"]
    conteudo += f"- **Linguagens:** {', '.join(comp['linguagens'])}\n"
    conteudo += f"- **Banco de Dados:** {', '.join(comp['banco_de_dados'])}\n"
    conteudo += f"- **Ferramentas:** {', '.join(comp['ferramentas'])}\n"
    conteudo += f"- **Sistemas:** {', '.join(comp['sistemas'])}\n\n"

    # Projetos
    conteudo += "## Projetos\n\n"
    for proj in dados["projetos"]:
        conteudo += f"### {proj['nome']}\n"
        conteudo += f"{proj['descricao']}\n\n"

    # Experiência
    conteudo += "## Experiência Profissional\n\n"
    for exp in dados["experiencia"]:
        conteudo += f"### {exp['empresa']}\n"
        conteudo += f"**{exp['cargo']}**  \n"
        conteudo += f"{exp['periodo']}  \n"
        conteudo += f"{exp['resumo']}\n\n"

    # Contato
    conteudo += "## Contato\n\n"
    conteudo += f"- 📍 {dados['contato']['cidade']}\n"
    conteudo += f"- ✉️ {dados['contato']['email']}\n"
    conteudo += f"- 🔗 [LinkedIn]({dados['contato']['linkedin']})\n"
    conteudo += f"- 💻 [GitHub]({dados['contato']['github']})\n"

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(conteudo)

if __name__ == "__main__":
    gerar_readme()
