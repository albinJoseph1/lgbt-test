from Companies.KaoUK.SubAgents.StandardKaoukAgent import Agent as ScrapAgent

class Agent(ScrapAgent):
    def __init__(self, chrome):
        self.chrome = chrome
        super(Agent, self).__init__(self.chrome)

        #     Company Details Start
        self.companyName = "Kao UK"
        self.ownerUsername ="kaouk"
        self.jobIndicesToRemove = []
        #     Company Details End

    def jobsForCompany(self):
        jobIndex = 0
        for job in self.jobs:
            jobLink = job.getLink()
            for moltonBrownJob in self.moltonBrownJobs:
                if jobLink == moltonBrownJob.apply_link:
                    self.jobIndicesToRemove.append(jobIndex)
            jobIndex = jobIndex + 1

        for currentIndex, jobIndexToRemove in enumerate(self.jobIndicesToRemove):
            del self.jobs[jobIndexToRemove - currentIndex]