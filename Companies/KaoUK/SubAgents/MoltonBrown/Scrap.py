from Companies.KaoUK.SubAgents.StandardKaoukAgent import Agent as ScrapAgent

class Agent(ScrapAgent):
    def __init__(self, chrome):
        self.chrome = chrome
        super(Agent, self).__init__(self.chrome)

        #     Company Details Start
        self.companyName = "Molton Brown"
        self.ownerUsername = "moltonbrown"
        #     Company Details End

    def jobsForCompany(self):
        self.jobs = []
        self.jobs = self.moltonBrownJobs