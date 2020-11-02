# standard libs
import datetime as dt
from collections import Counter

# third party libs
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib import lines as mlines
from matplotlib.axes import Axes
from pandas import factorize
from typing import List, Union

from .common import normalizeCounter, prettyNumber, uniqueList

def piePlot(counter: Counter, labels: str = None, title: str = None, savepath: str = None, digits: int = 0, startangle: int = 0, explode: list = None, colors = None, ax = None):

    if ax is None:
        fig, ax = plt.subplots()
    
    sizes = normalizeCounter(counter).values()

    if labels is None:
        labels = list(counter.keys())
    
    ax.pie(sizes, explode=explode, colors = colors, labels=labels, autopct=f'%1.{digits}f%%', startangle=startangle)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    
    if title is not None:
        ax.set(title = title)

    if savepath is not None:
        plt.savefig(savepath) 



def casePlot(case_index: List[int], start: List[dt.date], end: List[dt.date], hue: List[str] = None, hue_lines: List[str] = None, hue_lines_colors: List[str] = None, na_values = dt.date.today(), ax: Axes = None, **kwargs):

    if ax is None:
        fig, ax = plt.subplots()
    
    if type(start) != list:
        start = list(start)
    if type(end) != list:
        end = list(end)
    if type(case_index) != list:
        case_index = list(case_index)       
    
    # samling ad datoer, og case_index
    date       = start + end
    case_index = case_index + case_index
    
    # Plot - get dots
    if hue is None:
        sns.scatterplot(x = date, y = case_index, color = 'blue', ax = ax, **kwargs)
    else:
        if type(hue) != list and hue is not None:
            hue = list(hue)
            
        hue = hue + hue
        sns.scatterplot(x = date, y = case_index, hue = hue, ax = ax)
    
    # Lines in plt
    isUnfinished = pd.isnull(end)
    end__ = [pd.Timestamp(na_values) if unfinished else e for e, unfinished in zip(end, isUnfinished)]
    
    if hue_lines is None:
        ax.hlines(case_index, xmin = start, xmax = end__)
    
    # if hue_lines non-empty
    elif hue_lines is not None:
        
        if hue_lines_colors is None:
            hue_lines_colors  = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"] 
        for i in range(10):
            hue_lines_colors = hue_lines_colors + hue_lines_colors
        cols = hue_lines_colors
        mapIntToCol = dict(enumerate(cols)).get
        hue_line_colors = list(map(mapIntToCol, factorize(hue_lines)[0]))
        hue_lines_unique = uniqueList(hue_lines)
        
        
        ax.hlines(case_index, xmin = start, xmax = end__, colors = hue_line_colors, zorder=1)
        
        # legend
        handles_lines = [mlines.Line2D([], [], color=hue_lines_colors[i], marker='_', markersize=15, label=label) for i, label in enumerate(hue_lines_unique)]
        
        if hue is not None:
            ax.legend(handles = ax.legend_.legendHandles + handles_lines)
        else:
            ax.legend(handles = handles_lines)
        
        
    
    ax.set(xlabel = 'Year', ylabel = 'Case Index')
    ax.set_yticks(case_index)
    ax.set_yticklabels(case_index)
    ax.invert_yaxis()

    
def kpiPlot(title: str, info: Union[int, str], color: str, ax: Axes):
    ax.pie([1], colors = [color], labels=[""])
    centre_circle = plt.Circle((0,0),0.78,fc='white')
    
    ax.add_artist(centre_circle)
    ax.text(0, 1.45 ,title, va='top', ha='center',  fontsize=18, weight='bold')
    ax.text(0,0 ,prettyNumber(info), va='top', ha='center',  fontsize=16, weight='bold')
    
    return ax