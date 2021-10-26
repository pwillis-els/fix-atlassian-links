FROM python:3.8.12-alpine3.14
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY README.md setup.cfg setup.py /app/
COPY fix_atlassian_links /app/fix_atlassian_links/
RUN pip install -e .
ENTRYPOINT [ "fix-atlassian-links" ]
