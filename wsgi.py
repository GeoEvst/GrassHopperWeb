from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from private_key_generator import generate_random_key, gen_gamma
from inout import kuz_encrypt, kuz_decrypt, gam_encrypt, text_encrypt, gam_decrypt, text_decrypt
from datetime import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grasshopper.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = generate_random_key()
char = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']


@app.errorhandler(404)
def page404(error):
    return render_template('page404.html', titlle="Упс..."), 404


class Opentext(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    text = db.Column(db.String(64), nullable=False)
    key = db.Column(db.String(128), nullable=False)
    user = db.Column(db.String(128))
    sign = db.Column(db.Integer)

    def __repr__(self):
        return '<opentext %r>' % self.id


now = datetime.now()
year = now.year


@app.route('/')
def index():
    global year
    return render_template('index.html', year=year)


@app.route('/help')
def helps():
    global year
    return render_template('help.html', year=year)


@app.route('/contact', methods=["POST", "GET"])
def contact():
    global year
    if request.method == 'POST':
        if len(request.form['message']) == 0:
            flash('Сообщение не может быть пустым', category='error')
        else:
            flash('Успешно отправлено', category='success')
    return render_template('contact.html', year=year)


@app.route('/chipper', methods=['POST', 'GET'])
def chipper():
    global char, year
    if request.method == 'POST':
        text = request.form['text']
        key = request.form['key']
        if request.form['btn'] == 'Сгенерировать ключ':
            gen_key = generate_random_key()
            return render_template('chipper.html', key=gen_key, text=text, year=year)
        elif request.form['btn'] == 'Зашифровать':
            ip_user = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            opentext = Opentext(text=text, key=key, user=ip_user, sign=1)

            if len(request.form['text']) != 32 or len(request.form['key']) != 64:
                flash('Длина ключа должна быть 64 символа, длина блока данных 32 символа', category='error')
                return render_template('chipper.html', key=key, text=text, year=year)
            else:
                for i in range(32):
                    if text[i] not in char and text[i].lower() not in char:
                        print(text[i])
                        flash('В сообщении некорректные символы, допустимы: 0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f', category='error')
                        return render_template('chipper.html', key=key, text=text, year=year)
                for i in range(64):
                    if key[i] not in char and key[i].lower() not in char:
                        flash('В ключе некорректные символы, допустимы: 0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f', category='error')
                        return render_template('chipper.html', key=key, text=text, year=year)
                db.session.add(opentext)
                db.session.commit()
                flash('Сообщение зашифровано успешно', category='success')
                result = kuz_encrypt(text, key)
                return render_template('chipper_tab.html', key=key, text=text, result=result, year=year)
    else:
        return render_template('chipper.html', year=year)


@app.route('/chipper1', methods=["POST", "GET"])
def chipper1():
    global char, year
    if request.method == 'POST':
        IV = request.form['IV']
        text = request.form['text']
        key = request.form['key']
        if request.form['btn'] == 'Сгенерировать ключ':
            gen_key = generate_random_key()
            return render_template('chipper1.html', key=gen_key, IV=IV, text=text, year=year)
        if request.form['btn'] == 'Сгенерировать синхропосылку - IV':
            gen_IV = gen_gamma()
            return render_template('chipper1.html', key=key, IV=gen_IV, text=text, year=year)
        elif request.form['btn'] == 'Зашифровать':
            ip_user = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            opentext = Opentext(text=text, key=key, user=ip_user, sign=1)

            if len(request.form['IV']) != 16 or len(request.form['key']) != 64:
                flash('Длина ключа должна быть 64 символа, длина синхропосылки 16 символов', category='error')
                return render_template('chipper1.html', key=key, IV=IV, text=text, year=year)
            elif len(request.form['text']) < 32:
                flash('Сообщение не должно быть меньше 32-х символов', category='error')
                return render_template('chipper1.html', key=key, IV=IV, text=text, year=year)
            else:
                for i in range(32):
                    if text[i] not in char and text[i].lower() not in char:
                        flash('В сообщении некорректные символы, допустимы: 0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f', category='error')
                        return render_template('chipper1.html', key=key, IV=IV, text=text, year=year)
                for i in range(64):
                    if key[i] not in char and key[i].lower() not in char:
                        flash('В ключе некорректные символы, допустимы: 0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f', category='error')
                        return render_template('chipper1.html', key=key, IV=IV, text=text, year=year)
                for i in range(16):
                    if IV[i] not in char and IV[i].lower() not in char:
                        flash('В синхропосылке некорректные символы, допустимы: 0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f', category='error')
                        return render_template('chipper1.html', key=key, IV=IV, text=text, year=year)
                db.session.add(opentext)
                db.session.commit()
                flash('Сообщение зашифровано успешно', category='success')
                result = gam_encrypt(text, key, IV)
                return render_template('chipper1_tab.html', key=key, IV=IV, text=text, result=result, year=year)
    else:
        return render_template('chipper1.html', year=year)


@app.route('/chipper2', methods=["POST", "GET"])
def chipper2():
    global char, year
    if request.method == 'POST':
        IV = request.form['IV']
        text = request.form['text']
        key = request.form['key']
        if request.form['btn'] == 'Сгенерировать ключ':
            gen_key = generate_random_key()
            return render_template('chipper2.html', key=gen_key, IV=IV, text=text, year=year)
        if request.form['btn'] == 'Сгенерировать синхропосылку - IV':
            gen_IV = gen_gamma()
            return render_template('chipper2.html', key=key, IV=gen_IV, text=text, year=year)
        elif request.form['btn'] == 'Зашифровать':
            ip_user = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            opentext = Opentext(text=text, key=key, user=ip_user, sign=1)

            if len(request.form['IV']) != 16 or len(request.form['key']) != 64:
                flash('Длина ключа должна быть 64 символа, длина синхропосылки 16 символов', category='error')
                return render_template('chipper2.html', key=key, IV=IV, text=text, year=year)
            elif len(request.form['text']) == 0:
                flash('Сообщение не должно быть пустым', category='error')
                return render_template('chipper2.html', key=key, IV=IV, text=text, year=year)
            elif len(request.form['text']) > 150:
                flash('Сообщение не должно быть больше 150-ти символов', category='error')
                return render_template('chipper2.html', key=key, IV=IV, text=text, year=year)
            else:
                for i in range(64):
                    if key[i] not in char and key[i].lower() not in char:
                        flash('В ключе некорректные символы, допустимы: 0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f', category='error')
                        return render_template('chipper2.html', key=key, IV=IV, text=text, year=year)
                for i in range(16):
                    if IV[i] not in char and IV[i].lower() not in char:
                        flash('В синхропосылке некорректные символы, допустимы: 0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f', category='error')
                        return render_template('chipper2.html', key=key, IV=IV, text=text, year=year)
                db.session.add(opentext)
                db.session.commit()
                flash('Сообщение зашифровано успешно', category='success')
                result = text_encrypt(text, key, IV)
                return render_template('chipper2_tab.html', key=key, IV=IV, text=text, result=result, year=year)
    else:
        return render_template('chipper2.html', year=year)


@app.route('/decrypt', methods=["POST", "GET"])
def decrypt():
    global char, year
    if request.method == 'POST':
        text = request.form['text']
        key = request.form['key']
        if request.form['btn'] == 'Вставить ключ из ГОСТ':
            gen_key = '8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef'
            return render_template('decrypt.html', key=gen_key, text=text, year=year)
        if request.form['btn'] == 'Расшифровать':
            ip_user = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            opentext = Opentext(text=text, key=key, user=ip_user, sign=0)

            if len(request.form['text']) != 32 or len(request.form['key']) != 64:
                flash('Длина ключа должна быть 64 символа, длина блока данных 32 символа', category='error')
                return render_template('decrypt.html', key=key, text=text, year=year)
            else:
                for i in range(32):
                    if text[i] not in char and text[i].lower() not in char:
                        print(text[i])
                        flash('Некорректный шифр', category='error')
                        return render_template('decrypt.html', key=key, text=text, year=year)
                for i in range(64):
                    if key[i] not in char and key[i].lower() not in char:
                        flash('В ключе некорректные символы, допустимы: 0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f', category='error')
                        return render_template('decrypt.html', key=key, text=text, year=year)
                db.session.add(opentext)
                db.session.commit()
                flash('Сообщение расшифровано успешно', category='success')
                result = kuz_decrypt(text, key)
                return render_template('decrypt_tab.html', key=key, text=text, result=result, year=year)
    else:
        return render_template('decrypt.html', year=year)


@app.route('/decrypt1', methods=["POST", "GET"])
def decrypt1():
    global char, year
    if request.method == 'POST':
        IV = request.form['IV']
        text = request.form['text']
        key = request.form['key']
        if request.form['btn'] == 'Вставить ключ из ГОСТ':
            gen_key = '8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef'
            return render_template('decrypt1.html', key=gen_key, IV=IV, text=text, year=year)
        if request.form['btn'] == 'Вставить IV из ГОСТ':
            IV = '1234567890abcef0'
            return render_template('decrypt1.html', key=key, IV=IV, text=text, year=year)
        if request.form['btn'] == 'Расшифровать':
            ip_user = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            opentext = Opentext(text=text, key=key, user=ip_user, sign=0)

            if len(request.form['IV']) != 16 or len(request.form['key']) != 64:
                flash('Длина ключа должна быть 64 символа, длина синхропосылки 16 символов', category='error')
                return render_template('decrypt1.html', key=key, IV=IV, text=text, year=year)
            elif len(request.form['text']) < 32:
                flash('Некорректный шифр', category='error')
                return render_template('decrypt1.html', key=key, IV=IV, text=text, year=year)
            else:
                for i in range(32):
                    if text[i] not in char and text[i].lower() not in char:
                        flash('Некорректный шифр', category='error')
                        return render_template('decrypt1.html', key=key, IV=IV, text=text, year=year)
                for i in range(64):
                    if key[i] not in char and key[i].lower() not in char:
                        flash('В ключе некорректные символы, допустимы: 0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f', category='error')
                        return render_template('decrypt1.html', key=key, IV=IV, text=text, year=year)
                for i in range(16):
                    if IV[i] not in char and IV[i].lower() not in char:
                        flash('В синхропосылке некорректные символы, допустимы: 0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f', category='error')
                        return render_template('decrypt1.html', key=key, IV=IV, text=text, year=year)
                db.session.add(opentext)
                db.session.commit()
                flash('Сообщение расшифровано успешно', category='success')
                result = gam_decrypt(text, key, IV)
                return render_template('decrypt1_tab.html', key=key, IV=IV, text=text, result=result, year=year)
    else:
        return render_template('decrypt1.html', year=year)


@app.route('/decrypt2', methods=["POST", "GET"])
def decrypt2():
    global char, year
    if request.method == 'POST':
        IV = request.form['IV']
        text = request.form['text']
        key = request.form['key']
        if request.form['btn'] == 'Вставить ключ из ГОСТ':
            gen_key = '8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef'
            return render_template('decrypt2.html', key=gen_key, IV=IV, text=text, year=year)
        if request.form['btn'] == 'Вставить IV из ГОСТ':
            IV = '1234567890abcef0'
            return render_template('decrypt2.html', key=key, IV=IV, text=text, year=year)
        if request.form['btn'] == 'Расшифровать':
            ip_user = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            opentext = Opentext(text=text, key=key, user=ip_user, sign=0)

            if len(request.form['IV']) != 16 or len(request.form['key']) != 64:
                flash('Длина ключа должна быть 64 символа, длина синхропосылки 16 символов', category='error')
                return render_template('decrypt2.html', key=key, IV=IV, text=text, year=year)
            elif len(request.form['text']) > 610:
                flash('Некорректный шифр', category='error')
                return render_template('decrypt2.html', key=key, IV=IV, text=text, year=year)
            else:
                for i in range(64):
                    if key[i] not in char and key[i].lower() not in char:
                        flash('В ключе некорректные символы, допустимы: 0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f', category='error')
                        return render_template('decrypt2.html', key=key, IV=IV, text=text, year=year)
                for i in range(16):
                    if IV[i] not in char and IV[i].lower() not in char:
                        flash('В синхропосылке некорректные символы, допустимы: 0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f', category='error')
                        return render_template('decrypt2.html', key=key, IV=IV, text=text, year=year)
                for i in range(len(request.form['text'])):
                    if text[i] not in char and text[i].lower() not in char:
                        flash('Некорректный шифр', category='error')
                        return render_template('decrypt1.html', key=key, IV=IV, text=text, year=year)
                db.session.add(opentext)
                db.session.commit()
                flash('Сообщение расшифровано успешно', category='success')
                result = text_decrypt(text, key, IV)
                return render_template('decrypt2_tab.html', key=key, IV=IV, text=text, result=result, year=year)
    else:
        return render_template('decrypt2.html', year=year)


if __name__ == '__main__':
    app.run()


