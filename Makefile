
docker-build:
	docker build -t fix-atlassian-links:latest .

search-replace-page: docker-build
	docker run --rm -it fix-atlassian-links --page_id $(CONFLUENCE_PAGE_ID) --search_re "$(SEARCH_RE)" --replace "$(REPLACE_TEXT)" --username "$(CONFLUENCE_USER)" --url "$(CONFLUENCE_URL)" --auth_token "$(CONFLUENCE_PASS)" search-replace-page

local-venv:
	if [ ! -d venv ] ; then \
        virtualenv -p python3 venv && \
        ./venv/bin/pip install -r requirements.txt ; \
    fi
