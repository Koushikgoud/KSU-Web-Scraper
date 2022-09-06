import json
from collections import Counter
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
import string
import pandas as pd
import matplotlib.pyplot as plt

with open('ksu1000.json', encoding='utf8') as JSONFile:
    data = json.load(JSONFile)

#Length of pages 
total_length_of_pages = 0
for i in range(len(data)):
    total_length_of_pages += len(str((data)[i]).split())
    doc_len = total_length_of_pages/len(data)
    doc_len = "{:.3f}".format(doc_len)
print("")
print(f"doc_len: {doc_len}")

#Most frequent mails
mail_data = []
for i in range(len(data)):
    mail_data += data[i]['mails']

most_common_emails = [item for item in Counter(mail_data).most_common(10)]
print(f"emails: ")
for i in range(len(most_common_emails)): print(f"           {most_common_emails[i]}")

#Percentage of pages containing atleast one email
mail_containing_pages = 0
for i in range(len(data)):
    number_of_mails = len(data[i]['mails'])
    if number_of_mails > 0:
        mail_containing_pages +=1
perc = (mail_containing_pages/len(data))*100
perc = "{:.2f}".format(perc)
print(f"perc: {perc}%")
print("")



#Most common words before removing stopwords and punctuation
no_of_words = len(str(data).split())
most_common_words = [item for item in Counter(str(data).split()).most_common(30)]
most_common_words = dict(most_common_words)
# Print the names of the columns.
print("{:<10} {:<15} {:<10} {:<10}".format('rank', 'term', 'freq.', 'perc'))
print("{:<10} {:<15} {:<10} {:<10}".format('-----', '-----', '-----', '-----'))
 
# print each data item.
rank = 0
for key, value in most_common_words.items():
    rank +=1
    Frequency = value
    Term = key
    percentage = (Frequency/no_of_words)*100
    percentage = "{:.3f}".format(percentage)
    print("{:<10} {:<15} {:<10} {:<10}".format(rank, Term, Frequency, percentage))



#Most common words after removing stopwords and punctuations
unfiltered_data = ' '.join(str(data).split())
new_stopwords = ["�", "''", "��", "0", "n", "00000", "obj", "endobj", "���", "``"]
stpwrd = nltk.corpus.stopwords.words('english')
stpwrd.extend(new_stopwords)
stop = set(stpwrd + list(string.punctuation))
words_after_removing_stopwords = [i for i in word_tokenize(unfiltered_data.lower()) if i not in stop]
mcw_after_removing_sp = [item for item in Counter(words_after_removing_stopwords).most_common(30)]
mcw_after_removing_sp = dict(mcw_after_removing_sp)

# Print the names of the columns.
print("")
print("{:<10} {:<15} {:<10} {:<10}".format('rank', 'term', 'freq.', 'perc'))
print("{:<10} {:<15} {:<10} {:<10}".format('-----', '-----', '-----', '-----'))
 
# print each data item.
rank2 = 0
for key, value in mcw_after_removing_sp.items():
    rank2 += 1
    Frequency = value
    Term = key
    percentage2 = (Frequency/no_of_words)*100
    percentage2 = "{:.3f}".format(percentage2)
    print("{:<10} {:<15} {:<10} {:<10}".format(rank2, Term, Frequency, percentage2))


#Ploting the most common words before removing stopwords and punctuation
word_data = [item for item in Counter(str(data).split()).most_common(1000)]

word_list = []
word_freq = []
rank = []
r = 0
for i in range(1000):
    word_list.append(word_data[i][0])
    word_freq.append(word_data[i][1])
    r += 1
    rank.append(r)
plt.plot(rank, word_freq)
plt.xlabel("rank")
plt.ylabel("frequency")
plt.show()
print("Viewing plot1")

#log-log Plotting the most common words before removing stopwords and punctuation
plt.loglog(rank, word_freq)
plt.xlabel("rank")
plt.ylabel("log occurrences")
plt.show()
print("Viewing plot2")

