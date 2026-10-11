import os, sys, json, base64, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

if sys.platform == 'win32':
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def get_github_token():
    token_file = r"C:\Users\Admin\.gemini\github_token.txt"
    if os.path.exists(token_file):
        with open(token_file, "rb") as f:
            raw = f.read()
            if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
                return raw.decode("utf-16").strip()
            return raw.decode("utf-8-sig").strip()
    return ""

def api_request(url, headers, method="GET", data=None):
    payload = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=payload, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.loads(res.read().decode("utf-8"))

def publish_all_to_github(source_dir=None, repo_name="virallabs-studio-ai", commit_message="StreamHub 24/7 Studio AI - Sincronización Completa"):
    token = get_github_token()
    if not token:
        return {"success": False, "message": "No se encontró el token de GitHub en C:\\Users\\Admin\\.gemini\\github_token.txt"}

    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "StreamHub-AutoUploader",
        "Accept": "application/vnd.github+json"
    }

    # 1. Autenticar usuario
    try:
        user_data = api_request("https://api.github.com/user", headers)
        username = user_data.get("login", "chenyz10yt")
        print(f"[GITHUB AUTH] Autenticado como: @{username}")
    except Exception as e:
        return {"success": False, "message": f"Error de autenticación con GitHub: {str(e)}"}

    # 2. Verificar o crear repositorio
    repo_url = f"https://api.github.com/repos/{username}/{repo_name}"
    try:
        api_request(repo_url, headers)
        print(f"[GITHUB REPO] Repositorio existente: {username}/{repo_name}")
    except urllib.error.HTTPError as he:
        if he.code == 404:
            print(f"[GITHUB REPO] Creando repositorio {username}/{repo_name}...")
            api_request("https://api.github.com/user/repos", headers, method="POST", data={
                "name": repo_name,
                "description": "StreamHub 24/7 Studio AI - Panel de Transmisión Multiplataforma y Estudio de Overlays",
                "private": False,
                "auto_init": True
            })
            print(f"[GITHUB REPO] Creado con éxito!")
        else:
            return {"success": False, "message": f"Error verificando repositorio: {he.reason}"}

    # 3. Obtener el commit base de 'main'
    try:
        ref_data = api_request(f"https://api.github.com/repos/{username}/{repo_name}/git/refs/heads/main", headers)
        base_commit_sha = ref_data["object"]["sha"]
        commit_data = api_request(f"https://api.github.com/repos/{username}/{repo_name}/git/commits/{base_commit_sha}", headers)
        base_tree_sha = commit_data["tree"]["sha"]
    except Exception as e:
        base_commit_sha = None
        base_tree_sha = None

    # 4. Directorio de origen: C:\Users\Admin\Desktop\chenyz.app\panel_stream
    if not source_dir:
        source_dir = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream"
    if not os.path.exists(source_dir):
        source_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    print(f"[GITHUB SCAN] Escaneando archivos desde: {source_dir}")

    ALLOWED_EXTS = {
        ".py", ".html", ".js", ".css", ".json", ".bat", ".sh", ".md",
        ".txt", ".svg", ".png", ".jpg", ".jpeg", ".ico", ".yml", ".yaml"
    }
    EXCLUDED_DIRS = {
        "bin", "recordings", "__pycache__", ".git", "previews", "playlists"
    }

    files_to_upload = []
    for root, dirs, files in os.walk(source_dir):
        dirs[:] = [d for d in dirs if d.lower() not in EXCLUDED_DIRS]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in ALLOWED_EXTS:
                fp = os.path.join(root, f)
                size = os.path.getsize(fp)
                if size < 15 * 1024 * 1024:
                    rel = os.path.relpath(fp, source_dir).replace("\\", "/")
                    if not rel.endswith(".mp4") and not rel.endswith(".zip"):
                        files_to_upload.append((fp, rel))

    print(f"[GITHUB BLOBS] Creando blobs para {len(files_to_upload)} archivos...")

    def create_blob(item):
        abs_p, rel_p = item
        try:
            with open(abs_p, "rb") as fl:
                content_bytes = fl.read()
            b64_content = base64.b64encode(content_bytes).decode("utf-8")
            res = api_request(
                f"https://api.github.com/repos/{username}/{repo_name}/git/blobs",
                headers,
                method="POST",
                data={"content": b64_content, "encoding": "base64"}
            )
            return (True, rel_p, res["sha"])
        except Exception as err:
            return (False, rel_p, str(err))

    tree_entries = []
    failed_blobs = []
    with ThreadPoolExecutor(max_workers=6) as executor:
        results = executor.map(create_blob, files_to_upload)
        for ok, rel_path, res_val in results:
            if ok:
                tree_entries.append({
                    "path": rel_path,
                    "mode": "100644",
                    "type": "blob",
                    "sha": res_val
                })
                print(f"  [Blob OK] {rel_path}")
            else:
                failed_blobs.append((rel_path, res_val))
                print(f"  [Blob ERROR] {rel_path} : {res_val}")

    if not tree_entries:
        return {"success": False, "message": "No se pudieron crear blobs para los archivos."}

    # 5. Crear Tree
    print(f"[GITHUB TREE] Creando Git Tree con {len(tree_entries)} elementos...")
    tree_payload = {
        "tree": tree_entries
    }
    if base_tree_sha:
        tree_payload["base_tree"] = base_tree_sha

    new_tree = api_request(
        f"https://api.github.com/repos/{username}/{repo_name}/git/trees",
        headers,
        method="POST",
        data=tree_payload
    )
    new_tree_sha = new_tree["sha"]

    # 6. Crear Commit
    print(f"[GITHUB COMMIT] Creando Commit: '{commit_message}'...")
    commit_payload = {
        "message": commit_message,
        "tree": new_tree_sha
    }
    if base_commit_sha:
        commit_payload["parents"] = [base_commit_sha]

    new_commit = api_request(
        f"https://api.github.com/repos/{username}/{repo_name}/git/commits",
        headers,
        method="POST",
        data=commit_payload
    )
    new_commit_sha = new_commit["sha"]

    # 7. Actualizar Ref heads/main
    print(f"[GITHUB PUSH] Actualizando branch main a {new_commit_sha[:8]}...")
    api_request(
        f"https://api.github.com/repos/{username}/{repo_name}/git/refs/heads/main",
        headers,
        method="PATCH",
        data={"sha": new_commit_sha, "force": True}
    )

    summary = {
        "success": True,
        "total": len(files_to_upload),
        "uploaded_count": len(tree_entries),
        "failed_count": len(failed_blobs),
        "commit_sha": new_commit_sha,
        "repo_url": f"https://github.com/{username}/{repo_name}",
        "message": f"¡Publicados exitosamente {len(tree_entries)} archivos en GitHub en el commit {new_commit_sha[:8]}!"
    }
    print(f"\n[GITHUB FINALIZADO] {summary['message']}")
    print(f"URL: {summary['repo_url']}")
    return summary

if __name__ == "__main__":
    res = publish_all_to_github()
    print(json.dumps(res, indent=2, ensure_ascii=False))
