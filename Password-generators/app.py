from flask import Flask, render_template, request
import secrets
import string
import random

app = Flask(__name__)

def generate_password(length):
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation
    all_chars = string.ascii_letters + digits + symbols

    password_list = [
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(symbols)
    ]
    remaining_length = length - 3
    for _ in range(remaining_length):
        password_list.append(secrets.choice(all_chars))
    random.shuffle(password_list)
    return ''.join(password_list)

@app.route("/", methods=["GET", "POST"])
def index():
    website = ""
    username = ""
    length = 12  # Default length
    password = ""
    message = ""
    error = ""

    if request.method == "POST":
        website = request.form.get("website", "").strip()
        username = request.form.get("username", "").strip()
        length_str = request.form.get("length", "").strip()
        action = request.form.get("action")  # 'generate' or 'save'

        # Validate inputs
        if not website:
            error = "❌ Website is required."
        elif not username:
            error = "❌ Username is required."
        else:
            try:
                length = int(length_str)
                if length < 5:
                    error = "⚠️ Password length must be ≥5."
                else:
                    # Generate password only if not already generated
                    if not password:
                        password = generate_password(length)

                    # Save only if action == 'save'
                    if action == "save":
                        with open("passwords.txt", "a") as f:
                            f.write(f"{website} | {username} | {password}\n")
                        message = "✅ Credentials saved to 'passwords.txt'"
            except ValueError:
                error = "❌ Invalid length — must be a number."

    return render_template(
        "index.html",
        website=website,
        username=username,
        length=length,
        password=password,
        message=message,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)