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

# ── Shared styles ─────────────────────────────────────────────────────────────

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
  input[type=text], input[type=number], textarea { background:var(--bg4); color:white; border:1px solid rgba(233,69,96,0.3); border-radius:8px; padding:10px 16px; font-size:16px; font-family:'Rajdhani',sans-serif; outline:none; transition:border-color 0.2s; }
  input:focus, textarea:focus { border-color:var(--red); box-shadow:0 0 10px rgba(233,69,96,0.3); }
  textarea { resize:vertical; width:100%; }
  .tag { display:inline-block; background:rgba(233,69,96,0.15); color:var(--red); border:1px solid rgba(233,69,96,0.35); border-radius:20px; padding:3px 12px; font-size:12px; font-weight:600; letter-spacing:1px; text-transform:uppercase; }
</style>
"""

def make_header(active=""):
    links = [
        ("home", "/",           "Home"),
        ("calc", "/calculator", "Calculator"),
        ("pwd",  "/password",   "🔐 Password"),
        ("blog", "/blog",       "📝 Blog"),
    ]
    nav_html = "".join(
        f'<a href="{href}" {"class=active" if active==key else ""}>{label}</a>'
        for key, href, label in links
    )
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


# ── HOME ──────────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    content = """
    <style>
      #particle-canvas { position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:0; }
      .hero { position:relative; z-index:1; text-align:center; animation:fadeUp 1s ease both; }
      @keyframes fadeUp { from{opacity:0;transform:translateY(30px)} to{opacity:1;transform:translateY(0)} }
      .hero-title { font-family:'Orbitron',sans-serif; font-size:62px; color:var(--red); animation:glow 2.5s ease-in-out infinite alternate; line-height:1.1; margin-bottom:16px; }
      @keyframes glow { from{text-shadow:0 0 20px rgba(233,69,96,0.4)} to{text-shadow:0 0 60px rgba(233,69,96,1),0 0 100px rgba(233,69,96,0.4)} }
      .hero-sub { color:var(--text-muted); font-size:20px; letter-spacing:4px; margin-bottom:40px; animation:fadeUp 1s 0.3s ease both; }
      .hero-btns { display:flex; gap:16px; justify-content:center; flex-wrap:wrap; animation:fadeUp 1s 0.5s ease both; }
      .hero-btns a { min-width:160px; text-align:center; }
      .stats { display:flex; gap:50px; margin-top:60px; justify-content:center; animation:fadeUp 1s 0.7s ease both; }
      .stat { text-align:center; }
      .stat-num { font-family:'Orbitron',sans-serif; font-size:32px; color:var(--red); }
      .stat-label { color:var(--text-muted); font-size:13px; letter-spacing:2px; text-transform:uppercase; }
    </style>
    <canvas id="particle-canvas"></canvas>
    <div class="hero">
      <h1 class="hero-title">Hello Salar!!</h1>
      <p class="hero-sub">Developer · Builder · Creator</p>
      <div class="hero-btns">
        <a href="/blog" class="btn">📝 Read Blog</a>
        <a href="/calculator" class="btn purple">Calculator</a>
        <a href="/password" class="btn purple">🔐 Password Gen</a>
      </div>
      <div class="stats">
        <div class="stat"><div class="stat-num">4+</div><div class="stat-label">Pages Built</div></div>
        <div class="stat"><div class="stat-num">3</div><div class="stat-label">Blog Posts</div></div>
        <div class="stat"><div class="stat-num">1</div><div class="stat-label">Live Website</div></div>
      </div>
    </div>
    <script>
      const canvas=document.getElementById('particle-canvas'),ctx=canvas.getContext('2d');
      let particles=[];
      function resize(){canvas.width=window.innerWidth;canvas.height=window.innerHeight;}
      resize(); window.addEventListener('resize',resize);
      class Particle{
        constructor(){this.reset();}
        reset(){this.x=Math.random()*canvas.width;this.y=Math.random()*canvas.height;this.r=Math.random()*2+0.5;this.dx=(Math.random()-0.5)*0.6;this.dy=(Math.random()-0.5)*0.6;this.alpha=Math.random()*0.5+0.1;}
        update(){this.x+=this.dx;this.y+=this.dy;if(this.x<0||this.x>canvas.width||this.y<0||this.y>canvas.height)this.reset();}
        draw(){ctx.beginPath();ctx.arc(this.x,this.y,this.r,0,Math.PI*2);ctx.fillStyle=`rgba(233,69,96,${this.alpha})`;ctx.fill();}
      }
      for(let i=0;i<120;i++)particles.push(new Particle());
      function drawLines(){
        for(let i=0;i<particles.length;i++)for(let j=i+1;j<particles.length;j++){
          const dx=particles[i].x-particles[j].x,dy=particles[i].y-particles[j].y,d=Math.sqrt(dx*dx+dy*dy);
          if(d<100){ctx.beginPath();ctx.moveTo(particles[i].x,particles[i].y);ctx.lineTo(particles[j].x,particles[j].y);ctx.strokeStyle=`rgba(233,69,96,${0.12*(1-d/100)})`;ctx.lineWidth=0.5;ctx.stroke();}
        }
      }
      function animate(){ctx.clearRect(0,0,canvas.width,canvas.height);particles.forEach(p=>{p.update();p.draw();});drawLines();requestAnimationFrame(animate);}
      animate();
    </script>
    """
    return page(content, "home")


# ── BLOG LIST ─────────────────────────────────────────────────────────────────

@app.route("/blog")
def blog():
    cards = ""
    for post in reversed(blog_posts):
        cards += f"""
        <a href="/blog/{post['id']}" class="blog-card">
          <div class="blog-card-top">
            <span class="tag">{post['tag']}</span>
            <span class="blog-date">{post['date']}</span>
          </div>
          <h2 class="blog-title">{post['title']}</h2>
          <p class="blog-summary">{post['summary']}</p>
          <span class="read-more">Read more →</span>
        </a>"""

    content = f"""
    <style>
      .blog-wrap {{ width:100%; max-width:720px; }}
      .blog-header {{ text-align:center; margin-bottom:40px; }}
      .blog-header h1 {{ font-size:42px; }}
      .blog-header p {{ color:var(--text-muted); font-size:17px; letter-spacing:1px; }}
      .blog-card {{ display:block; text-decoration:none; background:linear-gradient(145deg,var(--bg2),var(--bg3)); border:1px solid rgba(233,69,96,0.15); border-radius:14px; padding:28px 32px; margin-bottom:20px; transition:all 0.3s; position:relative; overflow:hidden; }}
      .blog-card::before {{ content:''; position:absolute; top:0; left:0; width:4px; height:100%; background:linear-gradient(180deg,var(--red),var(--purple)); opacity:0; transition:opacity 0.3s; }}
      .blog-card:hover {{ transform:translateY(-4px); border-color:rgba(233,69,96,0.4); box-shadow:0 16px 40px rgba(0,0,0,0.4); }}
      .blog-card:hover::before {{ opacity:1; }}
      .blog-card-top {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; }}
      .blog-date {{ color:var(--text-muted); font-size:13px; letter-spacing:1px; }}
      .blog-title {{ font-family:'Orbitron',sans-serif; color:white; font-size:20px; margin-bottom:10px; line-height:1.3; }}
      .blog-summary {{ color:var(--text-muted); font-size:16px; line-height:1.6; margin-bottom:16px; }}
      .read-more {{ color:var(--red); font-size:14px; font-weight:600; letter-spacing:1px; }}
      .write-btn {{ text-align:center; margin-top:10px; }}
    </style>
    <div class="blog-wrap">
      <div class="blog-header">
        <h1>📝 Blog</h1>
        <p>Thoughts, projects, and lessons from my coding journey</p>
      </div>
      {cards}
      <div class="write-btn"><a href="/blog/new" class="btn">+ Write New Post</a></div>
    </div>"""
    return page(content, "blog")


# ── BLOG POST ─────────────────────────────────────────────────────────────────

@app.route("/blog/<int:post_id>")
def blog_post(post_id):
    post = next((p for p in blog_posts if p["id"] == post_id), None)
    if not post:
        return redirect(url_for("blog"))
    content = f"""
    <style>
      .post-wrap {{ max-width:680px; width:100%; }}
      .post-meta {{ display:flex; gap:16px; align-items:center; margin-bottom:20px; }}
      .post-date {{ color:var(--text-muted); font-size:14px; letter-spacing:1px; }}
      .post-title {{ font-family:'Orbitron',sans-serif; font-size:34px; color:var(--red); line-height:1.25; margin-bottom:28px; text-shadow:0 0 20px rgba(233,69,96,0.4); }}
      .post-body {{ color:#c8d6e5; font-size:18px; line-height:1.8; }}
      .divider {{ border:none; border-top:1px solid rgba(233,69,96,0.15); margin:32px 0; }}
    </style>
    <div class="post-wrap">
      <div class="post-meta"><span class="tag">{post['tag']}</span><span class="post-date">{post['date']}</span></div>
      <h1 class="post-title">{post['title']}</h1>
      <hr class="divider">
      <div class="post-body">{post['content']}</div>
      <a href="/blog" class="btn" style="margin-top:40px;display:inline-block;">← Back to Blog</a>
    </div>"""
    return page(content, "blog")


# ── NEW POST ──────────────────────────────────────────────────────────────────

@app.route("/blog/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        title   = request.form.get("title", "").strip()
        tag     = request.form.get("tag", "General").strip()
        summary = request.form.get("summary", "").strip()
        body    = request.form.get("body", "").strip()
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
    <style>
      .new-post-card { width:100%; max-width:640px; text-align:left; }
      .field { margin-bottom:20px; }
      .field label { display:block; color:var(--text-muted); font-size:14px; letter-spacing:1px; text-transform:uppercase; margin-bottom:8px; }
      .field input, .field textarea { width:100%; }
      .field textarea { min-height:180px; }
    </style>
    <h1 style="font-size:36px;">Write New Post</h1>
    <div class="card new-post-card">
      <form method="POST">
        <div class="field"><label>Title</label><input type="text" name="title" placeholder="Your post title..."></div>
        <div class="field"><label>Tag</label><input type="text" name="tag" placeholder="e.g. Python, Project, Life"></div>
        <div class="field"><label>Summary (optional)</label><input type="text" name="summary" placeholder="Short description shown on blog list..."></div>
        <div class="field"><label>Content</label><textarea name="body" placeholder="Write your post here..."></textarea></div>
        <button type="submit" class="btn" style="width:100%;">Publish Post</button>
      </form>
    </div>"""
    return page(content, "blog")


# ── CALCULATOR ────────────────────────────────────────────────────────────────

@app.route("/calculator")
def calculator():
    content = """
    <style>
      #display { width:290px; padding:15px; font-size:28px; text-align:right; background:var(--bg4); color:var(--red); border:1px solid rgba(233,69,96,0.3); border-radius:8px; margin-bottom:14px; font-family:'Orbitron',monospace; outline:none; }
      .calc-grid button { width:64px; height:64px; margin:4px; font-size:20px; border:none; border-radius:8px; cursor:pointer; font-family:'Rajdhani',sans-serif; font-weight:700; transition:all 0.15s; }
      .num { background:linear-gradient(135deg,var(--red),var(--red-dark)); color:white; }
      .op  { background:linear-gradient(135deg,var(--purple),var(--purple-dark)); color:white; }
      .calc-grid button:hover  { transform:scale(1.08); box-shadow:0 4px 15px rgba(233,69,96,0.4); }
      .calc-grid button:active { transform:scale(0.95); }
    </style>
    <h1 style="font-size:36px;">Calculator</h1>
    <div class="card">
      <input id="display" type="text" value="0" readonly><br>
      <div class="calc-grid">
        <button class="num" onclick="press('7')">7</button><button class="num" onclick="press('8')">8</button><button class="num" onclick="press('9')">9</button><button class="op" onclick="press('+')">+</button><br>
        <button class="num" onclick="press('4')">4</button><button class="num" onclick="press('5')">5</button><button class="num" onclick="press('6')">6</button><button class="op" onclick="press('-')">−</button><br>
        <button class="num" onclick="press('1')">1</button><button class="num" onclick="press('2')">2</button><button class="num" onclick="press('3')">3</button><button class="op" onclick="press('*')">×</button><br>
        <button class="op" onclick="clearD()">C</button><button class="num" onclick="press('0')">0</button><button class="op" onclick="calc()">=</button><button class="op" onclick="press('/')">÷</button>
      </div>
    </div>
    <script>
      function press(v){var d=document.getElementById('display');d.value=d.value=='0'?v:d.value+v;}
      function clearD(){document.getElementById('display').value='0';}
      function calc(){try{document.getElementById('display').value=eval(document.getElementById('display').value);}catch(e){document.getElementById('display').value='Error';}}
    </script>"""
    return page(content, "calc")


# ── PASSWORD ──────────────────────────────────────────────────────────────────

@app.route("/password")
def password():
    content = """
    <style>
      .pw-card { width:380px; text-align:left; }
      .field-label { color:var(--text-muted); font-size:15px; letter-spacing:1px; display:block; margin-bottom:6px; }
      .pw-card input[type=number] { width:100%; margin-bottom:18px; }
      .options { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:20px; }
      .opt { display:flex; align-items:center; gap:8px; background:var(--bg4); padding:10px 14px; border-radius:8px; border:1px solid rgba(233,69,96,0.15); cursor:pointer; transition:border-color 0.2s; }
      .opt:hover { border-color:rgba(233,69,96,0.5); }
      .opt input { accent-color:var(--red); width:16px; height:16px; }
      .opt span { color:var(--text-muted); font-size:15px; font-weight:600; }
      #result { width:100%; padding:12px 15px; font-size:14px; font-family:'Courier New',monospace; background:var(--bg4); color:var(--red); border:1px solid rgba(233,69,96,0.3); border-radius:8px; margin-bottom:6px; text-align:center; min-height:46px; word-break:break-all; letter-spacing:2px; }
      #copy-msg { color:#4caf50; font-size:13px; height:18px; margin-bottom:12px; text-align:center; }
      .btn-row { display:flex; gap:10px; }
      .btn-row .btn { flex:1; padding:12px; font-size:15px; text-align:center; }
    </style>
    <h1 style="font-size:34px;">🔐 Password Generator</h1>
    <div class="card pw-card">
      <span class="field-label">Password Length</span>
      <input type="number" id="length" value="12" min="4" max="64">
      <div class="options">
        <label class="opt"><input type="checkbox" id="lower" checked><span>Lowercase</span></label>
        <label class="opt"><input type="checkbox" id="upper" checked><span>Uppercase</span></label>
        <label class="opt"><input type="checkbox" id="digits" checked><span>Digits</span></label>
        <label class="opt"><input type="checkbox" id="symbols" checked><span>Symbols</span></label>
      </div>
      <div id="result">Click Generate!!</div>
      <div id="copy-msg"></div>
      <div class="btn-row">
        <button class="btn" onclick="generatePassword()">Generate</button>
        <button class="btn purple" onclick="copyPassword()">Copy</button>
      </div>
    </div>
    <script>
      function generatePassword(){
        const len=parseInt(document.getElementById('length').value);
        let chars='';
        if(document.getElementById('lower').checked) chars+='abcdefghijklmnopqrstuvwxyz';
        if(document.getElementById('upper').checked) chars+='ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        if(document.getElementById('digits').checked) chars+='0123456789';
        if(document.getElementById('symbols').checked) chars+='!@#$%^&*()_+-=[]{}|;:,.<>?';
        if(!chars){document.getElementById('result').innerText='Select at least one option!!';return;}
        let pwd='';
        for(let i=0;i<len;i++) pwd+=chars[Math.floor(Math.random()*chars.length)];
        document.getElementById('result').innerText=pwd;
        document.getElementById('copy-msg').innerText='';
      }
      function copyPassword(){
        const pwd=document.getElementById('result').innerText;
        if(pwd.includes('Click')||pwd.includes('Select')) return;
        navigator.clipboard.writeText(pwd).then(()=>{
          const m=document.getElementById('copy-msg');
          m.innerText='Copied to clipboard!';
          setTimeout(()=>m.innerText='',2000);
        });
      }
    </script>"""
    return page(content, "pwd")


# ── ABOUT ─────────────────────────────────────────────────────────────────────

@app.route("/about")
def about():
    content = """
    <style>
      .about-card { max-width:480px; text-align:center; }
      .about-card p { color:var(--text-muted); font-size:19px; margin:12px 0; letter-spacing:1px; line-height:1.7; }
      .about-card p span { color:var(--red); font-weight:700; }
    </style>
    <h1 style="font-size:42px;">About Me!!</h1>
    <div class="card about-card">
      <p>My name is <span>Salar!!</span></p>
      <p>I am learning <span>Python and Flask!!</span></p>
      <p>I build real websites and apps!!</p>
    </div>"""
    return page(content)


# ── CONTACT ───────────────────────────────────────────────────────────────────

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
    <style>
      .contact-card { width:380px; text-align:center; }
      .contact-card input { width:100%; margin-bottom:16px; text-align:center; }
    </style>
    <h1 style="font-size:42px;">Contact Me!!</h1>
    <div class="card contact-card">
      <form method="POST">
        <input type="text" name="name" placeholder="Your name!!">
        <button type="submit" class="btn" style="width:100%;margin-top:4px;">Submit!!</button>
      </form>
    </div>"""
    return page(content)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
