#Document clustering program : using K-means clustering and cosine similarity measure 
#Here this program is coded to produce 3 clusters i.e creates 3 folders and insersts similar document as a result/output 

from nltk.tokenize import word_tokenize
from nltk import FreqDist
import sys
from math import sqrt
import os
import random

reload(sys)

sys.setdefaultencoding('Utf8')
#----------------------------------------------------------------------------------------------------
# function retuns a zerow row matrix of length n
def getZeroRowMatrix(n) :
      l = []
      i=0 
      while(i<n) :
          l.append(float(0))
          i+=1
      return l

#-------------------------------------------------------------------------------------------------
                         #data preprocessing steps

#removing previoulsy documents in the clustered folder
os.system("rm cluster_1/d*") #
os.system("rm cluster_2/d*")
os.system("rm cluster_3/d*")

os.system("rmdir clu*")# remove all cluster directories

# we have mixed-up the file names so that we can easily verify it 
files_names =["doc3","doc7","doc5","doc4","doc2","doc6","doc1","doc8","doc9"] #filesnames present in document folder to be clustered

helping_words = [] #used to sotre helping words and remove from them from document to keep important words

all_words = [] #to sotre list of all words presnt in all document 

file_words = [] #is a list of ( list of word of file) 
file_words_freq = [] #is a list of ( dictionary of frequency of words in file)

file_freq_matrix =[] #to store only frequency of words in file


file1 = open("helping words",'r') #open the helping words file in read mode
txt = file1.readlines()  

#tokenize the words present in the helping wods file
for line in txt :
    l = line.strip('\n').lower()
    helping_words+= word_tokenize(str(l))

file1.close() # close the helping words file


#read words of each file and sotre in file_words list 
for filename in files_names :
     file1 = open("document/"+filename,'r')
     txt = file1.readlines()
     l1 = []
     for line in txt :
         l = line.strip('\n').lower()
         z= word_tokenize(str(l))
         m = []
         for x in z :
                if x not in helping_words :
                      m.append(x)
         l1+=m
     n = FreqDist(l1)
     file_words_freq.append(n)
     file_words.append(n.keys())
     file1.close()

#store all words in all_words list
for x in file_words :
    all_words+=x

all_words = FreqDist(all_words).keys() #remove repeated words


i = 0 #variable to iterate loop
# initalize rows for the frequency matrix
while i < len(files_names) :
    file_freq_matrix.append(getZeroRowMatrix(len(all_words)))
    i+=1



j = 0 #variable to iterate loop
#for every words in all_words list check its presence in file find its requenct and assign it to frequency matrix/vector
for x in all_words :
     i = 0
     while i < len(files_names) :
          if x in file_words[i] :
               file_freq_matrix[i][j] = float(file_words_freq[i][x])
          i+=1  
        
     j+=1    


                      #end of data preprocessing
#--------------------------------------------------------------------------------------------------

                     #pre process for algorithms

file_len = [] #to store length of file (length in terms of vector )

i = 0 #variable to iterate loop
#find length of wodrs of all file  eg: lenght of [a b] = sqrt(a*a + b*b)
for x in file_freq_matrix :
     sum1 = 0.0
     for y in x :
       sum1+= float(y*y)
     sum1 = sqrt(sum1)
     file_len.append(sum1)



#------------------------------------------------------------------------------------------

file_cosine = [] #to store cosine similarity , its a symmetric matrix

i=0 #variable to iterate loop
#initalize rows of cosine similarity matrix
while i< len(file_len):
    file_cosine.append(getZeroRowMatrix(len(file_len)))
    i+=1

i = 0#variable to iterate loop
j = 0#variable to iterate loop
# find the cosine similarity of each files
while i < len(file_freq_matrix) :
   j = i + 1
   while j < len(file_freq_matrix) :
      k = 0
      sumcos = 0.0
      while k <len(file_freq_matrix[i]) :
          sumcos+= file_freq_matrix[i][k]*file_freq_matrix[j][k]
          k+=1
      sumcos = sumcos/(file_len[i]*file_len[j])
      file_cosine[i][j]=file_cosine[j][i] = round(float(sumcos),4)
      j+=1
   file_cosine[i][i] = round(float(1.0),4)
   i+=1


              # end of preprocess for algorithm 
  
#--------------------------------------------------------------------------------------

