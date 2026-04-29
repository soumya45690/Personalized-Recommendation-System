from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import os, sys, subprocess

app = Flask(__name__)
app.secret_key = "sassy_chic_secret_123"

# --- DATABASE SETTINGS ---
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '' 
app.config['MYSQL_DB'] = 'style_recommendation'
app.config['MYSQL_PORT'] = 3307 
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' 

mysql = MySQL(app)
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)

# --- 1. HOME ROUTE (Strict Login) ---
@app.route("/")
def home():
    if not session.get('loggedin'):
        return redirect(url_for('login'))
    return render_template("index.html")

# --- 2. LOGIN ROUTES ---
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_process", methods=["POST"])
def login_process():
    email = request.form.get('email')
    password = request.form.get('password')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE email = %s AND password = %s", (email, password))
    user_data = cur.fetchone()
    cur.close()
    if user_data:
        session['loggedin'] = True
        session['user_id'] = user_data['user_id']
        session['user_name'] = user_data['name']
        return redirect(url_for('home'))
    else:
        flash("Invalid Email or Password!")
        return redirect(url_for('login'))

# --- 3. REGISTER ROUTE ---
@app.route("/register_process", methods=["POST"])
def register_process():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO user (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        mysql.connection.commit()
        flash("Registration Successful! Please Login.")
        return redirect(url_for('login'))
    except:
        flash("Email already exists!")
        return redirect(url_for('login'))
    finally:
        cur.close()

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- 4. GENDER & UPLOAD (SAME AS BEFORE) ---
@app.route("/gender")
def gender_page():
    if not session.get('loggedin'): return redirect(url_for('login'))
    return render_template("gender.html")

@app.route("/upload", methods=["POST"])
def upload():
    gender = request.form.get("gender")
    body = request.form.get("body_type")
    file = request.files.get("file")
    if file and file.filename != "":
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
    else:
        path = "CAMERA" 
    try:
        python_exe = sys.executable
        output = subprocess.check_output([python_exe, "facial_analysis.py", path], 
                                         universal_newlines=True, stderr=subprocess.STDOUT)
        if "RESULT:" in output:
            res_val = output.split("RESULT:")[1].strip()
            shape, tone = [x.strip() for x in res_val.split("|")]
            return redirect(url_for("results_page", shape=shape, tone=tone, gen=gender, body=body))
    except: pass
    return redirect(url_for("results_page", shape="Oval", tone="Fair", gen=gender, body=body))

@app.route("/results_page")
def results_page():
    shape, tone, gen, body = request.args.get('shape'), request.args.get('tone'), request.args.get('gen'), request.args.get('body')
    cur = mysql.connection.cursor()
    query = """
        SELECT h.hs_name, h.hs_image, o.outfit_name, o.outfit_image,
               a.acc_name, a.acc_image, s.shoe_name, s.shoe_image,
               ln.lens_name, ln.lens_image, l.lip_name, l.lip_image,
               hc.hc_name, hc.hc_image, cc.cc_name, cc.cc_image
        FROM recommendation r
        JOIN hairstyle h ON r.hairstyle_id = h.hsid
        JOIN outfit o ON r.outfit_id = o.outfit_id
        JOIN accessories a ON r.acc_id = a.acc_id
        JOIN shoes s ON r.shoe_id = s.shoe_id
        JOIN lens ln ON r.lens_id = ln.lens_id
        JOIN lipstick l ON r.lip_id = l.lip_id
        JOIN hair_colour hc ON r.haircolour_id = hc.hcid
        JOIN cloth_colour cc ON r.clothingcolour_id = cc.ccid
        WHERE r.face_shape_id = (SELECT fsid FROM face_shape WHERE fs_name = %s)
        AND r.skin_tone_id = (SELECT stid FROM skin_tone WHERE st_name = %s)
        AND r.gender = %s LIMIT 1
    """
    cur.execute(query, (shape, tone, gen))
    data = cur.fetchone() 
    cur.close()
    return render_template("results.html", d=data, shape=shape, tone=tone, gen=gen, body=body)

if __name__ == "__main__":
    app.run(debug=True)