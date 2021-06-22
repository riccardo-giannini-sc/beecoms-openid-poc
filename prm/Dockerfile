FROM php:7.3-fpm

RUN apt-get update -y && apt-get install -y libmcrypt-dev openssl git nodejs npm
RUN docker-php-ext-install pdo mbstring mysqli pdo_mysql
RUN pecl install mcrypt-1.0.3
RUN docker-php-ext-enable mcrypt

RUN apt-get install -y curl
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

WORKDIR /app
COPY . /app

#laravel project dependencies
RUN composer install
#provisioning for laravel passport
RUN npm install --global cross-env

CMD php artisan serve --host=0.0.0.0 --port=8002
EXPOSE 8002