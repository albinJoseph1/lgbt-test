# Required Packages
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from Companies.StandardAgent import ScrapAgent
from Objects import Job


class Agent(ScrapAgent):
    def __init__(self, chrome, storage=None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "Monica Vinader"
        self.ownerUsername = "monicavinader"
        self.scrapPageURL = "https://jobs.jobvite.com/monicavinader"
        self.locationFilters = ['UK', 'United Kingdom']
        self.feedType = self.feedTypeWebScrap
        #     Company Details End

    def loadScrapPage(self):

        self.chrome.getComplete(self.scrapPageURL)

        WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".jv-page-content"))
        )

    # Scraper Function
    def loadJobs(self):

        self.loadScrapPage()

        try:
            allLocJobs = []
            jobContainers = self.chrome.find_elements_by_css_selector("table.jv-job-list tr")
            for jobContainer in jobContainers:

                title = str(jobContainer.find_element_by_css_selector("td.jv-job-list-name > a").text)
                title = title.strip()
                self.job.setTitle(title)

                link = jobContainer.find_element_by_css_selector("td.jv-job-list-name > a").get_attribute("href")
                self.job.setLink(link)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)
                allLocJobs.append(self.job)
                self.job = Job()

            for jobIndex, job in enumerate(allLocJobs):

                self.chrome.getComplete(job.getLink())
                self.chrome.pageWait()

                self.chrome.execute_script("""jQuery('p.jv-job-detail-meta span.jv-inline-separator:nth-child(1)').removeClass('jv-inline-separator').text(':');
                              jQuery('p.jv-job-detail-meta span.jv-inline-separator').text('/');
                               """)
                location = self.chrome.find_element_by_css_selector('p.jv-job-detail-meta').text.strip()
                seperatorIndex = int(location.index(':')) + 1
                location = location[seperatorIndex:]
                location = location.strip()
                hasLocationFilters = bool([ele for ele in self.locationFilters if (ele in location)])
                # print(job.getTitle() + ": " + location + ": " + str(hasLocationFilters))
                if hasLocationFilters:
                    allLocJobs[jobIndex].setLocation(location)

                    self.sanitizeElementsForDescription()
                    descriptionElement = self.chrome.find_element_by_css_selector('.jv-job-detail-description')
                    self.chrome.execute_script("""jQuery('.jv-job-detail-description img').remove();
                                                jQuery('p').each(function() {
                                                            const $this = jQuery(this);
                                                            if($this.html().replace(/\s|&nbsp;/g, '').length === 0)
                                                                $this.remove();
                                                        });
                                                  """)
                    description = descriptionElement.get_attribute('innerHTML').strip()
                    allLocJobs[jobIndex].setDescription(description)

                    self.jobs.append(allLocJobs[jobIndex])

                else:
                    pass

            return True

        except:
            self.exceptionLogging()
            return False
