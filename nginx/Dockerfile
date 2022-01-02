FROM nginx:1.20.1-alpine

# デフォルト設定ファイルを削除し、ホストの/nginx/nginx.confをコンテナにCOPYして使う。
RUN rm /etc/nginx/conf.d/default.conf

COPY ./nginx.conf /etc/nginx/conf.d
