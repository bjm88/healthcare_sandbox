import pandas as pd
import numpy as np
import string
import re
import matplotlib.pyplot as plt
import seaborn as sns

print("Starting Medical Transcription program...")
print("Starting Medical Transcription data load...")
clinical_text_df = pd.read_csv("./app/data/test/fixtures/mtsamples.csv")
print("Finished Medical Transcription data load.")
print(clinical_text_df.columns)

print("Sample of data:\n " + str(clinical_text_df.head(5)))

clinical_text_df = clinical_text_df[clinical_text_df['transcription'].notna()]
data_categories  = clinical_text_df.groupby(clinical_text_df['medical_specialty'])
i = 1
print('===========Original Categories =======================')
for catName,dataCategory in data_categories:
    print('Cat:'+str(i)+' '+catName + ' : '+ str(len(dataCategory)) )
    i = i+1
print('==================================')


filtered_data_categories = data_categories.filter(lambda x:x.shape[0] > 50)
final_data_categories = filtered_data_categories.groupby(filtered_data_categories['medical_specialty'])
i=1
print('============Reduced Categories ======================')
for catName,dataCategory in final_data_categories:
    print('Cat:'+str(i)+' '+catName + ' : '+ str(len(dataCategory)) )
    i = i+1

plt.figure(figsize=(10,10))
sns.countplot(y='medical_specialty', data = filtered_data_categories )
plt.show()