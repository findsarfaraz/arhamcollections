import os

from flask_script import Manager

from flask_migrate import Migrate,MigrateCommand

import arhamcollection_app.config as Config

from arhamcollection_app.extensions	import db



from run import app

app.config.from_object(Config.DevelopmentConfig)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()