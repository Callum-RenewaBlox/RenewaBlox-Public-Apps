"""Keep eunice/data_lite.sqlite current on Streamlit Cloud.

The forecast is retrained and data_lite.sqlite is rebuilt twice a day (about 09:45 and 16:35
UTC) by the "Daily refresh" workflow in the private RenewaBlox/Eunice-Platform repository.
The copy committed beside this file is a snapshot, so on its own the app would go stale.

When the app's Streamlit secrets set EUNICE_DATA_TOKEN (a fine-grained GitHub token with
read-only Contents access to RenewaBlox/Eunice-Platform), the app downloads the latest
data_lite.sqlite from that repository at most once every REFRESH_SECONDS and swaps it in
atomically. Without the token, or if the download fails, the committed snapshot is used.
The token lives only in the app's secrets, never in this public repository.
"""

import os
import sqlite3
import tempfile
import time
from pathlib import Path

import requests

SOURCE_REPO = os.environ.get("EUNICE_DATA_REPO", "RenewaBlox/Eunice-Platform")
SOURCE_PATH = "data_lite.sqlite"
SOURCE_REF = os.environ.get("EUNICE_DATA_REF", "main")
REFRESH_SECONDS = 30 * 60


def refresh(db_path: Path) -> None:
    token = os.environ.get("EUNICE_DATA_TOKEN", "").strip()
    if not token:
        return
    # The last attempt is recorded in a marker file, not the database's mtime: a fresh
    # checkout's mtime is the clone time, which would delay the first download.
    marker = db_path.with_name(db_path.name + ".checked")
    if marker.exists() and time.time() - marker.stat().st_mtime < REFRESH_SECONDS:
        return
    marker.touch()
    try:
        r = requests.get(
            f"https://api.github.com/repos/{SOURCE_REPO}/contents/{SOURCE_PATH}",
            params={"ref": SOURCE_REF},
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.raw+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=60,
        )
        r.raise_for_status()
        fd, tmp = tempfile.mkstemp(dir=db_path.parent, suffix=".sqlite.part")
        with os.fdopen(fd, "wb") as f:
            f.write(r.content)
        try:
            # Only swap in a readable database with the prediction table.
            with sqlite3.connect(tmp) as c:
                c.execute("SELECT 1 FROM prediction LIMIT 1")
        except sqlite3.Error:
            os.remove(tmp)
            return
        os.chmod(tmp, 0o644)
        os.replace(tmp, db_path)
    except Exception:
        # Network or auth trouble: keep serving the database already on disk. The marker
        # above stops a failing token from retrying on every rerun.
        pass
