from flask import Flask, render_template, request
import os
import scripts
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "Documents", "docs")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form.get("action") == "Importer":
            fichier = request.files.get("fichier_csv")
            jour1 = request.form.get("jour1")
            jour2 = request.form.get('jour2')
            if fichier and fichier.filename != "":
                chemin = os.path.join(app.config["UPLOAD_FOLDER"],os.path.basename(fichier.filename))
                fichier.save(chemin)
                print(f'Jour 1 : {jour1}, Jour 2 : {jour2}')
                data = scripts.get_data(chemin, jour1, jour2)
                print(data)
                
                return render_template("accueil.html",total_heures=data[1],proportions=data[2], message = f"Statistiques calculées du {jour1} au {jour2}")
    return render_template("accueil.html", message = None)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("--------------------------------------------")
    print(app.url_map)
    print("--------------------------------------------")
    app.run(host="0.0.0.0", port=port)
