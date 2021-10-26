#!/usr/bin/env python3
# confluence.py - Update the text in a confluence page
# Copyright (2021) Peter Willis

"""
The fix_atlassian_links Confluence package.
Contains some custom functions, and inherits the atlassian.Confluence object.
"""

import re
from atlassian import Confluence

class FixConfluence(Confluence):

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

