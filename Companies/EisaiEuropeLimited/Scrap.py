import re
from datetime import datetime
# Required Packages
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage=None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "Eisai Europe Limited"
        self.ownerUsername = "eisaieurope"
        self.location = "Mosquito Way, Hatfield, Hertfordshire AL10 9SN"
        self.scrapPageURL = "https://careers.eisai.net/go/Current-Opportunities/8928001/"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

    def clean_html_description(self, html_description):
        """
        Function to clean up empty or whitespace-only paragraphs in an HTML job description.
        Removes tags like <p></p>, <p>&nbsp;</p>, <p class="...">&nbsp;</p>, and
        other variations like <p><br> &nbsp;</p>.
        Additionally, removes inline styles from all HTML tags, specifically removing font-size,
        and avoids <br> tags immediately after <p>.
        """
        # 1. Remove font-size from the style attribute of any tag
        html_description = re.sub(r'style="[^"]*font-size:[^;"]*;?', '', html_description)

        # 2. If the style attribute becomes empty, remove the entire style attribute
        html_description = re.sub(r'\s*style="\s*"', '', html_description)

        # 3. Remove empty or whitespace-only <p> tags
        clean_description = re.sub(r'<p[^>]*>(\s|&nbsp;|<br\s*/?>)*</p>', '', html_description)

        # 4. Avoid <br> tags immediately after opening <p> tags
        clean_description = re.sub(r'<p[^>]*>\s*<br\s*/?>', '<p>', clean_description)

        # 5. Clean up multiple newlines
        clean_description = re.sub(r'\n\s*\n', '\n', clean_description)

        return clean_description

    def loadJobs(self):
        self.loadScrapPage()
        try:
            jobContainers = self.chrome.find_elements_by_css_selector("#job-tile-list li.job-tile")
            for jobContainer in jobContainers:
                title_element = jobContainer.find_element_by_css_selector("span.section-title.title a.jobTitle-link")
                title =  title_element.get_attribute("textContent").strip()
                link = title_element.get_attribute("href")
                self.job.setTitle(title)
                self.job.setLink(link)
                self.job.setLocation(self.location)
                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)
                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                description_element = self.chrome.find_element_by_css_selector("span.jobdescription")
                description_html = description_element.get_attribute('innerHTML').strip()
                description_html = re.sub(r'<h2.*?>.*?</h2>', '', description_html, flags=re.DOTALL)
                description_html = self.clean_html_description(description_html)
                self.jobs[currentJobIndex].setDescription(description_html)

            return True

        except:
            self.exceptionLogging()
            return False
