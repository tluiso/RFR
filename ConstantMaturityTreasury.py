# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 18:25:14 2017

@author: luisota
"""

import urllib
import pandas as pd
import datetime
'''
Class for US Constant Maturity Treasury Rates

Attributes
==========
rel      : H15 - Federal Reserve H.15 Daily Rates
series   : bf17364827e38702b42a58cf8eaa3f78
lastobs  : null
from     : Start Date ('mm/dd/yyyy')
to       : End Date ('mm/dd/yyyy')
filetype : csv/spreadsheetml/sdmx
label    : include/omit
layout   : seriescolumn/seriesrow/serieslist


Methods
==========
rate: float
    return rate commensurate with term
'''
class ConstantMaturityTreasury:
    def __init__(self,date):
        self.date     = date
        self.rel      = 'H15'
        self.series   = 'bf17364827e38702b42a58cf8eaa3f78'
        self.lastobs  = ''
        self.date     = date
        self.filetype = 'csv'
        self.label    = 'omit'
        self.layout   = 'seriesrow'
        
        url = 'https://www.federalreserve.gov/datadownload/Output.aspx?'
        params = urllib.parse.urlencode([('rel',self.rel),
                                         ('series',self.series),
                                         ('lastobs',''),
                                         ('from',self.date.strftime('%m/%d/%Y')),
                                         ('to',self.date.strftime('%m/%d/%Y')),
                                         ('filetype',self.filetype),
                                         ('label',self.label),
                                         ('layout',self.layout)])
        url += params
        
        self.curve= pd.read_csv(url) # Risk-free Rate Curve
        
        # Rename ValDate rates
        self.curve = self.curve.rename(index=str,columns={self.date.strftime('%Y-%m-%d'):'Rate'})
        
        # Find Tenors
        self.curve['Tenor'] = self.curve['Series Name:'].apply(lambda x: x[-7:-4])
        
        # Set Terms
        self.curve['Term']  = self.curve['Tenor'].apply(lambda x: float(x[1:])/12 if (x[0]=='M') else float(x[1:]))
        
        self.curve['Rate'] = self.curve['Rate'].astype(float)
        # Set Tenor to Index
        #self.curve.set_index(['Tenor'],inplace=True)
        #del self.curve.index.name
    
    def rate(self, term):
        term = float(term)
        pos = 0
        for index, row in self.curve.iterrows():
            if term >= row['Term']:
                pos = int(index)
        if pos == 0:
            rate = self.curve['Rate'][pos]
        elif pos == len(self.curve)-1:
            rate = self.curve['Rate'][pos]
        else:
            rate =  (term-self.curve['Term'][pos])/(self.curve['Term'][pos+1]-self.curve['Term'][pos]) \
                    *(self.curve['Rate'][pos+1]-self.curve['Rate'][pos]) \
                    + self.curve['Rate'][pos]
        return rate * 10**(-2)
        
        
