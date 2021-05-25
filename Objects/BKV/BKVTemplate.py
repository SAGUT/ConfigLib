from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text
from sqlalchemy.orm import relationship
from .BKVChannel import BKVChannel
from .BKVPush import BKVPush
from .BKVRegister import BKVRegister
import json
from ...Database import Base

# Our User object, mapped to the 'users' table
class BKVTemplate(Base):
    __tablename__ = 'tab_bkv_template'

    # Every SQLAlchemy table should have a primary key named 'id'
    bkvtemplate_id = Column(Integer, primary_key=True)
    bkvtemplate_name = Column(String(255))
    bkvtemplate_templateid = Column(String(255))
    bkvtemplate_purpose = Column(Text)
    bkvtemplate_application = Column(String(255))
    bkvtemplate_description = Column(Text)
    bkvtemplate_filelink = Column(String(255))
    registers = relationship("BKVRegister", back_populates="template")
    pushes = relationship("BKVPush", back_populates="template")
    channels = relationship("BKVChannel", back_populates="template")

    def __init__(self, templatedata,application,description,filelink):
        self.templatedata=templatedata
        self.bkvtemplate_application=application
        self.bkvtemplate_description=description
        self.bkvtemplate_filelink=filelink
        self.parseSetup()

    def parseSetup(self):
        self.bkvtemplate_name=self.templatedata['heading'][0]['template_name']
        self.bkvtemplate_purpose=self.templatedata['heading'][0]['purpose']
        self.bkvtemplate_templateid=self.templatedata['heading'][0]['template_id']
        for channel in self.templatedata['channel']:
            bkvchannel_ch_idx = channel['ch_idx']
            bkvchannel_idstr = channel['id']
            bkvchannel_name = channel['name']
            if "limit_negative" in channel:
                bkvchannel_limit_negative = channel['limit_negative']
            else:
                bkvchannel_limit_negative=-1000000
            
            if "limit_positive" in channel:
                bkvchannel_limit_positive = channel['limit_positive']
            else:
                bkvchannel_limit_positive=-1000000
            
            if "offset" in channel:
                bkvchannel_offset = channel['offset']
            else:
                bkvchannel_offset=-1000000
            
            if "transducertype" in channel:
                bkvchannel_transducertype = channel['transducertype']
            else:
                bkvchannel_transducertype="na"

            if "CCS" in channel:
                bkvchannel_CCS = channel['CCS']
            else:
                bkvchannel_CCS=False
            
            if "sensitivity" in channel:
                bkvchannel_sensitivity = channel['sensitivity']
            else:
                bkvchannel_sensitivity=0.0
            
            if "enable" in channel:
                bkvchannel_enable = channel['enable']
            else:
                bkvchannel_enable=False
            
                       
            self.channels.append(BKVChannel(bkvchannel_templateid = self.bkvtemplate_id,
                                            bkvchannel_ch_idx = bkvchannel_ch_idx,
                                            bkvchannel_idstr = bkvchannel_idstr,
                                            bkvchannel_name = bkvchannel_name,
                                            bkvchannel_limit_negative = bkvchannel_limit_negative,
                                            bkvchannel_offset = bkvchannel_offset,
                                            bkvchannel_transducertype = bkvchannel_transducertype,
                                            bkvchannel_CCS = bkvchannel_CCS,
                                            bkvchannel_sensitivity = bkvchannel_sensitivity,
                                            bkvchannel_enable = bkvchannel_enable,
                                            bkvchannel_limit_positive =bkvchannel_limit_positive ))

        for push in self.templatedata['push']:
            bkvpush_bkvid = push['id']
            bkvpush_trigger = push['trigger']
            bkvpush_trigger_data_timer = push['trigger_data']['timer']
            bkvpush_target = push['target']
            if 'trigger' in push['target_data']:
                bkvpush_target_data_trigger =push['target_data']['trigger']
            else:
                bkvpush_target_data_trigger=""
            bkvpush_config_secure= push['config']['secure']
            bkvpush_config_refid = push['config']['refid']
            bkvpush_config_page = push['config']['page']
            bkvpush_config_remote_server = push['config']['remote_server']
            bkvpush_config_port = push['config']['port']
            bkvpush_config_retries = push['config']['retries']
            bkvpush_config_delay = push['config']['delay']
            bkvpush_config_timeout =push['config']['timeout']
            self.pushes.append(BKVPush(bkvpush_bkvid = bkvpush_bkvid,
                                        bkvpush_templateid=self.bkvtemplate_id,
                                        bkvpush_trigger = bkvpush_trigger,
                                        bkvpush_trigger_data_timer = bkvpush_trigger_data_timer,
                                        bkvpush_target = bkvpush_target,
                                        bkvpush_target_data_trigger = bkvpush_target_data_trigger,
                                        bkvpush_config_secure= bkvpush_config_secure,
                                        bkvpush_config_refid = bkvpush_config_refid,
                                        bkvpush_config_page = bkvpush_config_page,
                                        bkvpush_config_remote_server = bkvpush_config_remote_server,
                                        bkvpush_config_port = bkvpush_config_port,
                                        bkvpush_config_retries = bkvpush_config_retries,
                                        bkvpush_config_delay = bkvpush_config_delay,
                                        bkvpush_config_timeout = bkvpush_config_timeout  ))
        
        for register in self.templatedata['vic']:
            if "reg" in register:
                bkvregister_register = register['reg']
            else:
                bkvregister_register=0
            
            if "input" in register:
                bkvregister_input = register['input']
            else:
                bkvregister_input="na"
            
            if "name" in register:
                bkvregister_name = register['name']
            else:
                bkvregister_name="na"
            
            if "physical_quantity" in register:
                bkvregister_physical_quantity = register['physical_quantity']
            else:
                bkvregister_physical_quantity=""
            
            if "unit" in register:
                bkvregister_unit = register['unit']
            else:
                bkvregister_unit=""
            
            if "okrangehigh" in register:
                bkvregister_okrangehigh = register['okrangehigh']
            else:
                bkvregister_okrangehigh=0
            
            if "okrangelow" in register:
                bkvregister_okrangelow = register['okrangelow']
            else:
                bkvregister_okrangelow=0
            
            if "history" in register:
                bkvregister_history = json.dumps(register['history'])
            else:
                bkvregister_history="{}"
             
            self.registers.append(BKVRegister(bkvregister_templateid = self.bkvtemplate_id,
                                            bkvregister_register = bkvregister_register,
                                            bkvregister_input = bkvregister_input,
                                            bkvregister_name = bkvregister_name,
                                            bkvregister_physical_quantity= bkvregister_physical_quantity,
                                            bkvregister_unit = bkvregister_unit,
                                            bkvregister_okrangehigh = bkvregister_okrangehigh,
                                            bkvregister_okrangelow = bkvregister_okrangelow,
                                            bkvregister_history=bkvregister_history             ))






    
    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<BKVTemplate(bkvtemplate_id='%s', bkvtemplate_name='%s')>" % (self.bkvtemplate_id, self.bkvtemplate_name)
