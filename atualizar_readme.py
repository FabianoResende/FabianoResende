import json

def gerar_readme():
    # 1. Carrega os dados do JSON
    with open('dados_curriculo.json', 'r', encoding='utf-8') as f:
        dados = json.load(f)

    # 2. Dicionário de Badges (Aqui você define a beleza do README)
    # Você pode adicionar mais conforme aprender novas tecnologias!
    badges = {
        "Python": "![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)",
        "SQL": "![SQL](https://img.shields.io/badge/sql-003B57?style=for-the-badge&logo=postgresql&logoColor=white)",
        "JavaScript": "![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)",
        "Git & GitHub": "![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)"
    }

    # Transforma a lista de tecnologias em badges
    lista_badges = [badges.get(tecnologia, tecnologia) for tecnologia in dados['tecnologias']]
    string_badges = " ".join(lista_badges)

    # 3. O "Template" do seu README (Onde a mágica visual acontece)
    conteudo_readme = f"""
# Olá, eu sou o {dados['nome']}! 👋

### {dados['cargo']}

{dados['sobre']}

---

## 🛠️ Tecnologias e Ferramentas
{string_badges}

---

## 🎓 Formação Acadêmica
"""
    # Adiciona a educação dinamicamente
    for ed in dados['educacao']:
        conteudo_readme += f"- **{ed['curso']}** | {ed['instituicao']} ({ed['periodo']})\n"

    conteudo_readme += "\n## 🏆 Certificações\n"
    for cert in dados['certificacoes']:
        conteudo_readme += f"- {cert}\n"

    conteudo_readme += f"\n--- \n*Este perfil é atualizado automaticamente via Python e GitHub Actions! 🚀*"

    # 4. Salva o arquivo README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(conteudo_readme)
    
    print("README.md atualizado com sucesso!")

if __name__ == "__main__":
    gerar_readme()
