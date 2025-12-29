"""
Wizard end-to-end test using Flask test client.
Validates: language selection, welcome continue, requirements continue, db form render.
"""

from backend.src.app import create_app

app = create_app()
app.config["TESTING"] = True
client = app.test_client()

with app.app_context():
    # 1) GET /install/ should show language selection (wizard_started absent)
    r1 = client.get("/install/")
    html1 = r1.data.decode("utf-8", errors="ignore")
    assert r1.status_code == 200, f"/install/ status {r1.status_code}"
    assert ("Choisissez votre langue" in html1) or ("Choose your language" in html1), (
        "Language selection missing"
    )

    # 2) Select French language (start=1)
    r2 = client.get("/lang/fr?start=1", follow_redirects=True)
    assert r2.status_code == 200, f"/lang redirect status {r2.status_code}"

    # 3) GET /install/ after language should show welcome
    r3 = client.get("/install/")
    html3 = r3.data.decode("utf-8", errors="ignore")
    assert ("Bienvenue" in html3) or ("Welcome" in html3), "Welcome step not shown"

    # 4) POST welcome continue (HTMX equivalent)
    r4 = client.post(
        "/install/step", data={"step": "requirements", "welcome_shown": "1"}
    )
    html4 = r4.data.decode("utf-8", errors="ignore")
    assert r4.status_code == 200, f"POST /install/step status {r4.status_code}"
    assert ("Prérequis" in html4) or ("System Requirements" in html4), (
        "Requirements step not shown"
    )

    # 5) POST requirements continue to DB form
    r5 = client.post(
        "/install/step", data={"step": "db_form", "requirements_checked": "1"}
    )
    html5 = r5.data.decode("utf-8", errors="ignore")
    assert r5.status_code == 200, (
        f"POST /install/step (db_form) status {r5.status_code}"
    )
    assert ("Base de données" in html5) or ("Database" in html5), "DB form not shown"

print("WIZARD TEST: PASS")
