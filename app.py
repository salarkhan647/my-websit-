from flask import Flask, request
import os
app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Rajdhani:wght@400;600&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                background-color: #1a1a2e;
                text-align: center;
                font-family: 'Rajdhani', Arial, sans-serif;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                background-image: radial-gradient(circle at 20% 50%, #16213e 0%, #1a1a2e 50%, #0f3460 100%);
            }
            h1 {
                font-family: 'Orbitron', Arial, sans-serif;
                color: #e94560;
                font-size: 52px;
                margin-bottom: 10px;
                text-shadow: 0 0 30px rgba(233,69,96,0.5);
                animation: glow 2s ease-in-out infinite alternate;
            }
            @keyframes glow {
                from { text-shadow: 0 0 20px rgba(233,69,96,0.4); }
                to { text-shadow: 0 0 40px rgba(233,69,96,0.8), 0 0 60px rgba(233,69,96,0.3); }
            }
            p { color: #a0aec0; font-size: 20px; margin-bottom: 40px; letter-spacing: 2px; }
            .nav { display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; }
            .nav a {
                background: linear-gradient(135deg, #e94560, #c73652);
                color: white;
                padding: 12px 24px;
                text-decoration: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                letter-spacing: 1px;
                text-transform: uppercase;
                transition: all 0.3s;
                border: 1px solid rgba(233,69,96,0.3);
            }
            .nav a:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(233,69,96,0.4); }
        </style>
    </head>
    <body>
        <h1>Hello Salar!!</h1>
        <p>Welcome to my website!!</p>
        <div class="nav">
            <a href="/calculator">Calculator</a>
            <a href="/about">About</a>
            <a href="/contact">Contact</a>
            <a href="/password">🔐 Password Generator</a>
        </div>
    </body>
    </html>
    """

@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    return """
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Rajdhani:wght@400;600&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                background-color: #1a1a2e;
                text-align: center;
                font-family: 'Rajdhani', Arial, sans-serif;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                background-image: radial-gradient(circle at 20% 50%, #16213e 0%, #1a1a2e 50%, #0f3460 100%);
            }
            h1 { font-family: 'Orbitron', Arial, sans-serif; color: #e94560; font-size: 40px; margin-bottom: 30px; text-shadow: 0 0 20px rgba(233,69,96,0.5); }
            .calc-wrap { background: linear-gradient(145deg, #16213e, #0f3460); padding: 25px; border-radius: 16px; border: 1px solid rgba(233,69,96,0.2); box-shadow: 0 20px 60px rgba(0,0,0,0.5); }
            #display { width: 290px; padding: 15px; font-size: 30px; text-align: right; background-color: #0a1628; color: #e94560; border: 1px solid rgba(233,69,96,0.3); border-radius: 8px; margin-bottom: 15px; font-family: 'Orbitron', monospace; }
            button { width: 62px; height: 62px; margin: 4px; font-size: 20px; border: none; border-radius: 8px; cursor: pointer; font-family: 'Rajdhani', Arial, sans-serif; font-weight: 600; transition: all 0.15s; }
            .num { background: linear-gradient(135deg, #e94560, #c73652); color: white; }
            .op { background: linear-gradient(135deg, #533483, #3d2468); color: white; }
            button:hover { transform: scale(1.08); box-shadow: 0 4px 15px rgba(233,69,96,0.4); }
            button:active { transform: scale(0.95); }
            .back-btn { display: inline-block; margin-top: 25px; background: linear-gradient(135deg, #e94560, #c73652); color: white; padding: 10px 24px; text-decoration: none; border-radius: 8px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; transition: all 0.3s; }
            .back-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(233,69,96,0.4); }
        </style>
    </head>
    <body>
        <h1>Calculator!!</h1>
        <div class="calc-wrap">
            <input id="display" type="text" value="0" readonly>
            <div>
                <button class="num" onclick="press('7')">7</button>
                <button class="num" onclick="press('8')">8</button>
                <button class="num" onclick="press('9')">9</button>
                <button class="op" onclick="press('+')">+</button>
            </div>
            <div>
                <button class="num" onclick="press('4')">4</button>
                <button class="num" onclick="press('5')">5</button>
                <button class="num" onclick="press('6')">6</button>
                <button class="op" onclick="press('-')">-</button>
            </div>
            <div>
                <button class="num" onclick="press('1')">1</button>
                <button class="num" onclick="press('2')">2</button>
                <button class="num" onclick="press('3')">3</button>
                <button class="op" onclick="press('*')">*</button>
            </div>
            <div>
                <button class="op" onclick="clearDisplay()">C</button>
                <button class="num" onclick="press('0')">0</button>
                <button class="op" onclick="calculate()">=</button>
                <button class="op" onclick="press('/')">/</button>
            </div>
        </div>
        <a href="/" class="back-btn">← Home</a>
        <script>
            function press(val) {
                var d = document.getElementById('display');
                d.value = d.value == '0' ? val : d.value + val;
            }
            function clearDisplay() { document.getElementById('display').value = '0'; }
            function calculate() {
                try { document.getElementById('display').value = eval(document.getElementById('display').value); }
                catch(e) { document.getElementById('display').value = 'Error'; }
            }
        </script>
    </body>
    </html>
    """

@app.route("/about")
def about():
    return """
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Rajdhani:wght@400;600&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                background-color: #1a1a2e;
                text-align: center;
                font-family: 'Rajdhani', Arial, sans-serif;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                background-image: radial-gradient(circle at 20% 50%, #16213e 0%, #1a1a2e 50%, #0f3460 100%);
            }
            h1 { font-family: 'Orbitron', Arial, sans-serif; color: #e94560; font-size: 46px; margin-bottom: 30px; text-shadow: 0 0 20px rgba(233,69,96,0.5); }
            .card { background: linear-gradient(145deg, #16213e, #0f3460); padding: 35px 50px; border-radius: 16px; border: 1px solid rgba(233,69,96,0.2); box-shadow: 0 20px 60px rgba(0,0,0,0.5); max-width: 500px; }
            p { color: #a0aec0; font-size: 20px; margin: 10px 0; letter-spacing: 1px; line-height: 1.7; }
            p span { color: #e94560; font-weight: 600; }
            .back-btn { display: inline-block; margin-top: 30px; background: linear-gradient(135deg, #e94560, #c73652); color: white; padding: 10px 24px; text-decoration: none; border-radius: 8px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; transition: all 0.3s; }
            .back-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(233,69,96,0.4); }
        </style>
    </head>
    <body>
        <h1>About Me!!</h1>
        <div class="card">
            <p>My name is <span>Salar!!</span></p>
            <p>I am learning <span>Python and Flask!!</span></p>
            <p>I can build  websites and apps!!</p>
            <p> we provide ai servise!!</p>
        </div>
        <a href="/" class="back-btn">← Home</a>
    </body>
    </html>
    """

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        return """
        <html>
        <head>
            <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Rajdhani:wght@400;600&display=swap" rel="stylesheet">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { background-color: #1a1a2e; text-align: center; font-family: 'Rajdhani', Arial, sans-serif; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; background-image: radial-gradient(circle at 20% 50%, #16213e, #1a1a2e, #0f3460); }
                h1 { font-family: 'Orbitron', Arial, sans-serif; color: #e94560; font-size: 46px; margin-bottom: 15px; text-shadow: 0 0 20px rgba(233,69,96,0.5); }
                p { color: #a0aec0; font-size: 20px; margin-bottom: 30px; }
                .back-btn { background: linear-gradient(135deg, #e94560, #c73652); color: white; padding: 10px 24px; text-decoration: none; border-radius: 8px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; transition: all 0.3s; }
                .back-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(233,69,96,0.4); }
            </style>
        </head>
        <body>
            <h1>Hello """ + name + """!!</h1>
            <p>Thanks for contacting me!!</p>
            <a href="/" class="back-btn">← Home</a>
        </body>
        </html>
        """
    return """
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Rajdhani:wght@400;600&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { background-color: #1a1a2e; text-align: center; font-family: 'Rajdhani', Arial, sans-serif; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; background-image: radial-gradient(circle at 20% 50%, #16213e, #1a1a2e, #0f3460); }
            h1 { font-family: 'Orbitron', Arial, sans-serif; color: #e94560; font-size: 46px; margin-bottom: 30px; text-shadow: 0 0 20px rgba(233,69,96,0.5); }
            .card { background: linear-gradient(145deg, #16213e, #0f3460); padding: 35px 50px; border-radius: 16px; border: 1px solid rgba(233,69,96,0.2); box-shadow: 0 20px 60px rgba(0,0,0,0.5); }
            input { padding: 12px 20px; font-size: 18px; border-radius: 8px; border: 1px solid rgba(233,69,96,0.3); background: #0a1628; color: white; margin-bottom: 15px; width: 280px; font-family: 'Rajdhani', Arial, sans-serif; outline: none; }
            input:focus { border-color: #e94560; box-shadow: 0 0 10px rgba(233,69,96,0.3); }
            button { background: linear-gradient(135deg, #e94560, #c73652); color: white; padding: 12px 30px; font-size: 18px; border: none; border-radius: 8px; cursor: pointer; font-family: 'Rajdhani', Arial, sans-serif; font-weight: 600; letter-spacing: 1px; transition: all 0.3s; }
            button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(233,69,96,0.4); }
            .back-link { display: block; margin-top: 20px; color: #e94560; text-decoration: none; font-size: 16px; }
        </style>
    </head>
    <body>
        <h1>Contact Me!!</h1>
        <div class="card">
            <form method="POST">
                <input type="text" name="name" placeholder="Your name!!"><br>
                <button type="submit">Submit!!</button>
            </form>
            <a href="/" class="back-link">← Go back home</a>
        </div>
    </body>
    </html>
    """

@app.route("/password")
def password():
    return """
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Rajdhani:wght@400;600&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                background-color: #1a1a2e;
                text-align: center;
                font-family: 'Rajdhani', Arial, sans-serif;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                background-image: radial-gradient(circle at 20% 50%, #16213e 0%, #1a1a2e 50%, #0f3460 100%);
            }
            h1 { font-family: 'Orbitron', Arial, sans-serif; color: #e94560; font-size: 36px; margin-bottom: 25px; text-shadow: 0 0 20px rgba(233,69,96,0.5); }
            .card { background: linear-gradient(145deg, #16213e, #0f3460); padding: 30px 40px; border-radius: 16px; border: 1px solid rgba(233,69,96,0.2); box-shadow: 0 20px 60px rgba(0,0,0,0.5); width: 380px; }
            label { color: #a0aec0; font-size: 16px; display: block; margin-bottom: 6px; text-align: left; letter-spacing: 1px; }
            input[type=number] { width: 100%; padding: 10px 15px; font-size: 16px; border-radius: 8px; border: 1px solid rgba(233,69,96,0.3); background: #0a1628; color: white; font-family: 'Rajdhani', Arial, sans-serif; outline: none; margin-bottom: 18px; }
            input[type=number]:focus { border-color: #e94560; box-shadow: 0 0 10px rgba(233,69,96,0.3); }
            .options { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px; }
            .option { display: flex; align-items: center; gap: 8px; background: #0a1628; padding: 10px 14px; border-radius: 8px; border: 1px solid rgba(233,69,96,0.15); cursor: pointer; transition: all 0.2s; }
            .option:hover { border-color: rgba(233,69,96,0.5); }
            .option input[type=checkbox] { accent-color: #e94560; width: 16px; height: 16px; cursor: pointer; }
            .option span { color: #a0aec0; font-size: 15px; font-weight: 600; }
            #result { width: 100%; padding: 12px 15px; font-size: 15px; font-family: 'Courier New', monospace; background: #0a1628; color: #e94560; border: 1px solid rgba(233,69,96,0.3); border-radius: 8px; margin-bottom: 15px; letter-spacing: 2px; text-align: center; min-height: 46px; word-break: break-all; }
            .btn-row { display: flex; gap: 10px; }
            .btn { flex: 1; background: linear-gradient(135deg, #e94560, #c73652); color: white; padding: 11px; font-size: 15px; border: none; border-radius: 8px; cursor: pointer; font-family: 'Rajdhani', Arial, sans-serif; font-weight: 600; letter-spacing: 1px; transition: all 0.3s; text-transform: uppercase; }
            .btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(233,69,96,0.4); }
            .btn.copy { background: linear-gradient(135deg, #533483, #3d2468); }
            .btn.copy:hover { box-shadow: 0 6px 20px rgba(83,52,131,0.5); }
            .back-btn { display: inline-block; margin-top: 25px; background: linear-gradient(135deg, #e94560, #c73652); color: white; padding: 10px 24px; text-decoration: none; border-radius: 8px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; transition: all 0.3s; }
            .back-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(233,69,96,0.4); }
            #copy-msg { color: #4caf50; font-size: 14px; margin-top: 8px; height: 18px; transition: opacity 0.3s; }
        </style>
    </head>
    <body>
        <h1>🔐 Password Generator</h1>
        <div class="card">
            <label>Password Length</label>
            <input type="number" id="length" value="12" min="4" max="64">

            <div class="options">
                <label class="option">
                    <input type="checkbox" id="lower" checked>
                    <span>Lowercase</span>
                </label>
                <label class="option">
                    <input type="checkbox" id="upper" checked>
                    <span>Uppercase</span>
                </label>
                <label class="option">
                    <input type="checkbox" id="digits" checked>
                    <span>Digits</span>
                </label>
                <label class="option">
                    <input type="checkbox" id="symbols" checked>
                    <span>Symbols</span>
                </label>
            </div>

            <div id="result">Click Generate!!</div>
            <div id="copy-msg"></div>

            <div class="btn-row">
                <button class="btn" onclick="generatePassword()">Generate</button>
                <button class="btn copy" onclick="copyPassword()">Copy</button>
            </div>
        </div>
        <a href="/" class="back-btn">← Home</a>

        <script>
            function generatePassword() {
                const length = parseInt(document.getElementById('length').value);
                const lower = document.getElementById('lower').checked;
                const upper = document.getElementById('upper').checked;
                const digits = document.getElementById('digits').checked;
                const symbols = document.getElementById('symbols').checked;

                let chars = '';
                if (lower)   chars += 'abcdefghijklmnopqrstuvwxyz';
                if (upper)   chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
                if (digits)  chars += '0123456789';
                if (symbols) chars += '!@#$%^&*()_+-=[]{}|;:,.<>?';

                if (!chars) {
                    document.getElementById('result').innerText = 'Select at least one option!!';
                    return;
                }

                let password = '';
                for (let i = 0; i < length; i++) {
                    password += chars[Math.floor(Math.random() * chars.length)];
                }
                document.getElementById('result').innerText = password;
                document.getElementById('copy-msg').innerText = '';
            }

            function copyPassword() {
                const pwd = document.getElementById('result').innerText;
                if (pwd === 'Click Generate!!' || pwd === 'Select at least one option!!') return;
                navigator.clipboard.writeText(pwd).then(() => {
                    const msg = document.getElementById('copy-msg');
                    msg.innerText = '✅ Copied to clipboard!';
                    setTimeout(() => msg.innerText = '', 2000);
                });
            }
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
