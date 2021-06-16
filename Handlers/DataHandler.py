import logging
from ..LibFrame import applicationDict
from pathlib import Path
from datetime import datetime
import pytz
import json
import pyarrow as pa
import pyarrow.parquet as pq
from ..Datasources.FileServer import FileServer
import pandas as pd
class DataHandler(object):

    def __init__(self):
        self.config=applicationDict['config']
        self.fileserver=FileServer()

    def processSetup(self,setup ):
        starttime=setup['starttime']
        endtime=setup['endtime']
        targetdir=Path(setup['directory'])
        datedict=self.getDays(starttime,endtime)
        self.data=dict()
        refid=0
        signalmeta=dict()
        for signalid,parameter in setup['signals'].items():
            print(signalid)
            if parameter['proc']=="ref":
                refid=signalid
            self.data[signalid]={"process":parameter['proc'],"dataframe":self.getDataframe(signalid,datedict)}
            calcsig=applicationDict["dbconn"].getCalculatedSignal(signalid)
            signalmeta[signalid]={'name':calcsig.signal_name,"signal_azureid":calcsig.signal_azureid,"unit":calcsig.signal_measurementUnit}
        
        
        #save meta data
        filename=setup['filename']+".json"
        filelink=targetdir  /filename
        fp=open(filelink,"w")
        json.dump(signalmeta,fp)
        fp.close()
        #now make one dataframe
        resultdf=self.data[refid]['dataframe']
        for signalid,data in self.data.items():
            if signalid!=refid:
                adddf=data['dataframe']
                adddf.drop('timestamps',1, inplace=True)
                print(adddf)
                resultdf = pd.merge_asof(resultdf,adddf ,on='datetime',	tolerance=pd.Timedelta("40sec"), direction="nearest")
        
        table = pa.Table.from_pandas(resultdf)
        filename=setup['filename']+".parquet"
        filelink=targetdir  /filename
        pq.write_table(table, filelink)

        #write meta data



    def getSynchedFrame(self,timedf,dt):
        reduceddf=timedf
        reduceddf[['mean','min', 'max', 'std']]=self.reduceddf.apply(lambda row : self.getAggregate(row['timestamps']), axis = 1,result_type ='expand')
        return reduceddf
    
    def getAggregate(self,timestamp):
        rslt_df = self.dataframe.loc[(self.dataframe['timestamps'] >= (timestamp-self.signal_param1))&(self.dataframe['timestamps'] < (timestamp+self.signal_param1))]
        aggre=rslt_df.agg({'speed':['mean','min', 'max','std']})['speed']
        #print(rslt_df.agg({'speed':['min', 'max','std']})['speed']['min'])
        return [aggre['mean'],aggre['min'],aggre['max'],aggre['std']]
    
    def getDataframe(self,signalid,datedict):
        dataframes=[]
        for year in datedict.keys():
            for month in datedict[year].keys():
                for day in datedict[year][month].keys():
                    print(year,month,day,signalid)
                    scalarfile=applicationDict["dbconn"].getScalarFile(signalid,year,month,day)
                                            
                    dataframe=self.fileserver.getScalarDataframe(scalarfile.scalarfile_link)
                    dataframes.append(dataframe)
        resultdf=dataframes[0]
        for i in range(len(dataframes)-1):
            resultdf=resultdf.append(dataframes[i+1])
        resultdf.index.name = 'datetime'
        return resultdf


    def getDays(self,starttime,endtime):
        startdt=datetime.utcfromtimestamp(int(starttime/1000))
        nullstartdt=datetime(startdt.year,startdt.month,startdt.day,0,0,0,0, pytz.UTC)
        nullstarttime=int(1000*nullstartdt.timestamp())
        datedict=dict()
        currenttime=nullstarttime
        while currenttime<endtime:
            currentdt=datetime.utcfromtimestamp(int(currenttime/1000))
            year=currentdt.year
            month=currentdt.month
            day=currentdt.day
            if not year in datedict:
                datedict[year]=dict()
            if not month in datedict[year]:
                datedict[year][month]=dict()
            datedict[year][month][day]={"starttime":currenttime,"endtime":currenttime+(24*60*60*1000)}
            print(year,month,day)
            currenttime=currenttime+(24*60*60*1000)
        return datedict