import logging
from ..LibFrame import applicationDict
from ..Objects.Project import Project
class InformationHandler(object):
    

    def listProjects(self):
        dbentries=applicationDict["dbconn"].getAllProjects()
        output=dict()
        for dbentry in dbentries:
            if not dbentry.project_country in output:
                output[dbentry.project_country]=dict()
            if not dbentry.project_site in output[dbentry.project_country]:
                output[dbentry.project_country][dbentry.project_site]=dict()
            if not dbentry.projekt_application in output[dbentry.project_country][dbentry.project_site]:
                output[dbentry.project_country][dbentry.project_site][dbentry.projekt_application]={'id':dbentry.project_id,
                 'name':dbentry.project_name, 'description':dbentry.project_description,'systems':dbentry.systems}
            
        return output
        
        