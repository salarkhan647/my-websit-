from flask import Flask, request
import os
app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <body style="background-color: #1a1a2e; text-align: center; font-family: Arial;">
    <h1 style="color: #e94560; font-size: 50px; margin-top: 50px;">Hello Salar!!</h1>
    <p style="color: white; font-size: 20px;">Welcome to my website!!</p>
    <div style="margin-top: 30px;">
        <a href="/about" style="background-color: #e94560; color: white; padding: 10px 20px; margin: 10px; text-decoration: none; border-radius: 5px;">About</a>
        <a href="/contact" style="background-color: #e94560; color: white; padding: 10px 20px; margin: 10px; text-decoration: none; border-radius: 5px;">Contact</a>
        <a href="/calculator" style="background-color: #e94560; color: white; padding: 10px 20px; margin: 10px; text-decoration: none; border-radius: 5px;">Calculator</a>
    </div>
    
    </body>
    </html>
    """

@app.route("/about")
def about():
    return """
    <html>
    <body style="background-color: #1a1a2e; text-align: center; font-family: Arial;">
        <h1 style="color: #e94560; font-size: 50px; margin-top: 50px;">About Me!!</h1>
        <p style="color: white; font-size: 20px;">My name is Salar!!</p>
        <p style="color: white; font-size: 20px;">I am learning Python and Flask!!</p>
        <p style="color: white; font-size: 20px;">I build real websites and apps!!</p>
        <div style="margin-top: 30px;">
            <a href="/" style="background-color: #e94560; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Go back home!!</a>
        </div>
     </body>
    </html>
    """

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        return """
        <html>
        <body style="background-color: #1a1a2e; text-align: center; font-family: Arial;">
            <h1 style="color: #e94560; font-size: 50px; margin-top: 50px;">Hello """ + name + """!!</h1>
            <p style="color: white; font-size: 20px;">Thanks for contacting me!!</p>
            <a href="/" style="background-color: #e94560; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Go back home!!</a>
        </body>
        </html>
        """
    return """
    <html>
    <body style="background-color: #1a1a2e; text-align: center; font-family: Arial;">
        <h1 style="color: #e94560; font-size: 50px; margin-top: 50px;">Contact Me!!</h1>
        <form method="POST">
            <input type="text" name="name" placeholder="Your name!!" style="padding: 10px; font-size: 18px; border-radius: 5px; border: none; margin: 10px;">
            <button type="submit" style="background-color: #e94560; color: white; padding: 10px 20px; font-size: 18px; border: none; border-radius: 5px;">Submit!!</button>
        </form>
        <a href="/" style="color: #e94560;">Go back home!!</a>
    </body>
    </html>
    """

@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    return """
    <html>
    <body style="background-color: #1a1a2e; text-align: center; font-family: Arial;">
        <h1 style="color: #e94560; font-size: 40px; margin-top: 30px;">Calculator!!</h1>
        
        <div style="display: inline-block; background-color: #16213e; padding: 20px; border-radius: 10px;">
            
            <input id="display" type="text" value="0" readonly
            style="width: 280px; padding: 15px; font-size: 30px; text-align: right; 
            background-color: #0f3460; color: white; border: none; border-radius: 5px; margin-bottom: 10px;">
            
            <div>
                <button onclick="press('7')" style="width:60px;height:60px;margin:5px;font-size:20px;background-color:#e94560;color:white;border:none;border-radius:5px;">7</button>
                <button onclick="press('8')" style="width:60px;height:60px;margin:5px;font-size:20px;background-color:#e94560;color:white;border:none;border-radius:5px;">8</button>
                <button onclick="press('9')" style="width:60px;height:60px;margin:5px;font-size:20px;background-color:#e94560;color:white;border:none;border-radius:5px;">9</button>
                <button onclick="press('+')" style="width:60px;height:60px;margin:5px;font-size:20px;background-color:#533483;color:white;border:none;border-radius:5px;">+</button>
            </div>
            <div>
                <button onclick="press('4')" style="width:60px;height:60px;margin:5px;font-size:20px;background-color:#e94560;color:white;border:none;border-radius:5px;">4</button>
                <button onclick="press('5')" style="width:60px;height:60px;margin:5px;font-size:20px;background-color:#e94560;color:white;border:none;border-radius:5px;">5</button>
                <button onclick="press('6')" style="width:60px;height:60px;margin:5px;font-size:20px;background-color:#e94560;color:white;border:none;border-radius:5px;">6</button>
                <button onclick="press('-')" style="width:60px;height:60px;margin:5px;font-size:20px;background-color:#533483;color:white;border:none;border-radius:5px;">-</button>
            </div>
            <div>
                <button onclick="press('1')" style="width:60px;height:60px;margin:5px;font-size:20px;background-color:#e94560;color:white;border:none;border-radius:5px;">1</button>
                <button onclick="press('2')" style="width:60px;height:60px;margin:5px;font-size:20px;background-color:#e94560;color:white;border:none;border-radius:5px;">2</button>
                <button onclick="press('3')" style="width:60px;height:60px;margin:5px;font-size:20px;background-color:#e94560;color:white;border:none;border-radius:5px;">3</button>
                <button onclick="press('*')" style="width:60px;height:60px;margin:5px;font-size:20px;background-color:#533483;color:white;border:none;border-radius:5px;">*</button>
            </div>
            <div>
                <button onclick="clearDisplay()" style="width:60px;height:60px;margin:5px;font-size:20px;background-color:#e94560;color:white;border:none;border-radius:5px;">C</button>
                <button onclick="press('0')" style="width:60px;height:60px;margin:5px;font-size:20px;background-color:#e94560;color:white;border:none;border-radius:5px;">0</button>
                <button onclick="calculate()" style="width:60px;height:60px;margin:5px;font-size:20px;background-color:#533483;color:white;border:none;border-radius:5px;">=</button>
                <button onclick="press('/')" style="width:60px;height:60px;margin:5px;font-size:20px;background-color:#533483;color:white;border:none;border-radius:5px;">/</button>
            </div>
        </div>

        <br><br>
        <a href="/" style="background-color: #e94560; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Go back home!!</a>

        <script>
            function press(val) {
                var display = document.getElementById('display');
                if (display.value == '0') {
                    display.value = val;
                } else {
                    display.value += val;
                }
            }

            function clearDisplay() {
                document.getElementById('display').value = '0';
            }

            function calculate() {
                try {
                    var result = eval(document.getElementById('display').value);
                    document.getElementById('display').value = result;
                } catch(e) {
                    document.getElementById('display').value = 'Error';
                }
            }
        </script>
    </body>
    </html>
    """
