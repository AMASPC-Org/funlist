{ pkgs }: {
   deps = [
     pkgs.lsof
     pkgs.glibcLocales
     pkgs.openssl
     pkgs.postgresql
     pkgs.python311
     pkgs.python311Packages.flask
     pkgs.python311Packages.sqlalchemy
     pkgs.python311Packages.psycopg2
     pkgs.python311Packages.geopy
     pkgs.python311Packages.requests
     pkgs.python311Packages.flask-mail
     pkgs.python311Packages.flask-login
     pkgs.python311Packages.flask-session
     pkgs.python311Packages.flask-limiter
     pkgs.python311Packages.flask-migrate
     pkgs.python311Packages.werkzeug
     pkgs.nodejs-18_x
     pkgs.nettools
   ];
   env = {
     FLASK_APP = "app:app";
     FLASK_ENV = "development";
     DATABASE_URL = "<YOUR_DATABASE_URL>"; # Make sure to replace this
   };
   run = "python -m flask run --host=0.0.0.0 --port=5006";
 }