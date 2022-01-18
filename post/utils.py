import matplotlib.pyplot as plt
import base64
from io import BytesIO
import re

def removeNumbers(items:list):
    new_list = []
    pattern = re.compile(r'\d+[.]\s?')

    for item in items:
        p = pattern.sub("",item)
        new_list.append(p)
    return new_list
    
def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png',bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    return graph

def get_plot(x,y,title):
    plt.switch_backend('AGG')
    # plt.figure(figsize=(10,5))
    # plt.title(title)
    # plt.plot(x,y)
    # plt.xlabel('Products Count')
    # plt.ylabel('Products Name')
    # plt.tight_layout()
    
    # plt.style.use('fivethirtyeight')
    # plt.rcParams.update({'figure.autolayout':True})
    # plt.figure(figsize=(10,40))
    # fig, ax = plt.subplots()
    # ax.barh(x,y)

    plt.rcdefaults()
    plt.figure(figsize=(5,len(y)/2))
    plt.barh(y,x,align='center')
    plt.yticks(y,y)
    plt.title(title)
    plt.xlabel('Products Count')
    plt.ylabel('Products Name')
    plt.tight_layout()
    for a,b in zip(x,y):
        plt.text(a-.4,b,str(a))

    graph = get_graph()
    return graph