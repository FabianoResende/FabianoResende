import json

def gerar_readme():
    with open('dados_curriculo.json', 'r', encoding='utf-8') as f:
        dados = json.load(f)

    badges = {
        "Python": "![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)",
        "SQL": "![SQL](https://img.shields.io/badge/sql-003B57?style=for-the-badge&logo=postgresql&logoColor=white)",
        "JavaScript": "![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)",
        "Git & GitHub": "![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)",
        "Linux": "![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)"
    }

    # Monta as badges de Linguagens
    badges_tecnicas = " ".join([badges.get(t, f"`{t}`") for t in dados['competencias']['linguagens']])

    conteudo = f"""
# {dados['nome']} 🚀

### {dados['cargo']}
**Foco:** {dados['foco']}

{dados['sobre']}

---

## 🛠️ Competências Técnicas
{badges_tecnicas}

---

## 📂 Projetos
"""
    for proj in dados['projetos']:
        conteudo += f"### 🔹 {proj['nome']}\n{proj['descricao']}\n\n"

    conteudo += "## 💼 Experiência Profissional\n"
    for exp in dados['experiencia']:
        conteudo += f"**{exp['empresa']}** | {exp['cargo']} ({exp['periodo']})\n- {exp['resumo']}\n\n"

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(conteudo)

if __name__ == "__main__":
    gerar_readme()
