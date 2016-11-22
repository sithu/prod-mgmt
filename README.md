#### Run the App
```sh
export APP_SETTINGS="config.DevelopmentConfig"
# DB setup
flask/bin/python manage.py db init
flask/bin/python manage.py db migrate
flask/bin/python manage.py db upgrade
# Run the app
./flask/bin/python run.py 
```

#### Create Test Data

```sh
./flask/bin/python manage.py create_admin
```

#### Employee Level

* 0 - Admin/CEO
* 1 - VP
* 2 - Director
* 3 - Manager
* 4 - Supervisor
* 5 - Skilled worker

```sh
80  npm install -g yo
   81  npm install -g generator-angular-flask
   82  ./install.sh
   83  pip install --upgrade pip
   84  bower install
   85  bower install
   86  npm install -g bower
   87  bower install
   88  bower install
   89  vi ~/.bash_profile 
   90  . ~/.bash_profile 
   91  ls
   92  bower -v
   93  ls
   94  more generator.json 
   95  ls
   96  npm -v
   97  bower -v
   98  ls
   99  ls -al
  100  node -v
  101  npm install -g grunt-cli
  102  npm install
  103  sudo npm install
  104  grunt
  105  grunt --force
  106  ls
  107  bower install
  108  bower install
  109  "type": "input"
  110  export APP_SETTINGS="config.DevelopmentConfig"
  111  ./flask/bin/python run.py
  112  history
```