import argparse
from core import generate_migration, generate_seeds

parser = argparse.ArgumentParser(description='Sequelize Migration Generator.')
parser.add_argument("-H", '--host', metavar='host', type=str, nargs='?', default="localhost", help='Mysql database host default <localhost>')
parser.add_argument('-P', '--port', metavar='port', type=int, nargs='?', default="3306", help='Mysql database port default <3306>')
parser.add_argument('-u', '--username', metavar='username', type=str, nargs='?', default="root", help='Mysql database username default <root>')
parser.add_argument('-p', '--password', metavar="password", type=str, nargs='?', help='Mysql database password default<''>')
parser.add_argument('-d', '--database', metavar="database", type=str, nargs='?', required=True, help='Mysql database name')
parser.add_argument('--path', metavar="path", type=str, nargs='?', default="migrations", help='Migration store path')
parser.add_argument('-M', '--migration', metavar="migration", type=str, nargs='?', default="M", help='Migration OR Seeds default<M> M= migration, S= seeds')
args = parser.parse_args()
if args.migration == "M":
    generate_migration(args.host, args.port, args.username, args.password, args.database, args.path)
elif args.migration == "S":
    generate_seeds(args.host, args.port, args.username, args.password, args.database, args.path)
else:
    pass
print("DONE!!!")