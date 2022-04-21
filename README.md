
# Sequelize Migration Generator

Generates Sequelize migrations from an existing database structure.


## Enviroment
```
Python >3.6 < 3.7

```
## Installation And Run

Install my-project with npm

```bash
  git clone https://github.com/vinivia/sequelize-migration-generator.git
  cd sequelize-migration-generator
  pip install -r requirement.txt
  sequelize.py -H <database_host> -P <database_port> -u <database_username> 
  -p <database_password> -d <database_name> --path <path_of_migrations_file>
```
## Command Help
```
sequelize.py -h for help
```
```commandline
usage: sequelize.py [-h] [-H [host]] [-P [port]] [-u [username]]
                    [-p [password]] -d [database] [--path [path]]

Sequelize Migration Generator.

optional arguments:
  -h, --help            show this help message and exit
  -H [host], --host [host]
                        Mysql database host default <localhost>
  -P [port], --port [port]
                        Mysql database port default <3306>
  -u [username], --username [username]
                        Mysql database username default <root>
  -p [password], --password [password]
                        Mysql database password default<>
  -d [database], --database [database]
                        Mysql database name
  --path [path]         Migration store path


```