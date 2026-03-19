FROM php:8.2-apache

RUN a2enmod proxy proxy_http

COPY apache.conf /etc/apache2/sites-available/000-default.conf
COPY index.html /var/www/html/index.html

# uploads dir is populated via shared Docker volume at runtime
RUN mkdir -p /var/www/html/uploads && chmod 777 /var/www/html/uploads
