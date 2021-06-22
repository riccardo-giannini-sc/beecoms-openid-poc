# create databases
CREATE DATABASE IF NOT EXISTS `layer`;
CREATE DATABASE IF NOT EXISTS `prm`;
CREATE DATABASE IF NOT EXISTS `serverapp`;

# grant privileges on these databases to mysql user
CREATE USER 'laravel'@'%' IDENTIFIED WITH mysql_native_password BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'laravel'@'%';