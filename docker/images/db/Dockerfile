FROM postgres:9.6.5

ENV POSTGRES_USER=is
ENV POSTGRES_PASSWORD=is
ENV POSTGRES_DB=xml-rpc-project

COPY schema.sql /docker-entrypoint-initdb.d/

EXPOSE 5432