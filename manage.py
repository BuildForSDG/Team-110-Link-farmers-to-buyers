from flask_script import Manager  # help convert module to a script
from flask_migrate import Migrate, MigrateCommand

from run import app, db, User, Farm, Product, Category, Order, OrderItem

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()  # starting the manager
