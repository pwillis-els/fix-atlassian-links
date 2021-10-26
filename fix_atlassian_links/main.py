#!/usr/bin/env python3
# fix-atlassian-links.py - Update the text in a confluence page
# Copyright (2021) Peter Willis

import sys, os, argparse, json, re
from atlassian import Confluence

###############################################################################################

# We could subclass Confluence here and get rid of MyConfluence(), but then we couldn't
# re-use this class for Jira or some other object type.
class Main(object):

    def parse_args(self):
        parser = argparse.ArgumentParser(
            # don't want to reformat the description message, use file's doc_string
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=__doc__
        )
        parser.add_argument( '--url', default=None, help='Page base URL, default=%(default)s')
        parser.add_argument( '--title', default=None, help='The title of a page [to get, create, update]')
        parser.add_argument( '--page_id',  default=None, help='ID of page to update')
        parser.add_argument( '--username', default=None, help='Username of Confluence account')
        parser.add_argument( '--auth_token', default=None, help='Confluence auth token for user')
        parser.add_argument( '--page_content', default=None, help='New page content')
        parser.add_argument( '--search_re', default=None, help='Search regular expression')
        parser.add_argument( '--replace', default=None, help='Replacement text for search')
        parser.add_argument( '--literal', default=False, action='store_true', help='Only do literal search/replace, no regular expression')
        parser.add_argument( '--read_only', default=False, action='store_true', help='Do not perform any write actions')
        parser.add_argument( 'action', choices={"get-page", "put-page", "search-replace-page"},
            help='Choose an action to perform')
        parser.add_argument( 'args', nargs='*')
        args = parser.parse_args()

        self.CONFLUENCE_URL  = os.environ.get("CONFLUENCE_URL")
        self.CONFLUENCE_USER = os.environ.get("CONFLUENCE_USER")
        self.CONFLUENCE_PASS = os.environ.get("CONFLUENCE_PASS")
        if args.url != None:        self.CONFLUENCE_URL  = args.url
        if args.username != None:   self.CONFLUENCE_USER = args.username
        if args.auth_token != None: self.CONFLUENCE_PASS = args.auth_token

        if self.CONFLUENCE_URL == None or self.CONFLUENCE_USER == None or self.CONFLUENCE_PASS == None:
            raise Exception("Must pass a CONFLUENCE_URL, CONFLUENCE_USER, CONFLUENCE_PASS environment variables or via command-line options")

        self.args = args

    def __init__(self):
        self.parse_args()

        c = MyConfluence( url=self.CONFLUENCE_URL, username=self.CONFLUENCE_USER, password=self.CONFLUENCE_PASS )

        if self.args.action == 'get-page':
            if self.args.page_id == None:
                raise Exception("Please pass --page_id")

            result = c.get_content(self.args)
            print(json.dumps(result))

        elif self.args.action == 'search-replace-page':
            if self.args.page_id == None or self.args.search_re == None or self.args.replace == None:
                raise Exception("Please pass --page_id, --search_re, --replace")

            result = c.search_replace_content(self.args)
            print(json.dumps(result))

###############################################################################################

class MyConfluence(Confluence):

    #def __init__(self, url, *args, **kwargs):
    #    super().__init__(url, args, kwargs)

    def put_content(self, args, title, body):
        result = None
        if title == None:
            content = get_content(args)
            title = content["title"]
        if args.read_only == False:
            result = self.update_page( page_id=args.page_id, title=title, body=body, version_comment="Updated by automation" )
        return result

    def get_content(self, args):
        return self.get_page_by_id( args.page_id, expand="body.storage" )

    def search_replace_content(self, args):
        content = self.get_content(args)
        #print("content: %s" % content)
        content_body = "%s" % content["body"]["storage"]["value"]

        if args.literal == True:
            result = content_body.replace(args.search_re, args.replace)
            content_body = result
        elif args.literal == False:
            result = re.sub(args.search_re, args.replace, content_body)
            content_body = result

        title = args.title
        if args.title == None:
            title = content["title"]

        #result = { 
        #    "old_content": content["body"]["storage"]["value"],
        #    "new_content": content_body,
        #    "title": title
        #}
        #print( json.dumps(result) )
        return self.put_content(args, title, content_body)

###############################################################################################

if __name__ == "__main__":
    Main()
