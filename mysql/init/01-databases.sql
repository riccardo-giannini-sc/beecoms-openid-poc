# create databases
CREATE DATABASE IF NOT EXISTS `layer`;
CREATE DATABASE IF NOT EXISTS `prm`;
CREATE DATABASE IF NOT EXISTS `serverapp`;

# grant privileges on these databases to mysql user
GRANT ALL PRIVILEGES ON *.* TO 'mysql'@'%';