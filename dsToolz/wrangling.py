# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 13:26:35 2019

@author: wiz
"""

import numpy as np
import pandas as pd
import time
from typing import List, Callable, Dict, Tuple
import itertools

class Window:
    """
    A window function performs a calculation across a set of table rows that are somehow 
    related to the current row. This is comparable to the type of calculation that can be 
    done with an aggregate function. But unlike regular aggregate functions, use of a window 
    function does not cause rows to become grouped into a single output row — the rows retain 
    their separate identities. Behind the scenes, the window function is able to access more 
    than just the current row of the query result.
    
    Example (sql):
    --------------
    SELECT start_terminal,
           duration_seconds,
           SUM(duration_seconds) OVER (PARTITION BY start_terminal ORDER BY start_time) AS running_total
    FROM bikeshare
    WHERE start_time < '2012-01-08'
    
    
    Example (Window):
    -----------------
    let bikeshare be a pandas data frame that corresponds to the bikeshare SQL table.
    
    then by using the Window class one can write
    
        assignRunningTotal = Window(partitionBy = 'start_terminal', 
                                    agg = {"duration_seconds": "sum"}, 
                                    name = "running_total", 
                                    where = "start_time < '2012-01-08'", 
                                    orderby = "start_time")
        
        assignRunningTotal.assign(bikeshare)
    
    in order to get the same output
    
    Source of example: https://mode.com/sql-tutorial/sql-window-functions/
    
    """
    def __init__(self, partitionBy: List[str], agg: Dict[str, Callable[[pd.Series], pd.Series]], name: str = "temp_var", where: str = None, orderby: List[str] = None, orderbyasc: bool = True):
        self.partitionBy    = partitionBy
        self.agg            = agg
        self.name           = name
        self.where          = where
        self.orderby        = orderby
        self.orderbyasc     = orderbyasc
        self.columnToMap    = [*self.agg.keys()][0]
        self.function       = [*self.agg.values()][0]
    
    def __prepareDataFrame(self, dataFrame: pd.DataFrame):
        
        if self.orderby is not None:
            dataFrame = dataFrame.sort_values(self.partitionBy + self.orderby, ascending = self.orderbyasc)
        if self.where is not None:
            dataFrame = dataFrame.query(self.where)
        
        return dataFrame
    
    def getColumnToAssign(self, dataFrame: pd.DataFrame) -> pd.DataFrame:
        assert all([c in dataFrame.columns for c in self.agg.keys()])
        assert all([c in dataFrame.columns for c in self.partitionBy])
        
        pdGroupBy = self.__prepareDataFrame(dataFrame).groupby(self.partitionBy)
        
        if self.function == "prev":
            return pdGroupBy[self.columnToMap]\
                            .shift(periods = 1)
                            
        if self.function == "next":
            return pdGroupBy[self.columnToMap]\
                            .shift(periods = -1)
                            
        if self.function == "cumsumlist":
            return pdGroupBy[self.columnToMap]\
                            .apply(lambda x: [set(l) for l in itertools.accumulate(x)])\
                            .rename(self.name)
    
        if isinstance(self.function, str):
            return pdGroupBy.agg(self.agg)\
                            .rename(columns={self.columnToMap : self.name})
    
        elif callable(self.function):
            return pdGroupBy[self.columnToMap]\
                            .apply(self.function)\
                            .rename(self.name)
    
    def assign(self, dataFrame: pd.DataFrame) -> pd.DataFrame:
        
        assert all(c in dataFrame.columns for c in self.partitionBy)
        assert self.columnToMap in dataFrame.columns
        
        newdata = self.getColumnToAssign(dataFrame)
        
        if len(dataFrame) == len(newdata):
            return dataFrame.assign(**{self.name: newdata})
        else:
            if self.name in dataFrame.columns:
                dataFrame = dataFrame.drop(self.name, axis = 1)
                
            return dataFrame.merge(newdata, on = self.partitionBy, how = "left")
    
    def getColumn(self, dataFrame: pd.DataFrame) -> pd.Series:
        """
        using this method instead of the 'assign'-method returns a column instead of a dataframe.
        If one uses this column to assign a new columns, it might be nessesary to reset the index
        of the corresponding dataframe. 
        """
        
        return dataFrame.pipe(self.assign)[self.name]
                