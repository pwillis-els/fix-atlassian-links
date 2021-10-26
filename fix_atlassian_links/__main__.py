#!/usr/bin/env python3
# __main__.py - Command-line interface to fix_atlassian_links
# Copyright (2021) Peter Willis

__description__ = """
The fix-atlassian-links command-line interface to the fix_atlassian_links Python package.

You can pass three environment variables:
   CONFLUENCE_URL       - This is the base URL of the Confluence instance. This is NOT an individual page.
   CONFLUENCE_USER      - The username to connect to Confluence with.
   CONFLUENCE_PASS      - The password or authentiction token to connect to Confluence with.

The 'get-page' action requires the following options:
    --page_id

The 'search-replace-page' action requires the following options:
    --page_id
    --search_re
    --replace
"""

import sys, os, argparse, json
#from fix_atlassian_links import confluence
from . import confluence

###############################################################################################

class Cmdline(object):
    """
    The Cmdline() class implements the command-line tool.
    """

    def parse_args(self):
        """ Parses command-line arguments and prepares help message """
        parser = argparse.ArgumentParser(
            # don't want to reformat the description message, use file's doc_string
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=__description__
        )
        #parser = argparse.ArgumentParser()

        parser.add_argument( '--url', default=None, help='Page base URL, default=%(default)s')
        parser.add_argument( '--title', default=None, help='The title of a page [to get, create, update]')
        parser.add_argument( '--page_id',  default=None, help='ID of page to update')
        parser.add_argument( '--username', default=None, help='Username for Confluence')
        parser.add_argument( '--auth_token', default=None, help='Authentication token or password for Confluence')
        parser.add_argument( '--page_content', default=None, help='New page content (not currently used)')
        parser.add_argument( '--search', default=None, help='Search regular expression (or literal search text)')
        parser.add_argument( '--replace', default=None, help='Replacement text for search')
        parser.add_argument( '--literal', default=False, action='store_true', help='Only do literal search/replace, no regular expression')
        parser.add_argument( '--read_only', default=False, action='store_true', help='Do not perform any write actions')
        parser.add_argument( 'action', choices={"get-page", "put-page", "search-replace-page"},
            help='Choose an action to perform')

        return parser


    def main(self):
        """
        The main entrypoint of the command-line tool.
        """
        parser = self.parse_args()
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

        c = confluence.FixConfluence( url=self.CONFLUENCE_URL, username=self.CONFLUENCE_USER, password=self.CONFLUENCE_PASS )

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

def main():
    Cmdline().main()

# This matches whenever pydoc is run
#if __name__ == "fix_atlassian_links.__main__":

if __name__ == "__main__":
    Cmdline().main()
else:
    # Populate pydoc with argparse help
    _p = Cmdline().parse_args()
    __doc__ = _p.format_help()
    
