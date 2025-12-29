"""Debug DB form display"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.src.app import create_app

app = create_app()
app.config["TESTING"] = True

with app.test_client() as client, app.app_context():
    client.get("/lang/fr?start=1")
    client.post("/install/step", data={"step": "requirements", "welcome_shown": "1"})

    r = client.post(
        "/install/step",
        data={"step": "db_form", "requirements_checked": "1", "welcome_shown": "1"},
    )

    html = r.data.decode("utf-8", errors="ignore")
    print(f"Status: {r.status_code}")
    print("HTML preview (first 2000 chars):")
    print(html[:2000])

    if "SQLite" in html:
        print("\n✅ SQLite found")
    else:
        print("\n❌ SQLite NOT found")

    if "Base de données" in html or "Database" in html:
        print("✅ Database label found")
    else:
        print("❌ Database label NOT found")
