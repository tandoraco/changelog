CREATE_DB_COMMAND_WITH_PASSWORD = 'createdb --host {host} --username {username} --password {password} {database_name}'
CREATE_DB_COMMAND = 'createdb --host {host} --username {username} {database_name}'

DELETE_DB_COMMAND_WITH_PASSWORD = CREATE_DB_COMMAND_WITH_PASSWORD.replace('createdb', 'dropdb')
DELETE_DB_COMMAND = CREATE_DB_COMMAND.replace('createdb', 'dropdb')
