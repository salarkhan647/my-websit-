from flask import Flask, request
import os

app = Flask(__name__)

# ── Shared styles (goes in <head> only) ─────────────────────────────────────

STYLES = """
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@400;600&display=swap" rel="stylesheet">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    background: #1a1a2e;
    font-family: 'Rajdhani', sans-serif;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background-image: radial-gradient(circle at 20% 50%, #16213e 0%, #1a1a2e 50%, #0f3460 100%);
  }

  /* ── HEADER ── */
  header {
    position: sticky; top: 0; z-index: 100;
    background: rgba(10, 22, 40, 0.95);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(233,69,96,0.25);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 40px;
    height: 64px;
  }
  .logo {
    font-family: 'Orbitron', sans-serif;
    color: #e94560;
    font-size: 20px;
    text-decoration: none;
    letter-spacing: 2px;
    text-shadow: 0 0 14px rgba(233,69,96,0.5);
  }
  nav { display: flex; gap: 6px; align-items: center; }
  nav a {
    color: #a0aec0;
    text-decoration: none;
    padding: 8px 18px;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    transition: all 0.25s;
    border: 1px solid transparent;
  }
  nav a:hover, nav a.active {
    color: #fff;
    background: rgba(233,69,96,0.15);
    border-color: rgba(233,69,96,0.4);
    text-shadow: 0 0 8px rgba(233,69,96,0.6);
  }

  /* ── MAIN ── */
  main {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 50px 20px;
  }

  /* ── FOOTER ── */
  footer {
    background: rgba(10, 22, 40, 0.95);
    border-top: 1px solid rgba(233,69,96,0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 40px;
    padding: 22px 40px;
  }
  footer a {
    color: #a0aec0;
    text-decoration: none;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    transition: color 0.2s;
  }
  footer a:hover { color: #e94560; }
  footer .dot { color: rgba(233,69,96,0.35); font-size: 18px; }
  footer .copy { color: #a0aec0; font-size: 13px; }

  /* ── SHARED COMPONENTS ── */
  h1 {
    font-family: 'Orbitron', sans-serif;
    color: #e94560;
    text-shadow: 0 0 30px rgba(233,69,96,0.5);
    margin-bottom: 20px;
  }
  .card {
    background: linear-gradient(145deg, #16213e, #0f3460);
    border-radius: 16px;
    border: 1px solid rgba(233,69,96,0.2);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    padding: 35px 45px;
  }
  .btn {
    display: inline-block;
    background: linear-gradient(135deg, #e94560, #c73652);
    color: white;
    padding: 11px 26px;
    text-decoration: none;
    border-radius: 8px;
    font-size: 15px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    border: none;
    cursor: pointer;
    font-family: 'Rajdhani', sans-serif;
    transition: all 0.3s;
  }
  .btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(233,69,96,0.4); }
  .btn.purple { background: linear-gradient(135deg, #533483, #3d2468); }
  .btn.purple:hover { box-shadow: 0 6px 20px rgba(83,52,131,0.5); }
  input[type=text], input[type=number] {
    background: #0a1628;
    color: white;
    border: 1px solid rgba(233,69,96,0.3);
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 16px;
    font-family: 'Rajdhani', sans-serif;
    outline: none;
    transition: border-color 0.2s;
  }
  input:focus { border-color: #e94560; box-shadow: 0 0 10px rgba(233,69,96,0.3); }
</style>
"""

def make_header(active=""):
    home_cls  = 'class="active"' if active == "home" else ""
    calc_cls  = 'class="active"' if active == "calc" else ""
    pwd_cls   = 'class="active"' if active == "pwd"  else ""
    return f"""
    <header>
      <a class="logo" href="/">SALAR.DEV</a>
      <nav>
        <a href="/" {home_cls}>Home</a>
        <a href="/calculator" {calc_cls}>Calculator</a>
        <a href="/password" {pwd_cls}>🔐 Password</a>
      </nav>
    </header>
    """

FOOTER = """
<footer>
  <a href="/about">About Me</a>
  <span class="dot">·</span>
  <a href="/contact">Contact</a>
  <span class="dot">·</span>
  <span class="copy">© 2026 Salar</span>
</footer>
"""

