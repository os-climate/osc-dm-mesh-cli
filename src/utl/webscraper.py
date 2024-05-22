# Copyright 2023 Broda Group Software Inc.
#
# Created: 2023-06-27 by davis.broda@brodagroupsoftware.com
import logging
import os.path
from typing import List, Set, Dict
import re

import requests
from bs4 import BeautifulSoup


class WebScraper:
    logger = logging.getLogger(__name__)

    def __init__(
            self,
            top_level_url: str,
            depth: int = 0,
            user_agent: str = "Broda Group Text Scraper",
            blacklist_link_regexs: List[str] = None,
            min_words: int | None = None
    ):
        """
        A class that will scrape provided web page(s) and return the output.

        :param top_level_url:
            When scraping a page, only outgoing links that remain within this
            domain will be scraped. For example if http://a.com/b is provided
            as a top_level_url, then pages like http://a.com/b/c/d will be
            scraped, but http://a.com/z will not, nor will
            http://www.wikipedia.com
        :type top_level_url: str
        :param depth:
            The number of times links found on the scraped page should be
            followed and recursivly scraped. defaults to 0.
        :type depth: int
        :param user_agent:
            Name of the scraper. Currently unused.
            Defaults to "Broda Group Text Scraper"
        :type user_agent: str
        :param blacklist_link_regexs:
            Only links that match no entries in this blacklist will be
            followed and recursivly scraped
        :type blacklist_link_regexs: List[str]
        :param min_words:
            The minimum number of words that must be present in a html element
            for it to be included in the scraped results. Intended for
            excluding things like menu elements which are not likely to
            provide semantically useful information.
            Defaults to None, which will include everything in the results.
        :type min_words: int | None

        """
        if depth < 0:
            raise InvalidDepthException(
                f"depth cannot be less than 0. Provided depth was {depth}")
        if depth > 2:
            raise InvalidDepthException(
                f"Maximum allowable depth is 2. Provided depth was {depth}")
        self.depth = depth
        self.user_agent = user_agent
        self.currentOutputIndex = 0
        self.scannedLinks: Set[str] = set()
        self.exclude_link_regexes = blacklist_link_regexs or []
        self.top_level_url = top_level_url
        self.min_words = min_words

    @staticmethod
    def __check_robots_txt():
        # TODO: Deal with this later
        return None

    def scrape_with_depth(self, base_url: str) -> List[Dict[str, str]]:
        """
        Scrapes the provided url, putting all text into an entry in the
        output list. Will then recursively scrape all non-excluded links
        on the page in the same manner, until target depth is reached.

        :param base_url: The url to be scraped.
        :type base_url: str

        :return:
            A list containing the contents of all scraped pages, up to
            maximum depth.
        :rtype: List[Dict[str, str]]
        """

        return self.__scrape_with_depth(base_url, base_url, self.depth, [])

    def __scrape_with_depth(
            self,
            current_url: str,
            base_url: str,
            depth: int,
            out_page_contents: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        """
        TODO: for large numbers of pages this recursion will probably not be
         efficient due to a lack of tail recursion

        :param current_url:
            The current page being scraped
        :param base_url:
            The url of the original page being scraped. Will be the same as
            base_url if scrape_with_depth has not yet recursed
        :param depth:
            Controls how many times links will be followed and recursivly
            scraped
        :param out_page_contents:
            The content of the pages scanned,
            with prepended base url and current url
        :return:
            A list of the the file content. Each item is a dictionary with the
            following structure:

            {
                "base-url": base url that initiated scanning before recursion
                "current-url": url being scanned now
                "content": text content on the current url
            }
        :rtype: List[Dict[str, str]]

        :raise InvalidDepthException:
            if depth is negative
        """

        if depth < 0:
            raise InvalidDepthException(
                f"cannot have negative depth. Provided depth was {depth}")

        links: List[str] = []
        try:
            (content, links) = self.scrape_single_page(current_url)
        except InvalidHttpResponse as e:
            self.logger.warning(
                f"Invalid Http status recieved when attempting"
                f" to access page {current_url}")
        except Exception as e:
            self.logger.exception(f"Error encountered getting page {current_url}.")
            return out_page_contents
        else:
            out = {
                "base-url": base_url,
                "current-url": current_url,
                "content": content

            }
            out_page_contents.append(out)

        if depth > 0:
            n_depth = depth - 1
            for link in links:
                if not (link in self.scannedLinks):
                    self.scannedLinks.add(link)
                    self.__scrape_with_depth(
                        link,
                        base_url,
                        n_depth,
                        out_page_contents)

        return out_page_contents

    def scrape_single_page(self, base_url: str) -> tuple[str, List[str]]:
        """
        Scrape the contents of a single page

        :param base_url:
            The url to be parsed.
        :type base_url: str

        :return:
            a tuple, where the first element is a string containing all
             text on the page being scraped. The second element contains
             a list of all non-excluded links from the scraped page.
        :rtype: tuple[str, List[str]]
        """
        self.logger.info(f"Scanning URL: {base_url}")
        base_page = requests.get(url=base_url)
        if base_page.status_code < 200 or base_page.status_code >= 300:
            raise InvalidHttpResponse(
                f"Non successful status code returned:"
                f" {base_page.status_code}")
        soup = BeautifulSoup(base_page.content.decode('utf-8', 'ignore'), features="html.parser")

        # remove all scripts and style elements,
        # as they are not desired Content
        for script in soup.find_all(["script", "style"]):
            script.extract()

        temp_delimiter = "~~SCRAPER_DELIMITER~~"

        all_text = soup.get_text(temp_delimiter, True)
        text_chunks = all_text.split(temp_delimiter)

        def above_min_words(text: str) -> bool:
            if self.min_words is None:
                return True
            else:
                return len(text.split(" ")) >= self.min_words

        filter_text_chunks = list(filter(above_min_words, text_chunks))

        all_text = '\n'.join(filter_text_chunks)

        # get links
        links = self.get_links(soup)

        return all_text, links

    def get_links(
            self,
            soup: BeautifulSoup
    ) -> Set[str]:
        """
        Get all unique links from a supplied soup instance. Duplicate links
        will only appear once in the output set.

        :param soup:
            A BeautifulSoup instance representing the content of
            a webpage.
        :type soup: BeautifulSoup

        :return: a set of all links on the page
        :rtype: Set[str]
        """

        links: Set[str] = set()
        for link in soup.find_all('a', href=True):
            if link.attrs["href"] is not None:
                raw_link = link["href"]
                link_str = self.__fix_relative_url(raw_link)
                starts_with_top = self.__starts_with_top_level_url(link_str)
                (allowed_by_blacklist, blEntry) = \
                    self.__link_match_no_blacklist_entry(link_str)

                if starts_with_top and allowed_by_blacklist:
                    links.add(link_str)
                else:
                    if not starts_with_top:
                        self.logger.debug(
                            f"excluding link ${link_str} as it was "
                            f"not within the top level domain "
                            f"${self.top_level_url}")
                    else:
                        self.logger.debug(
                            f"excluding link ${link_str} as it was "
                            f"excluded by the blacklist entry ${blEntry}"
                        )

        return links

    def __link_match_no_blacklist_entry(self, link: str) -> (bool, str):
        actual_link = self.__fix_relative_url(link)
        for exclude in self.exclude_link_regexes:
            regex = re.compile(exclude)
            if regex.match(actual_link):
                return False, exclude
        return True, None

    def __starts_with_top_level_url(self, link: str) -> bool:
        return link.startswith(self.top_level_url)

    def __fix_relative_url(self, link_str):
        # Parse the URL
        from urllib.parse import urlparse
        url = self.top_level_url
        parsed_url = urlparse(url)
        site_url = parsed_url.scheme + "://" + parsed_url.hostname

        original_link_str = link_str
        if link_str.startswith("/"):
            link_str = site_url + link_str
            self.logger.debug(f"Fixing relative link:{original_link_str}"
                          f" to fully qualified link:{link_str}")
        return link_str


class InvalidDepthException(Exception):
    def __init__(self, message: str):
        """Raised if depth is not a valid value"""
        self.message = message
        super().__init__(self.message)

class InvalidHttpResponse(Exception):
    def __init__(self, message: str):
        """Raised if the http response recieved is not valid"""
        self.message = message
        super().__init__(self.message)
