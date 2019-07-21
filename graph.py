import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import io
import base64

matplotlib.use('agg')
data = pd.read_csv('./dataset/framingham.csv')

def create_graphic(X):
    """create graph from the given dictionary X"""
    plt.close('all')
    plt.figure(figsize=(12,6))
    sns.set(style='darkgrid', palette='bright')
    for i,j in enumerate(X):    
        plt.subplot(2, 3, (i+1))
        plt.text(X[j], 0, X[j], color='black')
        plt.axvline(x=X[j], linestyle='--', c='red')
        sns.distplot(data[j].dropna(), bins=30, kde=False)
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    graph = 'data:image/png;base64,{}'.format(graph_url)
    return graph