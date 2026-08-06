FROM n8nio/n8n:latest

USER root

RUN mkdir -p /files \
    && chown -R node:node /files

COPY --chown=node:node docs/pdf/knowledge/ /files/

USER node