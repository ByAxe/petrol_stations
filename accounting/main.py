import os

from accounting.controller.controller import app

if __name__ == '__main__':
    # app.debug = True
    app.config['DATABASE_NAME'] = "dbname=petrol_stations user=postgres password=postgres host=localhost port=5432"
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 9090))
    app.run(host=host, port=port)
