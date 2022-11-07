import pandera as pa
import numpy as np
import pandas as pd
from pandera import Check, DataFrameSchema, Column,check_io
from utils.error import *
from constants.constants import yamlFile
from constants.constants import *

from utils.enums import datatypes

from ruamel.yaml import round_trip_dump  as yaml_dump

import csv

INDENTATION=2
class TestCases:
    def __init__(self,source,target,dms):
        self.source = source
        self.target = target
        self.dms = dms

    def commonTestCases(self):
        try:
            self.dms["Static Value"] = self.dms["Static Value"].fillna('')
            source = self.source.fillna('')
            # self.dms["Static Value"] = self.dms["Static Value"]
            self.dms['DataType'] = self.dms['DataType'].str.lower()
            list1 = {
                'schema_type': 'dataframe',
                'version': '0.7.0',
                'columns': {

                }
            }
            for index,row in self.dms.iterrows():
                columnName = row["Fields"]
                staticValue=None
                isblank = None
                dataType = row['DataType']
                nullable = not(row["Required Field"]=='Yes' or False)
                if(row["Static Value"] != "<Blank>" and row["Static Value"] != ''):
                    staticValue = row["Static Value"]
                if(row["Static Value"] == '<Blank>'):
                    isblank = ''
                    nullable= True
                checkeq = staticValue or isblank
                list1['columns'][columnName] =   {
                            'required': True,
                            'nullable': nullable,
                        }
                if(pd.notna(row['DataType'])):
                    list1['columns'][columnName]['dtype'] = datatypes[row['DataType']].value
                    list1['columns'][columnName]['coerce'] = True
                if(checkeq is not None):
                    list1['columns'][columnName]['checks'] = {'eq': checkeq}

            with open(yamlFile,'w') as f:
                yaml_dump(list1,f,indent=INDENTATION, block_seq_indent=INDENTATION,default_flow_style=False)
            with open(yamlFile, 'r') as r:
                yaml_schema = r.read()
            schema = pa.DataFrameSchema.from_yaml(yaml_schema)
            schema.validate(source, lazy= True)
            printOk("All tests are successful")
        except pa.errors.SchemaErrors as err:
            printError("Raised when schema validation fails")
            printError(err.failure_cases)
        except Exception as ex:
            printError("Unknown Error:")
            printError(f" {str(ex)}")

#Finding the delimetter used
    def findDelimetter(self):
        with open(devRepLoc) as csvfile:
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(csvfile.read())
            print('Hey there')
            print(dialect.delimiter)