#initially take some random  3 files for clustering 
p1 =  random.randrange(0,len(file_len)-1,1) #holds index of 1st random file
p2 = 0 #holds index of 2nd random file
p3 = 0 #holds index of 3rd random file
#make sure p1,p2 is different
while(True) :
   p2 = random.randrange(0,len(file_len)-1,1)
   if p2 != p1 :
         break
#make sure all 3 are different
while True :
  p3 = random.randrange(0,len(file_len)-1,1)
  if p3 != p1 and p3 != p2 :
      break 



#--------------------------------------------------------------------------------------

#here we make use of index of file in files_names list and group them to form clusters

pl1 = [] # to store previous cluster 
pl2 = []
pl3 = []

l1 = []# to store current cluster
l2 = []
l3 = []

err1 = []
err2 = []
err3 = []

#k-means clustering

while True :
    #assing previous values
    pl1 = l1 ; pl2 = l2 ; pl3 = l3
    l1 = [] ; l2 = [] ;l3 = []
    err1 = [] ; err2 = [] ; err3 = []

    i = 0
    d1 = 0.0 ; d2 = 0.0 ; d3 = 0.0
    #find files having similarity using cosine similarity matrix
    while i < len(file_cosine) :
        d1 = file_cosine[p1][i]
        d2 = file_cosine[p2][i]
        d3 = file_cosine[p3][i]
        if d1 > d2 and d1 > d3 :
            l1.append(i)
        elif d2 > d1 and d2 > d3 :
            l2.append(i)
        else :
            l3.append(i)
        i+=1
    l1.sort();l2.sort();l3.sort()
    #if any of the cluster is empty continue from first
    if ( len(l1) == 0 or len(l2) == 0 or len(l3) == 0 ) :
           l1 = []; l2 =[] ; l3 =[]
           p1 =  random.randrange(0,len(file_len)-1,1)
           p2 =  random.randrange(0,len(file_len)-1,1)
           p3 =  random.randrange(0,len(file_len)-1,1)
           continue 

    #get the cosine similarity value for each clusters 
    all_val_l1 = []; all_val_l2 = []; all_val_l3 = [];
    for x in l1 :
        all_val_l1.append( file_cosine[p1][x]);

    for x in l2 :
        all_val_l2.append( file_cosine[p2][x]);

    for x in l3 :
        all_val_l3.append( file_cosine[p3][x]);
   
   #finding the mean of cosine similarity of the clusters 
    mean_c1 = sum(all_val_l1)/len(all_val_l1)
    mean_c2 = sum(all_val_l2)/len(all_val_l2)
    mean_c3 = sum(all_val_l3)/len(all_val_l3)

    #finding error b/w mean cosine and the actual value  
    for x in all_val_l1 :
      err1.append(abs(mean_c1 - x)) ;
 
    for x in all_val_l2 :
      err2.append(abs(mean_c2 - x)) ;

    for x in all_val_l3 :
      err3.append(abs(mean_c3 - x)) ;

    
    
    p1 = l1[err1.index(min(err1))] # finding the leading document for cluster 1 i.e the one with min error from mean
    p2 = l2[err2.index(min(err2))] # finding the leading document for cluster 2 i.e the one with min error from mean
    p3 = l3[err3.index(min(err3))] # finding the leading document for cluster 3 i.e the one with min error from mean

    print "p1 = ",p1," p2 = ",p2," p3 = ",p3 

    #check previous and current clusters if they are same or not
    flag = abs(cmp(l1,pl1)) + abs(cmp(l2,pl2))  + abs(cmp(l3,pl3))
    if flag == 0 :
       break # break the loop if clusters are same

    

  
#-------------------------------------------------------------------------------------------------------------------------


#create new directories to insert clustered file
os.mkdir("cluster_1")
os.mkdir("cluster_2")
os.mkdir("cluster_3")

#copy 1st cluster of files to 1st directory
for x in l1 :
  os.system("cp document/"+files_names[x]+" cluster_1")

#copy 2nd cluster of files to 2nd directory
for x in l2 :
   os.system("cp document/"+files_names[x]+" cluster_2")

#copy 3rd cluster of files to 3rd directory
for x in l3 :
  os.system("cp document/"+files_names[x]+" cluster_3")

#--------------------------------------------------------------------------------------------------

print" done with clustring "
