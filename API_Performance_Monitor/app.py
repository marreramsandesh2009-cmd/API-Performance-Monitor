from flask import Flask, render_template, request, jsonify
from monitor import check_api
from database import init_db, save_result, get_results

app = Flask(__name__)

init_db()

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/check", methods=["POST"])
def check():
    data = request.get_json()
    url = data.get("url", "").strip()

    if not url:
        return jsonify({
            "success": False,
            "error": "API URL is required."
        }), 400

    result = check_api(url)
    save_result(result)

    return jsonify(result)

@app.route("/api/results")
def results():
    return jsonify(get_results())

if __name__ == "__main__":
    app.run(debug=True)