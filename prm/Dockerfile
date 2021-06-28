FROM php:7.3-apache

RUN apt-get update -y && apt-get install -y libmcrypt-dev openssl git nodejs npm libgmp-dev
RUN docker-php-ext-install pdo mbstring mysqli pdo_mysql gmp
RUN pear install MDB2

RUN pecl install mcrypt-1.0.3
RUN docker-php-ext-enable mcrypt

COPY ./openidserver.conf /etc/apache2/sites-available
RUN a2enmod rewrite
RUN service apache2 restart
WORKDIR /etc/apache2/sites-available
RUN a2ensite openidserver.conf

RUN chmod 777 ./php-openid/examples/server/openid

EXPOSE 80