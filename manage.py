import os

from flask_script import Manager, Server, prompt_bool

from app import create_app

manager = Manager(create_app)

# Override the default `runserver` command, to monitor the change of
# the configuration file.
# XXX: `Config.root_path` is an undocumented attribute.
class Server(Server):
    def handle(self, app, *args, **kwargs):
        config_path = os.path.join(app.config.root_path, "config.py")
        self.server_options["extra_files"] = [config_path]
        super(Server, self).handle(app, *args, **kwargs)


manager.add_command("runserver", Server())

if __name__ == "__main__":
    manager.run()
