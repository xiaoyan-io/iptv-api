#!/usr/bin/env python3
"""chat-proxy — 轻量 LLM 代理，转发 prompt 到 Hermes 上游 API"""
import os, json, http.server, urllib.request

API_URL = os.environ.get("LLM_API_URL", "https://apihub.agnes-ai.com/v1/chat/completions")
API_KEY = os.environ.get("LLM_API_KEY", "")
MODEL  = os.environ.get("LLM_MODEL", "agnes-2.0-flash")
PORT   = int(os.environ.get("PROXY_PORT", "5181"))

class Handler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Methods","POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path != "/api/chat":
            self.send_error(404); return
        length = int(self.headers.get("Content-Length",0))
        body = json.loads(self.rfile.read(length))
        prompt = body.get("prompt","")
        system = body.get("system","你是一个实用的技术助手，用中文回答。先给结论再给步骤。\n\n当前可用的工具列表会在每次请求时由前端注入。")

        req = urllib.request.Request(
            API_URL,
            data=json.dumps({
                "model": MODEL,
                "messages": [
                    {"role":"system","content": system},
                    {"role":"user","content": prompt}
                ],
                "temperature": 0.5,
                "max_tokens": 2048,
            }).encode(),
            headers={
                "Content-Type":"application/json",
                "Authorization":f"Bearer {API_KEY}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read())
                reply = data["choices"][0]["message"]["content"]
        except Exception as e:
            reply = f"错误：{e}"

        self.send_response(200)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin","*")
        self.end_headers()
        self.wfile.write(json.dumps({"reply":reply}, ensure_ascii=False).encode())

    def log_message(self, fmt, *args):
        print(f"[chat-proxy] {args[0]} {args[1]} {args[2]}")

if __name__ == "__main__":
    if not API_KEY:
        print("⚠️  LLM_API_KEY 未设置，代理将返回模拟回复")
    print(f"chat-proxy 启动: {PORT}")
    http.server.HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