def page(content, active=""):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Salar.dev</title>
      {STYLES}
    </head>
    <body>
      {make_header(active)}
      <main>{content}</main>
      {FOOTER}
    </body>
    </html>
    """


# ── ROUTES ──────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    content = """
    <style>
      .hero-title { font-size: 58px; animation: glow 2s ease-in-out infinite alternate; }
      @keyframes glow {
        from { text-shadow: 0 0 20px rgba(233,69,96,0.4); }
        to   { text-shadow: 0 0 50px rgba(233,69,96,0.9), 0 0 80px rgba(233,69,96,0.3); }
      }
      .sub { color: #a0aec0; font-size: 20px; letter-spacing: 3px; margin-bottom: 10px; }
    </style>
    <h1 class="hero-title">Hello Salar!!</h1>
    <p class="sub">Welcome to my website!!</p>
    """
    return page(content, "home")


@app.route("/calculator")
def calculator():
    content = """
    <style>
      #display { width:290px; padding:15px; font-size:28px; text-align:right;
        background:#0a1628; color:#e94560; border:1px solid rgba(233,69,96,0.3);
        border-radius:8px; margin-bottom:14px; font-family:'Orbitron',monospace; outline:none; }
      .calc-grid button { width:64px; height:64px; margin:4px; font-size:20px;
        border:none; border-radius:8px; cursor:pointer;
        font-family:'Rajdhani',sans-serif; font-weight:700; transition:all 0.15s; }
      .num { background:linear-gradient(135deg,#e94560,#c73652); color:white; }
      .op  { background:linear-gradient(135deg,#533483,#3d2468); color:white; }
      .calc-grid button:hover  { transform:scale(1.08); box-shadow:0 4px 15px rgba(233,69,96,0.4); }
      .calc-grid button:active { transform:scale(0.95); }
    </style>
    <h1 style="font-size:36px;">Calculator</h1>
    <div class="card">
      <input id="display" type="text" value="0" readonly><br>
      <div class="calc-grid">
        <button class="num" onclick="press('7')">7</button>
        <button class="num" onclick="press('8')">8</button>
        <button class="num" onclick="press('9')">9</button>
        <button class="op"  onclick="press('+')">+</button><br>
        <button class="num" onclick="press('4')">4</button>
        <button class="num" onclick="press('5')">5</button>
        <button class="num" onclick="press('6')">6</button>
        <button class="op"  onclick="press('-')">−</button><br>
        <button class="num" onclick="press('1')">1</button>
        <button class="num" onclick="press('2')">2</button>
        <button class="num" onclick="press('3')">3</button>
        <button class="op"  onclick="press('*')">×</button><br>
        <button class="op"  onclick="clearD()">C</button>
        <button class="num" onclick="press('0')">0</button>
        <button class="op"  onclick="calc()">=</button>
        <button class="op"  onclick="press('/')">÷</button>
      </div>
    </div>
    <script>
      function press(v){ var d=document.getElementById('display'); d.value=d.value=='0'?v:d.value+v; }
      function clearD(){ document.getElementById('display').value='0'; }
      function calc(){ try{ document.getElementById('display').value=eval(document.getElementById('display').value); }catch(e){ document.getElementById('display').value='Error'; } }
    </script>
    """
    return page(content, "calc")


@app.route("/password")
def password():
    content = """
    <style>
      .pw-card { width:380px; text-align:left; }
      .pw-card .field-label { color:#a0aec0; font-size:15px; letter-spacing:1px; display:block; margin-bottom:6px; }
      .pw-card input[type=number] { width:100%; margin-bottom:18px; }
      .options { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:20px; }
      .opt { display:flex; align-items:center; gap:8px; background:#0a1628;
        padding:10px 14px; border-radius:8px; border:1px solid rgba(233,69,96,0.15);
        cursor:pointer; transition:border-color 0.2s; }
      .opt:hover { border-color:rgba(233,69,96,0.5); }
      .opt input { accent-color:#e94560; width:16px; height:16px; }
      .opt span { color:#a0aec0; font-size:15px; font-weight:600; }
      #result { width:100%; padding:12px 15px; font-size:14px; font-family:'Courier New',monospace;
        background:#0a1628; color:#e94560; border:1px solid rgba(233,69,96,0.3);
        border-radius:8px; margin-bottom:6px; text-align:center; min-height:46px;
        word-break:break-all; letter-spacing:2px; }
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
        if(document.getElementById('lower').checked)   chars+='abcdefghijklmnopqrstuvwxyz';
        if(document.getElementById('upper').checked)   chars+='ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        if(document.getElementById('digits').checked)  chars+='0123456789';
        if(document.getElementById('symbols').checked) chars+='!@#$%^&*()_+-=[]{}|;:,.<>?';
        if(!chars){ document.getElementById('result').innerText='Select at least one option!!'; return; }
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
          m.innerText='✅ Copied to clipboard!';
          setTimeout(()=>m.innerText='',2000);
        });
      }
    </script>
    """
    return page(content, "pwd")


@app.route("/about")
def about():
    content = """
    <style>
      .about-card { max-width:480px; text-align:center; }
      .about-card p { color:#a0aec0; font-size:19px; margin:12px 0; letter-spacing:1px; line-height:1.7; }
      .about-card p span { color:#e94560; font-weight:700; }
    </style>
    <h1 style="font-size:42px;">About Me!!</h1>
    <div class="card about-card">
      <p>My name is <span>Salar!!</span></p>
      <p>I am learning <span>Python and Flask!!</span></p>
      <p>I build real websites and apps!!</p>
    </div>
    """
    return page(content)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        content = f"""
        <h1 style="font-size:46px;">Hello {name}!!</h1>
        <p style="color:#a0aec0; font-size:20px; margin-bottom:30px;">Thanks for contacting me!!</p>
        <a href="/" class="btn">← Home</a>
        """
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
        <button type="submit" class="btn" style="width:100%;">Submit!!</button>
      </form>
    </div>
    """
    return page(content)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
