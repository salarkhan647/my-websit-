from flask import Flask, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

# ── Blog posts stored in memory ──────────────────────────────────────────────
blog_posts = [
    {
        "id": 1,
        "title": "I Built My First Website!!",
        "date": "April 22, 2026",
        "tag": "Python",
        "summary": "I learned Flask and built a real website with multiple pages. Here is how I did it.",
        "content": """
        I started learning Python a few months ago and today I deployed my first real website using Flask!
        It has a home page, calculator, password generator, and now a blog.
        <br><br>
        The hardest part was understanding how routes work — but once it clicked, it was so fun.
        Flask makes it really easy to build multi-page websites with just Python.
        <br><br>
        I am hosting it on Render.com for free. If you are learning Python, I highly recommend trying Flask!
        """
    },
    {
        "id": 2,
        "title": "How I Built a Password Generator",
        "date": "April 20, 2026",
        "tag": "Project",
        "summary": "A password generator that works in both desktop and web — built with Python.",
        "content": """
        I first built the password generator as a desktop app using customtkinter.
        It let users pick length, uppercase, lowercase, digits, and symbols.
        <br><br>
        Then I converted it into a web page using HTML and JavaScript so anyone can use it in their browser —
        no installation needed!
        <br><br>
        The logic is the same: build a character pool from selected options, then randomly pick characters.
        It was a great exercise in converting a desktop app to a web app.
        """
    },
    {
        "id": 3,
        "title": "Why I am Learning Programming",
        "date": "April 18, 2026",
        "tag": "Life",
        "summary": "My journey into coding and why I decided to start building real projects.",
        "content": """
        I started learning programming because I wanted to build things that actually work and that people can use.
        <br><br>
        I chose Python because it is beginner-friendly but also very powerful.
        You can build websites, apps, games, AI tools — almost anything.
        <br><br>
        My goal is to keep building, keep learning, and turn this into something real.
        Every project teaches me something new. If you are thinking about starting — just start!!
        """
    }
]

