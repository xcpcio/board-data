FROM nginx:1.27-alpine

COPY site/ /site/
COPY scripts/export-site.sh /usr/local/bin/export-site.sh

RUN apk add --no-cache bash \
    && rm -rf /usr/share/nginx/html \
    && ln -s /site /usr/share/nginx/html

ENTRYPOINT ["export-site.sh"]
