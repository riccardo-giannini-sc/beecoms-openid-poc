FROM php:7.3-apache

RUN apt update
RUN apt install -y apt-utils libcurl4-gnutls-dev;

COPY ./app-php-server.conf /etc/apache2/sites-available
RUN a2enmod rewrite
RUN service apache2 restart
WORKDIR /etc/apache2/sites-available
RUN a2dissite 000-default.conf
RUN a2ensite app-php-server.conf

RUN docker-php-ext-install curl

COPY ./src /var/www/html/app-php

WORKDIR /var/www/html/app-php

EXPOSE 80