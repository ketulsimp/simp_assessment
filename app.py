from flask import Flask, render_template
from Blueprints import blueprints

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I_hate_setting_secret_key'

for blueprint in blueprints:
    app.register_blueprint(blueprint)
    
@app.route('/')
def main():
    return render_template('/base.html')

if __name__=='__main__':
    app.run(host='localhost')