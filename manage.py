import os
from flask_script import Server, Manager, prompt_bool
from app import create_app
from app.models import db

manager = Manager(create_app)

# Override the default `runserver` command, to monitor the change of
# the configuration file.
# XXX: `Config.root_path` is an undocumented attribute.
class Server(Server):
    def handle(self, app, *args, **kwargs):
        config_path = os.path.join(app.config.root_path, 'config.py')
        self.server_options['extra_files'] = [config_path]
        super(Server, self).handle(app, *args, **kwargs)
manager.add_command('runserver', Server())


db_manager = Manager()

@db_manager.command
def create_all():
    db.create_all()

@db_manager.command
def drop_all():
    if prompt_bool('This action will DESTROY ALL DATA. Continue'):
        db.drop_all()

manager.add_command('db', db_manager)


if __name__ == '__main__':
    manager.run()