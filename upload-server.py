#!/usr/bin/env python3
"""upload-server — 文件上传 + 分享链接"""
import os, json, shutil, hashlib, time, http.server, urllib.parse, uuid

SHARE_DIR = os.environ.get("SHARE_DIR", "/iptv-api/user_output/share/files")
PORT      = int(os.environ.get("UPLOAD_PORT", "5183"))
MAX_SIZE  = int(os.environ.get("MAX_UPLOAD_SIZE", str(200 * 1024 * 1024)))  # 200MB
BASE_URL  = os.environ.get("BASE_URL", "https://iptv.diynets.xyz")

os.makedirs(SHARE_DIR, exist_ok=True)

class Handler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/upload/list":
            self._list_files()
        else:
            self._send_json({"error": "not found"}, 404)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/upload":
            self._handle_upload()
        else:
            self._send_json({"error": "not found"}, 404)

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        if parsed.path == "/api/upload/delete" and qs.get("file"):
            self._delete_file(qs["file"][0])
        else:
            self._send_json({"error": "not found"}, 404)

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _send_json(self, data, status=200):
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    def _list_files(self):
        files = []
        for f in sorted(os.listdir(SHARE_DIR), key=lambda x: os.path.getmtime(os.path.join(SHARE_DIR, x)), reverse=True):
            fpath = os.path.join(SHARE_DIR, f)
            if os.path.isfile(fpath):
                size = os.path.getsize(fpath)
                mtime = os.path.getmtime(fpath)
                files.append({
                    "name": f,
                    "size": size,
                    "size_str": self._fmt_size(size),
                    "mtime": time.strftime("%Y-%m-%d %H:%M", time.localtime(mtime)),
                    "url": f"{BASE_URL}/share/files/{f}",
                })
        self._send_json({"files": files})

    def _delete_file(self, name):
        name = os.path.basename(name)
        fpath = os.path.join(SHARE_DIR, name)
        if os.path.exists(fpath):
            os.remove(fpath)
            self._send_json({"ok": True})
        else:
            self._send_json({"error": "file not found"}, 404)

    def _parse_multipart(self, body, boundary):
        """Simple multipart parser without cgi module (removed in Python 3.13)"""
        result = {}
        for part in body.split(b"--" + boundary):
            if not part.strip() or part.strip() == b"--":
                continue
            header_end = part.find(b"\r\n\r\n")
            if header_end == -1:
                continue
            headers_raw = part[:header_end].decode("utf-8", errors="replace")
            data = part[header_end + 4:]
            if data.endswith(b"\r\n"):
                data = data[:-2]

            filename = None
            name = None
            for line in headers_raw.split("\r\n"):
                if line.lower().startswith("content-disposition:"):
                    for seg in line.split(";"):
                        seg = seg.strip()
                        if seg.startswith('name="'):
                            name = seg[6:-1]
                        elif seg.startswith('filename="'):
                            filename = seg[10:-1]
            if name:
                result[name] = {"data": data, "filename": filename}
        return result

    def _handle_upload(self):
        ctype = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in ctype:
            self._send_json({"error": "multipart/form-data required"}, 400)
            return

        length = int(self.headers.get("Content-Length", 0))
        if length > MAX_SIZE:
            self._send_json({"error": f"file too large (max {MAX_SIZE//1024//1024}MB)"}, 413)
            return

        if length == 0:
            self._send_json({"error": "empty request"}, 400)
            return

        # extract boundary
        boundary = ctype.split("boundary=")[-1].strip().strip('"').encode()
        raw = self.rfile.read(length)
        parts = self._parse_multipart(raw, boundary)

        if "file" not in parts:
            self._send_json({"error": "no file provided (field name: 'file')"}, 400)
            return

        field = parts["file"]
        if not field.get("filename"):
            self._send_json({"error": "no filename"}, 400)
            return

        original_name = os.path.basename(field["filename"])
        data = field["data"]

        if len(data) == 0:
            self._send_json({"error": "empty file"}, 400)
            return

        sha1 = hashlib.sha1(data).hexdigest()
        name_parts = original_name.rsplit(".", 1)
        ext = name_parts[1].lower() if len(name_parts) > 1 else ""
        fname = f"{sha1[:12]}_{original_name}" if ext else f"{sha1[:12]}_{original_name}"
        fpath = os.path.join(SHARE_DIR, fname)

        with open(fpath, "wb") as f:
            f.write(data)

        file_size = len(data)
        share_url = f"{BASE_URL}/share/files/{fname}"
        self._send_json({
            "ok": True,
            "name": fname,
            "original_name": original_name,
            "size": file_size,
            "size_str": self._fmt_size(file_size),
            "url": share_url,
        })

    def _fmt_size(self, b):
        for unit in ("B","KB","MB","GB"):
            if b < 1024: return f"{b:.1f} {unit}"
            b /= 1024
        return f"{b:.1f} TB"

    def log_message(self, fmt, *args):
        print(f"[upload] {args[0]} {args[1]} {args[2]}")

if __name__ == "__main__":
    print(f"upload-server 启动: {PORT}  目录: {SHARE_DIR}")
    http.server.HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