# ── Shared styles (full, no placeholders) ────────────────────────────────────
STYLES = """
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@400;600&display=swap" rel="stylesheet">
<style>
  :root {
    --red: #e94560;
    --red-dark: #c73652;
    --purple: #533483;
    --purple-dark: #3d2468;
    --bg: #1a1a2e;
    --bg2: #16213e;
    --bg3: #0f3460;
    --bg4: #0a1628;
    --text-muted: #a0aec0;
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    background: var(--bg);
    font-family: 'Rajdhani', sans-serif;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background-image: radial-gradient(circle at 20% 50%, var(--bg2) 0%, var(--bg) 50%, var(--bg3) 100%);
  }
  header {
    position: sticky; top: 0; z-index: 100;
    background: rgba(10,22,40,0.95);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(233,69,96,0.25);
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 40px; height: 64px;
  }
  .logo {
    font-family: 'Orbitron', sans-serif; color: var(--red);
    font-size: 20px; text-decoration: none; letter-spacing: 2px;
    text-shadow: 0 0 14px rgba(233,69,96,0.5);
  }
  nav { display: flex; gap: 6px; align-items: center; }
  nav a {
    color: var(--text-muted); text-decoration: none; padding: 8px 16px;
    border-radius: 6px; font-size: 14px; font-weight: 600; letter-spacing: 1px;
    text-transform: uppercase; transition: all 0.25s; border: 1px solid transparent;
  }
  nav a:hover, nav a.active {
    color: #fff; background: rgba(233,69,96,0.15);
    border-color: rgba(233,69,96,0.4); text-shadow: 0 0 8px rgba(233,69,96,0.6);
  }
  main { flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:50px 20px; }
  footer {
    background: rgba(10,22,40,0.95); border-top: 1px solid rgba(233,69,96,0.2);
    display:flex; align-items:center; justify-content:center; gap:40px; padding:22px 40px;
  }
  footer a { color:var(--text-muted); text-decoration:none; font-size:14px; font-weight:600; letter-spacing:1px; text-transform:uppercase; transition:color 0.2s; }
  footer a:hover { color:var(--red); }
  footer .dot { color:rgba(233,69,96,0.35); font-size:18px; }
  footer .copy { color:var(--text-muted); font-size:13px; }
  h1 { font-family:'Orbitron',sans-serif; color:var(--red); text-shadow:0 0 30px rgba(233,69,96,0.5); margin-bottom:20px; }
  .card { background:linear-gradient(145deg,var(--bg2),var(--bg3)); border-radius:16px; border:1px solid rgba(233,69,96,0.2); box-shadow:0 20px 60px rgba(0,0,0,0.5); padding:35px 45px; }
  .btn { display:inline-block; background:linear-gradient(135deg,var(--red),var(--red-dark)); color:white; padding:11px 26px; text-decoration:none; border-radius:8px; font-size:15px; font-weight:600; letter-spacing:1px; text-transform:uppercase; border:none; cursor:pointer; font-family:'Rajdhani',sans-serif; transition:all 0.3s; }
  .btn:hover { transform:translateY(-2px); box-shadow:0 6px 20px rgba(233,69,96,0.4); }
  .btn.purple { background:linear-gradient(135deg,var(--purple),var(--purple-dark)); }
  .btn.purple:hover { box-shadow:0 6px 20px rgba(83,52,131,0.5); }
  input[type=text], input[type=number], input[type=password], textarea { background:var(--bg4); color:white; border:1px solid rgba(233,69,96,0.3); border-radius:8px; padding:10px 16px; font-size:16px; font-family:'Rajdhani',sans-serif; outline:none; transition:border-color 0.2s; width:100%; }
  input:focus, textarea:focus { border-color:var(--red); box-shadow:0 0 10px rgba(233,69,96,0.3); }
  textarea { resize:vertical; width:100%; }
  .tag { display:inline-block; background:rgba(233,69,96,0.15); color:var(--red); border:1px solid rgba(233,69,96,0.35); border-radius:20px; padding:3px 12px; font-size:12px; font-weight:600; letter-spacing:1px; text-transform:uppercase; }
  .saved-item, .history-item { display: flex; justify-content: space-between; align-items: center; background: var(--bg4); border-radius: 8px; padding: 8px 12px; margin-bottom: 8px; transition: background 0.2s; }
  .saved-item { cursor: pointer; }
  .saved-item:hover, .history-item:hover { background: rgba(233,69,96,0.1); }
  .saved-info { flex: 1; display: flex; gap: 10px; align-items: baseline; overflow: hidden; }
  .saved-label { font-weight: bold; color: var(--red); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 120px; }
  .saved-pass { font-family: monospace; color: var(--text-muted); font-size: 12px; word-break: break-all; flex: 1; }
  .copy-pass-btn { background: none; border: 1px solid var(--red); color: var(--red); border-radius: 4px; padding: 4px 8px; margin-right: 8px; cursor: pointer; font-size: 12px; }
  .copy-pass-btn:hover { background: var(--red); color: white; }
  .saved-del { background: none; border: none; color: var(--text-muted); cursor: pointer; font-size: 18px; padding: 0 8px; }
  .saved-del:hover { color: var(--red); }
  .pin-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); z-index: 1000; display: flex; justify-content: center; align-items: center; }
  .pin-box { background: var(--bg2); padding: 30px; border-radius: 16px; text-align: center; border: 1px solid var(--red); max-width: 400px; width: 90%; }
  .clear-btn { margin-top: 15px; background: #333; }
  .save-section { border-top: 1px solid rgba(233,69,96,0.2); padding-top: 20px; margin-top: 10px; }
  .save-row { display: flex; gap: 10px; margin-bottom: 15px; }
  .btn-row { display: flex; gap: 10px; margin-bottom: 20px; }
  .options { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px; }
  .opt { display: flex; align-items: center; gap: 8px; background: var(--bg4); padding: 10px 14px; border-radius: 8px; border: 1px solid rgba(233,69,96,0.15); cursor: pointer; }
  .opt input { accent-color: var(--red); width: 16px; height: 16px; }
  #result { width:100%; padding:12px 15px; font-size:14px; font-family:'Courier New',monospace; background:var(--bg4); color:var(--red); border:1px solid rgba(233,69,96,0.3); border-radius:8px; margin-bottom:6px; text-align:center; min-height:46px; word-break:break-all; }
  #copy-msg { color:#4caf50; font-size:13px; height:18px; margin-bottom:12px; text-align:center; }
  .calc-grid button { width:64px; height:64px; margin:4px; font-size:20px; border:none; border-radius:8px; cursor:pointer; font-family:'Rajdhani',sans-serif; font-weight:700; transition:all 0.15s; }
  .num { background:linear-gradient(135deg,var(--red),var(--red-dark)); color:white; }
  .op  { background:linear-gradient(135deg,var(--purple),var(--purple-dark)); color:white; }
  .calc-grid button:hover  { transform:scale(1.08); box-shadow:0 4px 15px rgba(233,69,96,0.4); }
  #display { width:290px; padding:15px; font-size:28px; text-align:right; background:var(--bg4); color:var(--red); border:1px solid rgba(233,69,96,0.3); border-radius:8px; margin-bottom:14px; font-family:'Orbitron',monospace; outline:none; }
  .history-panel { margin-top: 30px; border-top: 1px solid rgba(233,69,96,0.2); padding-top: 20px; width: 100%; }
  .blog-card { display:block; text-decoration:none; background:linear-gradient(145deg,var(--bg2),var(--bg3)); border:1px solid rgba(233,69,96,0.15); border-radius:14px; padding:28px 32px; margin-bottom:20px; transition:all 0.3s; position:relative; overflow:hidden; }
  .blog-card:hover { transform:translateY(-4px); border-color:rgba(233,69,96,0.4); box-shadow:0 16px 40px rgba(0,0,0,0.4); }
  .blog-title { font-family:'Orbitron',sans-serif; color:white; font-size:20px; margin-bottom:10px; }
  .blog-summary { color:var(--text-muted); font-size:16px; line-height:1.6; margin-bottom:16px; }
  .read-more { color:var(--red); font-size:14px; font-weight:600; }
</style>
"""

