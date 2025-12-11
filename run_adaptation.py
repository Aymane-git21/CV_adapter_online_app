import os
import app
from app import adapt_cv_with_gemini, compile_latex, generate_cover_letter, generate_short_message

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
    
    # 1.5 Read Master CV
    master_cv_path = os.path.abspath('master_cv.md')
    print(f"Reading {master_cv_path}...")
    if os.path.exists(master_cv_path):
        with open(master_cv_path, 'r', encoding='utf-8') as f:
            master_cv_content = f.read()
    else:
        print("Warning: master_cv.md not found.")
        master_cv_content = ""

    # 2. Adapt CV with Gemini
    print("Adapting CV with Gemini (this may take a few seconds)...")
    try:
        adapted_tex_content = adapt_cv_with_gemini(tex_content, job_description, master_cv_content)
    except Exception as e:
        print(f"Error during Gemini adaptation: {e}")
        return

    # Clean up markdown code blocks if Gemini adds them
    if adapted_tex_content.startswith("```latex"): adapted_tex_content = adapted_tex_content[8:]
    if adapted_tex_content.startswith("```"): adapted_tex_content = adapted_tex_content[3:]
    if adapted_tex_content.endswith("```"): adapted_tex_content = adapted_tex_content[:-3]
    
    # Save adapted version
    adapted_filename = f"adapted_{cv_filename}"
    adapted_file_path = os.path.join(app.app.config['UPLOAD_FOLDER'], adapted_filename)
    
    print(f"Saving adapted LaTeX to {adapted_file_path}...")
    with open(adapted_file_path, 'w', encoding='utf-8') as f:
        f.write(adapted_tex_content)
    
    # 3. Compile CV to PDF
    print("Compiling CV to PDF...")
    try:
        pdf_path = compile_latex(adapted_file_path, app.app.config['OUTPUT_FOLDER'])
        print(f"Success! CV PDF generated at: {pdf_path}")
    except Exception as e:
        print(f"Error during CV compilation: {e}")

    # 4. Generate Cover Letter
    print("Generating Cover Letter...")
    try:
        cover_letter_tex = generate_cover_letter(job_description, master_cv_content)
        
        if cover_letter_tex.startswith("```latex"): cover_letter_tex = cover_letter_tex[8:]
        if cover_letter_tex.startswith("```"): cover_letter_tex = cover_letter_tex[3:]
        if cover_letter_tex.endswith("```"): cover_letter_tex = cover_letter_tex[:-3]

        cl_filename = "Cover_Letter.tex"
        cl_file_path = os.path.join(app.app.config['UPLOAD_FOLDER'], cl_filename)
        
        print(f"Saving Cover Letter LaTeX to {cl_file_path}...")
        with open(cl_file_path, 'w', encoding='utf-8') as f:
            f.write(cover_letter_tex)
            
        cl_pdf_path = compile_latex(cl_file_path, app.app.config['OUTPUT_FOLDER'])
        print(f"Success! Cover Letter PDF generated at: {cl_pdf_path}")
    except Exception as e:
        print(f"Error during Cover Letter generation: {e}")

    # 5. Generate Short Message
    print("Generating Short Message...")
    try:
        short_message = generate_short_message(job_description, master_cv_content)
        msg_filename = "short_message.txt"
        msg_file_path = os.path.join(app.app.config['OUTPUT_FOLDER'], msg_filename)
        
        with open(msg_file_path, 'w', encoding='utf-8') as f:
            f.write(short_message)
        print(f"Success! Short message saved to: {msg_file_path}")
        print("-" * 20)
        print(short_message)
        print("-" * 20)
    except Exception as e:
        print(f"Error during Short Message generation: {e}")

if __name__ == "__main__":
    main()
