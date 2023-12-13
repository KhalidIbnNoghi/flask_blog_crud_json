from flask import Flask

app = Flask(__name__)
app.secret_key = 'huisahduh876sd=+87sdy98'

from core import routes