def make_header(active=""):
    links = [
        ("home", "/", "Home"),
        ("calc", "/calculator", "Calculator"),
        ("pwd", "/password", "🔐 Password"),
        ("blog", "/blog", "📝 Blog"),
    ]
    nav_html = "".join(f'<a href="{href}" {"class=active" if active==key else ""}>{label}</a>' for key, href, label in links)
    return f'<header><a class="logo" href="/">SALAR.DEV</a><nav>{nav_html}</nav></header>'

FOOTER = """
<footer>
  <a href="/about">About Me</a><span class="dot">·</span>
  <a href="/contact">Contact</a><span class="dot">·</span>
  <span class="copy">© 2026 Salar</span>
</footer>"""

def page(content, active=""):
    return f"""<!DOCTYPE html>
<html><head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Salar.dev</title>
  {STYLES}
</head><body>
  {make_header(active)}
  <main>{content}</main>
  {FOOTER}
</body></html>"""


# ── HOME (full particle effect) ──────────────────────────────────────────────
@app.route("/")
def home():
    content = """
    <canvas id="particle-canvas" style="position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:0;"></canvas>
    <div style="position:relative; z-index:1; text-align:center;">
      <h1 class="hero-title" style="font-family:'Orbitron',sans-serif; font-size:62px; color:var(--red); animation:glow 2.5s infinite alternate;">Hello Salar!!</h1>
      <p style="color:var(--text-muted); font-size:20px; letter-spacing:4px; margin-bottom:40px;">Developer · Builder · Creator</p>
      <div style="display:flex; gap:16px; justify-content:center; flex-wrap:wrap;">
        <a href="/blog" class="btn">📝 Read Blog</a>
        <a href="/calculator" class="btn purple">Calculator</a>
        <a href="/password" class="btn purple">🔐 Password Gen</a>
      </div>
      <div style="display:flex; gap:50px; margin-top:60px; justify-content:center;">
        <div><div style="font-family:'Orbitron'; font-size:32px; color:var(--red);">4+</div><div style="color:var(--text-muted);">Pages Built</div></div>
        <div><div style="font-family:'Orbitron'; font-size:32px; color:var(--red);">3</div><div style="color:var(--text-muted);">Blog Posts</div></div>
        <div><div style="font-family:'Orbitron'; font-size:32px; color:var(--red);">1</div><div style="color:var(--text-muted);">Live Website</div></div>
      </div>
    </div>
    <script>
      const canvas=document.getElementById('particle-canvas'),ctx=canvas.getContext('2d');
      let particles=[];
      function resize(){canvas.width=window.innerWidth;canvas.height=window.innerHeight;}
      resize(); window.addEventListener('resize',resize);
      class Particle{ constructor(){this.reset();} reset(){this.x=Math.random()*canvas.width;this.y=Math.random()*canvas.height;this.r=Math.random()*2+0.5;this.dx=(Math.random()-0.5)*0.6;this.dy=(Math.random()-0.5)*0.6;this.alpha=Math.random()*0.5+0.1;} update(){this.x+=this.dx;this.y+=this.dy;if(this.x<0||this.x>canvas.width||this.y<0||this.y>canvas.height)this.reset();} draw(){ctx.beginPath();ctx.arc(this.x,this.y,this.r,0,Math.PI*2);ctx.fillStyle=`rgba(233,69,96,${this.alpha})`;ctx.fill();} }
      for(let i=0;i<120;i++)particles.push(new Particle());
      function animate(){ctx.clearRect(0,0,canvas.width,canvas.height);particles.forEach(p=>{p.update();p.draw();}); for(let i=0;i<particles.length;i++)for(let j=i+1;j<particles.length;j++){const dx=particles[i].x-particles[j].x,dy=particles[i].y-particles[j].y,d=Math.hypot(dx,dy); if(d<100){ctx.beginPath();ctx.moveTo(particles[i].x,particles[i].y);ctx.lineTo(particles[j].x,particles[j].y);ctx.strokeStyle=`rgba(233,69,96,${0.12*(1-d/100)})`;ctx.lineWidth=0.5;ctx.stroke();}} requestAnimationFrame(animate);}
      animate();
    </script>
    <style> @keyframes glow { from{text-shadow:0 0 20px rgba(233,69,96,0.4);} to{text-shadow:0 0 60px rgba(233,69,96,1),0 0 100px rgba(233,69,96,0.4);} } </style>
    """
    return page(content, "home")


