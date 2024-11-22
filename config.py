import os


basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True   
WTF_CSRF_ENABLED = True
SECRET_KEY = '*f#Vkp8qw7AAb3iGqfFc1rZzmoDOIp7e68Qr7^7!1H1$vI!FA5w7viirhAUJpZbjxrOpw#KWKOmysFKLj!vBHZMVfjecuHqZik#ny7a&KyRNf6%qLmFa&nfPo6js3*9o'