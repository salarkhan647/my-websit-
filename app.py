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
    result = ""
    if request.method == "POST":
        a = float(request.form["a"])
        b = float(request.form["b"])
        operation = request.form["operation"]
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            if b == 0:
                result = "Error!! Cannot divide by zero!!"
            else:
                result = a / b
    return """
    <html>
    <body style="background-color: #1a1a2e; text-align: center; font-family: Arial;">
        <h1 style="color: #e94560; font-size: 50px; margin-top: 50px;">Calculator!!</h1>
        <form method="POST">
            <input type="number" name="a" placeholder="First number" style="padding: 10px; font-size: 18px; border-radius: 5px; border: none; margin: 10px;">
            <input type="number" name="b" placeholder="Second number" style="padding: 10px; font-size: 18px; border-radius: 5px; border: none; margin: 10px;">
            <select name="operation" style="padding: 10px; font-size: 18px; border-radius: 5px; border: none; margin: 10px;">
                <option value="add">Add +</option>
                <option value="subtract">Subtract -</option>
                <option value="multiply">Multiply *</option>
                <option value="divide">Divide /</option>
            </select>
            <button type="submit" style="background-color: #e94560; color: white; padding: 10px 20px; font-size: 18px; border: none; border-radius: 5px;">Calculate!!</button>
        </form>
        <h2 style="color: white; font-size: 30px;">Answer: """ + str(result) + """</h2>
        <a href="/" style="background-color: #e94560; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Go back home!!</a>
    </body>
    </html>
    """