# ── BLOG LIST ────────────────────────────────────────────────────────────────
@app.route("/blog")
def blog():
    cards = ""
    for post in reversed(blog_posts):
        cards += f"""
        <a href="/blog/{post['id']}" class="blog-card">
          <div style="display:flex; justify-content:space-between; margin-bottom:12px;"><span class="tag">{post['tag']}</span><span style="color:var(--text-muted);font-size:13px;">{post['date']}</span></div>
          <h2 class="blog-title">{post['title']}</h2>
          <p class="blog-summary">{post['summary']}</p>
          <span class="read-more">Read more →</span>
        </a>"""
    content = f"""
    <div style="max-width:720px; width:100%;">
      <div style="text-align:center; margin-bottom:40px;"><h1 style="font-size:42px;">📝 Blog</h1><p style="color:var(--text-muted);">Thoughts, projects, and lessons</p></div>
      {cards}
      <div style="text-align:center; margin-top:10px;"><a href="/blog/new" class="btn">+ Write New Post</a></div>
    </div>"""
    return page(content, "blog")

@app.route("/blog/<int:post_id>")
def blog_post(post_id):
    post = next((p for p in blog_posts if p["id"] == post_id), None)
    if not post:
        return redirect(url_for("blog"))
    content = f"""
    <div style="max-width:680px;">
      <div style="display:flex; gap:16px; align-items:center; margin-bottom:20px;"><span class="tag">{post['tag']}</span><span style="color:var(--text-muted);">{post['date']}</span></div>
      <h1 style="font-family:'Orbitron'; font-size:34px; color:var(--red); margin-bottom:28px;">{post['title']}</h1>
      <hr style="border-color:rgba(233,69,96,0.15); margin:32px 0;">
      <div style="color:#c8d6e5; font-size:18px; line-height:1.8;">{post['content']}</div>
      <a href="/blog" class="btn" style="margin-top:40px; display:inline-block;">← Back to Blog</a>
    </div>"""
    return page(content, "blog")

