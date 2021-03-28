#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from urllib.parse import urlparse
try:
    import markdown
    from bs4 import BeautifulSoup
except ImportError as e:
    print(e, "Use: pip install beautifulsoup4 markdown")
    exit(0)


class TestReadme(unittest.TestCase):

    def setUp(self) -> None:
        with open('README.md', 'r') as md:
            content = md.read()
            contentHTML = markdown.markdown(content)
            self.soup = BeautifulSoup(contentHTML, "html.parser")
        return super().setUp()

    def test_readme(self):
        tc_title = self.soup.find("h2", text='Table of Contents')
        self.assertNotEqual(tc_title, None)

        tc_unordered_list = tc_title.find_next("ul")
        self.assertNotEqual(tc_unordered_list, None)

        tc_hyperlinks = tc_unordered_list.find_all('a')
        self.assertNotEqual(len(tc_hyperlinks), 0)
        tc_hyperlink_order = []

        for a in tc_hyperlinks:

            a_text = a.get_text()
            a_href = a['href']
            # Check Struct href
            self.assertEqual(a_href,
                "#{}".format(a_text.lower().replace(' ', '-')))
            # Check if exists href
            h3 = self.soup.find_all("h3", text=a_text)
            self.assertEqual(len(h3), 1)
            tc_hyperlink_order.append(a_text)

        # check if table of contents is sorted
        tc_hyperlink_order_asc = sorted(tc_hyperlink_order)
        self.assertListEqual(tc_hyperlink_order_asc, tc_hyperlink_order)

        # Check if item table of contents is sorted on body
        self.assertListEqual(tc_hyperlink_order_asc,
                            [h.get_text() for h in self.soup.find_all("h3")])

        # check if sub-items body is sorted
        domain = lambda s: urlparse(s).netloc
        hypelinks = []
        for i in tc_hyperlink_order_asc:
            s_title = self.soup.find("h3", text=i)
            s_unordered_list = s_title.find_next("ul")
            self.assertNotEqual(s_unordered_list, None)
            s_hyperlinks = s_unordered_list.find_all('a')
            self.assertNotEqual(len(s_hyperlinks), 0)
            s_hyperlink_order = []
            for a in s_hyperlinks:
                a_text = a.get_text()
                a_href = domain(a['href'])
                s_hyperlink_order.append(a_text)
                # Check if hyperlink duplicate
                self.assertFalse(a_href in hypelinks,
                    "%s : Hypelink duplicate " % a_href)
                hypelinks.append(a_href)
            # check sub-items is sorted
            s_hyperlink_order_asc = sorted(s_hyperlink_order)
            self.assertListEqual(s_hyperlink_order_asc, s_hyperlink_order)


if __name__ == '__main__':
    unittest.main()
