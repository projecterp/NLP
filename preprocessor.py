
# coding: utf-8

# In[7]:


import re
import pickle
import stemmer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

#fp = open("/home/pranav/classes.txt","r")
with open('stop_words.pickle', 'rb') as handle:
    stop_words = pickle.load(handle)
stemmer = stemmer.Stemmer('english')    
#paragraphs = fp.readlines()


# In[8]:


def add_to_dictionary(word, dictionary, keywords):
    if word not in stop_words:
        keywords.add(stemmer.stemWord(word))
    if word in dictionary:
        dictionary[stemmer.stemWord(word)] += 1
    else :
        dictionary[stemmer.stemWord(word)] = 1    

def process_word(word, dictionary, keywords):
    number = re.search("(^[\d]+)|($[\d]+)", word)
    if number is None or len(number.group()) != len(word):
        if re.search("(www\.)|([\S]+\@)([\S]+\.[\S]+)", word) is None:
            word = word.replace(".","")   
        add_to_dictionary(word.lower(), dictionary, keywords)        
        
def process_line(line, dictionary, words, keywords):
    pattern = r'[\w][\S]*[\w]'
    word_list = re.findall(pattern, line)
    words = words + word_list
    for word in word_list:
        process_word(word, dictionary, keywords)
        
def get_words(line):
    pattern = r'[\w][\S]*[\w]'
    word_list = re.findall(pattern, line)
    if word_list is None:
        return []
    return word_list

def get_lines(para):
    pattern = "[\.|\?\!] "
    splitter = re.compile(pattern)
    return splitter.split(para);

def process_paragraph(paras, dictionary, lines, words, keywords):
    for para in paras:
        para = para.strip()
        para = re.sub("\n","",para)
        lines = lines + [line for line in get_lines(para) if line.strip()!=""]
    for line in lines:
        process_line(line,dictionary, words, keywords)

def perc(a1,a2):
    return (a1/a2)*100

def pie_plotter(dictionary, keywords, words):
    labels = 'Keywords', 'Stop-words', 'Repeats'
    sizes = [perc(len(keywords),len(words)), perc((len(dictionary) - len(keywords)),len(words)),perc((len(words) - len(dictionary)),len(words))]
    explode = (0.1, 0.2, 0.1)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    plt.show()  

def bar_plotter(dictionary, keywords, words):
    labels = []
    freq = []
    for word in keywords:
        if dictionary[word]>=5:
            labels.append(word)
            freq.append(dictionary[word])
    plt.bar(range(len(freq)), freq)
    plt.xticks(range(len(freq)), labels, rotation = "vertical")
    plt.gcf().set_size_inches(18.5,10.5)
    plt.show()
    
    
# In[4]:


#process_paragraph(paragraphs)


# In[6]:


'''
print ("\n####################################################################################\n")
print ("The number of paragraphs is ", len(paragraphs),"\n")
print ("The number of sentences is ", len(lines),"\n")
print ("The number of words is ", len(words),"\n")
print ("Total no. of words in vocabulary is ", len(dictionary), "\n")
print ("Total no. of stop words in vocabulary is ", len(dictionary), "\n")
print ("The number of keywords in vocabulary is ", len(keywords), "\n") 
print ("\n####################################################################################\n")
plotter()
bar_plotter()
print ("\n####################################################################################\n")
for k,v in sorted(dictionary.items(), key=lambda p:p[1], reverse=True):
    print(k.rjust(30), " : ", v)
'''    