@app.route("/blog/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        tag = request.form.get("tag", "General").strip()
        summary = request.form.get("summary", "").strip()
        body = request.form.get("body", "").strip()
        if title and body:
            new_id = max(p["id"] for p in blog_posts) + 1
            blog_posts.append({
                "id": new_id,
                "title": title,
                "date": datetime.now().strftime("%B %d, %Y"),
                "tag": tag,
                "summary": summary or body[:120] + "...",
                "content": body.replace("\n", "<br>")
            })
            return redirect(url_for("blog_post", post_id=new_id))
    content = """
    <h1 style="font-size:36px;">Write New Post</h1>
    <div class="card" style="max-width:640px; text-align:left;">
      <form method="POST">
        <div style="margin-bottom:20px;"><label style="display:block; color:var(--text-muted); margin-bottom:8px;">Title</label><input type="text" name="title" placeholder="Your post title..."></div>
        <div style="margin-bottom:20px;"><label style="display:block; color:var(--text-muted); margin-bottom:8px;">Tag</label><input type="text" name="tag" placeholder="e.g. Python, Project"></div>
        <div style="margin-bottom:20px;"><label style="display:block; color:var(--text-muted); margin-bottom:8px;">Summary (optional)</label><input type="text" name="summary" placeholder="Short description..."></div>
        <div style="margin-bottom:20px;"><label style="display:block; color:var(--text-muted); margin-bottom:8px;">Content</label><textarea name="body" rows="8" placeholder="Write your post here..."></textarea></div>
        <button type="submit" class="btn" style="width:100%;">Publish Post</button>
      </form>
    </div>"""
    return page(content, "blog")


# ── CALCULATOR with history ───────────────────────────────────────────────────
@app.route("/calculator")
def calculator():
    content = """
    <h1 style="font-size:36px;">Calculator</h1>
    <div class="card">
      <input id="display" type="text" value="0" readonly><br>
      <div class="calc-grid">
        <button class="num" onclick="press('7')">7</button><button class="num" onclick="press('8')">8</button><button class="num" onclick="press('9')">9</button><button class="op" onclick="press('+')">+</button><br>
        <button class="num" onclick="press('4')">4</button><button class="num" onclick="press('5')">5</button><button class="num" onclick="press('6')">6</button><button class="op" onclick="press('-')">−</button><br>
        <button class="num" onclick="press('1')">1</button><button class="num" onclick="press('2')">2</button><button class="num" onclick="press('3')">3</button><button class="op" onclick="press('*')">×</button><br>
        <button class="op" onclick="clearD()">C</button><button class="num" onclick="press('0')">0</button><button class="op" onclick="calc()">=</button><button class="op" onclick="press('/')">÷</button>
      </div>
      <div class="history-panel">
        <h3 style="color:var(--red); margin-bottom:10px;">📜 History (click to autofill)</h3>
        <div id="historyList"></div>
        <button class="btn clear-btn" onclick="clearHistory()">Clear History</button>
      </div>
    </div>
    <script>
      let calculationHistory = JSON.parse(localStorage.getItem('calc_history') || '[]');
      function saveHistory() { localStorage.setItem('calc_history', JSON.stringify(calculationHistory)); renderHistory(); }
      function renderHistory() {
        const container = document.getElementById('historyList');
        if (!calculationHistory.length) { container.innerHTML = '<div style="color:var(--text-muted); text-align:center; padding:10px;">No saved calculations</div>'; return; }
        container.innerHTML = calculationHistory.map((item, idx) => `<div class="history-item" onclick="useHistory(${idx})"><span>${item.expr}</span><span style="color:var(--red); margin-left:10px;">= ${item.result}</span></div>`).join('');
      }
      function useHistory(idx) { document.getElementById('display').value = calculationHistory[idx].expr; }
      function clearHistory() { calculationHistory = []; saveHistory(); }
      window.calc = function() {
        let display = document.getElementById('display');
        let expr = display.value;
        try {
          let result = eval(expr);
          display.value = result;
          if (!calculationHistory.length || calculationHistory[0].expr !== expr) {
            calculationHistory.unshift({ expr: expr, result: result });
            if (calculationHistory.length > 20) calculationHistory.pop();
            saveHistory();
          }
        } catch(e) { display.value = 'Error'; }
      }
      function press(v) { var d=document.getElementById('display'); d.value = d.value=='0' ? v : d.value+v; }
      function clearD() { document.getElementById('display').value='0'; }
      renderHistory();
    </script>
    """
    return page(content, "calc")


# ── PASSWORD GENERATOR with PIN lock & save/autofill ─────────────────────────
@app.route("/password")
def password():
    content = """
    <div id="pinOverlay" class="pin-overlay">
      <div class="pin-box">
        <h2 style="color:var(--red);">🔒 Enter PIN to access saved passwords</h2>
        <input type="password" id="pinInput" placeholder="4-digit PIN" maxlength="4" style="margin:20px 0; text-align:center; width:100%;">
        <div><button class="btn" onclick="checkPin()">Unlock</button></div>
        <div style="margin-top:15px;"><button class="btn purple" onclick="setupPin()">Set New PIN (if not set)</button></div>
      </div>
    </div>
    <div id="mainContent" style="display:none;">
      <h1 style="font-size:34px;">🔐 Password Generator</h1>
      <div class="card pw-card" style="width:450px; max-width:100%;">
        <span class="field-label">Password Length</span>
        <input type="number" id="length" value="12" min="4" max="64">
        <div class="options">
          <label class="opt"><input type="checkbox" id="lower" checked><span>Lowercase</span></label>
          <label class="opt"><input type="checkbox" id="upper" checked><span>Uppercase</span></label>
          <label class="opt"><input type="checkbox" id="digits" checked><span>Digits</span></label>
          <label class="opt"><input type="checkbox" id="symbols" checked><span>Symbols</span></label>
        </div>
        <div id="result">Click Generate!!</div>
        <div id="copyMsg"></div>
        <div class="btn-row">
          <button class="btn" onclick="generatePassword()">Generate</button>
          <button class="btn purple" onclick="copyPassword()">Copy</button>
        </div>
        <div class="save-section">
          <div class="save-row">
            <input type="text" id="saveLabel" placeholder="Label (e.g. Gmail)">
            <button class="btn purple" onclick="saveCurrentPassword()">Save Password</button>
          </div>
          <h3 style="color:var(--red); font-size:16px; margin-bottom:10px;">💾 Saved Passwords (click to autofill, 📋 to copy)</h3>
          <div id="savedPasswordsList"></div>
          <button class="btn clear-btn" onclick="clearAllData()">Clear All Saved Data</button>
        </div>
      </div>
    </div>
    <script>
      let savedPasswords = [];
      let isUnlocked = false;
      let pinHash = localStorage.getItem('pin_hash');
      
      function hashPin(pin) {
        let hash = 0;
        for (let i = 0; i < pin.length; i++) { hash = ((hash << 5) - hash) + pin.charCodeAt(i); hash |= 0; }
        return hash.toString();
      }
      function setupPin() {
        let newPin = prompt("Set a new 4-digit PIN for this browser:");
        if (newPin && newPin.length === 4 && /^\\d+$/.test(newPin)) {
          localStorage.setItem('pin_hash', hashPin(newPin));
          alert("PIN set! Reload page to lock again.");
          location.reload();
        } else { alert("PIN must be 4 digits."); }
      }
      function checkPin() {
        let entered = document.getElementById('pinInput').value;
        if (!pinHash) { unlock(); return; }
        if (hashPin(entered) === pinHash) { unlock(); }
        else { alert("Wrong PIN!"); }
      }
      function unlock() {
        isUnlocked = true;
        document.getElementById('pinOverlay').style.display = 'none';
        document.getElementById('mainContent').style.display = 'block';
        loadSavedPasswords();
        renderSavedPasswords();
      }
      function loadSavedPasswords() { if(isUnlocked) savedPasswords = JSON.parse(localStorage.getItem('saved_passwords') || '[]'); }
      function saveToLocalStorage() { localStorage.setItem('saved_passwords', JSON.stringify(savedPasswords)); }
      function renderSavedPasswords() {
        const container = document.getElementById('savedPasswordsList');
        if (!savedPasswords.length) { container.innerHTML = '<div style="color:var(--text-muted); text-align:center; padding:10px;">No saved passwords</div>'; return; }
        container.innerHTML = savedPasswords.map((item, idx) => `
          <div class="saved-item">
            <div class="saved-info" onclick="autofillPassword(${idx})">
              <span class="saved-label">${escapeHtml(item.label)}</span>
              <span class="saved-pass">${escapeHtml(item.password)}</span>
            </div>
            <button class="copy-pass-btn" onclick="event.stopPropagation(); copySinglePassword('${escapeHtml(item.password)}')">📋 Copy</button>
            <button class="saved-del" onclick="event.stopPropagation(); deletePassword(${idx})">🗑️</button>
          </div>
        `).join('');
      }
      function escapeHtml(str) { return str.replace(/[&<>]/g, function(m){ if(m==='&') return '&amp;'; if(m==='<') return '&lt;'; if(m==='>') return '&gt;'; return m;}); }
      function copySinglePassword(pwd) { navigator.clipboard.writeText(pwd).then(()=>{ let m=document.getElementById('copyMsg'); m.innerText='Copied!'; setTimeout(()=>m.innerText='',1500); }); }
      function saveCurrentPassword() {
        if(!isUnlocked) return;
        const password = document.getElementById('result').innerText;
        if(password.includes('Click')||password.includes('Select')){ document.getElementById('copyMsg').innerText='Generate a password first!'; setTimeout(()=>document.getElementById('copyMsg').innerText='',1500); return; }
        let label = document.getElementById('saveLabel').value.trim();
        if(label==='') label = `Password ${savedPasswords.length+1}`;
        savedPasswords.unshift({ label: label, password: password });
        if(savedPasswords.length > 20) savedPasswords.pop();
        saveToLocalStorage();
        renderSavedPasswords();
        document.getElementById('saveLabel').value = '';
        document.getElementById('copyMsg').innerText = 'Saved!';
        setTimeout(()=>document.getElementById('copyMsg').innerText='',1500);
      }
      function autofillPassword(idx) { document.getElementById('result').innerText = savedPasswords[idx].password; document.getElementById('copyMsg').innerText = 'Autofilled!'; setTimeout(()=>document.getElementById('copyMsg').innerText='',1500); }
      function deletePassword(idx) { savedPasswords.splice(idx,1); saveToLocalStorage(); renderSavedPasswords(); }
      function clearAllData() { if(confirm('Delete ALL saved passwords and history?')){ localStorage.removeItem('saved_passwords'); localStorage.removeItem('calc_history'); savedPasswords=[]; renderSavedPasswords(); document.getElementById('copyMsg').innerText='All data cleared.'; setTimeout(()=>document.getElementById('copyMsg').innerText='',2000); } }
      function generatePassword(){
        const len=parseInt(document.getElementById('length').value);
        let chars='';
        if(document.getElementById('lower').checked) chars+='abcdefghijklmnopqrstuvwxyz';
        if(document.getElementById('upper').checked) chars+='ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        if(document.getElementById('digits').checked) chars+='0123456789';
        if(document.getElementById('symbols').checked) chars+='!@#$%^&*()_+-=[]{}|;:,.<>?';
        if(!chars){document.getElementById('result').innerText='Select at least one option!!';return;}
        let pwd=''; for(let i=0;i<len;i++) pwd+=chars[Math.floor(Math.random()*chars.length)];
        document.getElementById('result').innerText=pwd;
        document.getElementById('copyMsg').innerText='';
      }
      function copyPassword(){
        const pwd=document.getElementById('result').innerText;
        if(pwd.includes('Click')||pwd.includes('Select')) return;
        navigator.clipboard.writeText(pwd).then(()=>{ const m=document.getElementById('copyMsg'); m.innerText='Copied to clipboard!'; setTimeout(()=>m.innerText='',2000); });
      }
      if(!pinHash) { unlock(); } // if no PIN set, show content directly
    </script>
    """
    return page(content, "pwd")


# ── ABOUT & CONTACT ──────────────────────────────────────────────────────────
@app.route("/about")
def about():
    content = """
    <div style="text-align:center; max-width:480px;">
      <h1 style="font-size:42px;">About Me!!</h1>
      <div class="card">
        <p style="color:var(--text-muted); font-size:19px; margin:12px 0;">My name is <span style="color:var(--red);">Salar!!</span></p>
        <p style="color:var(--text-muted); font-size:19px;">I am learning <span style="color:var(--red);">Python and Flask!!</span></p>
        <p style="color:var(--text-muted); font-size:19px;">I build real websites and apps!!</p>
      </div>
    </div>"""
    return page(content)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "")
        content = f"""
        <h1 style="font-size:46px;">Hello {name}!!</h1>
        <p style="color:var(--text-muted);font-size:20px;margin-bottom:30px;">Thanks for contacting me!!</p>
        <a href="/" class="btn">Home</a>"""
        return page(content)
    content = """
    <h1 style="font-size:42px;">Contact Me!!</h1>
    <div class="card" style="width:380px; text-align:center;">
      <form method="POST">
        <input type="text" name="name" placeholder="Your name!!">
        <button type="submit" class="btn" style="width:100%; margin-top:16px;">Submit!!</button>
      </form>
    </div>"""
    return page(content)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
