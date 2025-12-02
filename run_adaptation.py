import os
import app
from app import adapt_cv_with_gemini, compile_latex

# Job Description provided by the user
job_description = """
Contexte :
Berger-Levrault mène depuis plusieurs années une démarche de numérique responsable portée par la DRIT, notamment à travers des travaux de recherche en Green IT. Des premières expérimentations ont permis de mesurer la consommation énergétique et les coûts des pipelines CI/CD, mais uniquement sur des applications de petite taille.

Pour obtenir une vision représentative des environnements réels du groupe, il devient nécessaire d’étendre ces mesures à des applications plus variées et complexes, afin d'évaluer les impacts énergétiques et financiers des pratiques DevOps. 

🎯 Objectif :
Constituer un dataset structuré et représentatif pour analyse et apprentissage.
Développer un prototype d’outil de recommandation FinOps/Green IT, basé sur les données collectées.
Concevoir un tableau de bord de visualisation des métriques et recommandations.
 
🛠️ Missions :
Exécuter et mesurer la consommation de ressources (CPU, mémoire, durée, coût, énergie, empreinte carbone estimée) lors des processus CI/CD.
Instrumenter et exécuter des pipelines sur un panel d’applications variées (tailles, langages, architectures, charges).
Identifier les facteurs influençant la consommation et les pistes d’optimisation afin de concevoir un moteur de recommandation.
Étudier la transmission de l'étude au delà des pipeline CI-CD.

Preferred experience
Vous possédez des connaissances en développement logiciel et en intégration continue (Git, Jenkins, GitLab CI…).
Vous vous intéressez aux thématiques Green IT et FinOps.Vous disposez de compétences en analyse de données (Python, Pandas, SQL, Jupyter).
Vous avez des connaissances souhaitées en cloud computing, en monitoring (Prometheus, Grafana) ou en containers (Docker, Kubernetes).
Vous faites preuve d’un esprit d’analyse, de rigueur, de curiosité scientifique et d’autonomie.
Vous préparez un Master 2 et vous recherchez un stage de 6 mois débutant au printemps 2026.
"""

def main():
    print("Starting CV adaptation process...")
    
    # 1. Read LaTeX
    cv_filename = 'CV.tex'
    file_path = os.path.abspath(cv_filename)
    
    if not os.path.exists(file_path):
        print(f"Error: {cv_filename} not found.")
        return

    print(f"Reading {cv_filename}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        tex_content = f.read()
    
    # 2. Adapt with Gemini
    print("Adapting CV with Gemini (this may take a few seconds)...")
    try:
        adapted_tex_content = adapt_cv_with_gemini(tex_content, job_description)
    except Exception as e:
        print(f"Error during Gemini adaptation: {e}")
        return

    # Clean up markdown code blocks if Gemini adds them
    if adapted_tex_content.startswith("```latex"):
        adapted_tex_content = adapted_tex_content[8:]
    if adapted_tex_content.startswith("```"):
        adapted_tex_content = adapted_tex_content[3:]
    if adapted_tex_content.endswith("```"):
        adapted_tex_content = adapted_tex_content[:-3]
    
    # Save adapted version
    adapted_filename = f"adapted_{cv_filename}"
    adapted_file_path = os.path.join(app.app.config['UPLOAD_FOLDER'], adapted_filename)
    
    print(f"Saving adapted LaTeX to {adapted_file_path}...")
    with open(adapted_file_path, 'w', encoding='utf-8') as f:
        f.write(adapted_tex_content)
    
    # 3. Compile to PDF
    print("Compiling to PDF...")
    try:
        pdf_path = compile_latex(adapted_file_path, app.app.config['OUTPUT_FOLDER'])
        print(f"Success! PDF generated at: {pdf_path}")
    except Exception as e:
        print(f"Error during compilation: {e}")

if __name__ == "__main__":
    main()
