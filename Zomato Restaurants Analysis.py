#!/usr/bin/env python
# coding: utf-8

# # Work showing cheap resturant with good ratings(by average).

# In[163]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('dark_background')
zomato=pd.read_csv('zomato.csv')


# In[164]:


zomato.head()


# In[165]:


zomato.shape


# In[166]:


zomato.duplicated().value_counts()


# # Can Also check for df.drop_duplicates()

# In[167]:


zomato.drop_duplicates(inplace=True)


# In[168]:


zomato.shape


# In[169]:


zomato.isnull().sum()


# In[170]:


zomato.rate.unique()


# In[171]:


zomato[zomato.rate=='NEW' ]


# In[172]:


def func(x):
    if x == '-' or x=='NEW':
        return np.nan
    else:
        x=str(x).split('/')
        x=x[0]
        return float(x)
       


# In[173]:


zomato['rate']=zomato['rate'].apply(func)


# In[174]:


#zomato['rates']=zomato.rate.dropna().apply(lambda x: x[0:3])
#zomato.rates


# In[175]:


zomato.rate.unique()


# In[176]:


zomato.shape


# In[177]:


zomato.rate.mean()


# In[178]:


zomato['rate'].fillna(zomato.rate.mean(),inplace=True)
zomato.rate.isna().sum()


# In[179]:


zomato.isna().sum()


# In[180]:


zomato.dropna(inplace=True)


# In[181]:


zomato.columns


# In[182]:


zomato.rename(columns={'approx_cost(for two people)':'cost_for_2','listed_in(type)':'type','listed_in(city)':'city'},inplace=True)


# In[183]:


zomato.columns


# In[184]:


zomato[zomato.cuisines.isna()]


# In[ ]:





# In[185]:


zomato.dtypes


# In[186]:


zomato.info()


# In[ ]:





# In[187]:


zomato[['name','rate','reviews_list','votes','cost_for_2']]


# In[188]:


zomato.cuisines.str.contains('Indian').value_counts()


# In[189]:


zomato.city.unique()


# In[190]:


zomato.location.unique()


# City is te subset of location so we are replacing the city. 

# In[191]:


zomato.drop('city',axis='columns',inplace=True)
zomato.head()


# In[192]:


zomato.cost_for_2.unique()


#  def con(x):
#     if ',' in str(x):
#         x=x.replace(',','')
#         return float(x)
#     else:
#         return float(x)

# In[193]:


zomato['cost_for_2']=zomato.cost_for_2.str.replace(',','').astype(float)


# In[194]:


zomato.cost_for_2.unique()


# In[195]:


zomato.rest_type.unique()


# In[196]:


rest_types = zomato['rest_type'].value_counts(ascending  = False)
rest_types


# In[ ]:





# In[197]:


rest_types_lessthan1000 = rest_types[rest_types<1000]
rest_types_lessthan1000


# In[198]:


rest_types[zomato.rest_type.value_counts()<1000]


# In[199]:


def rest(x):
    if x in rest_types_lessthan1000:
        return 'others'
    else:
        return x


# In[200]:


zomato['rest_type']=zomato.rest_type.apply(rest)
zomato.rest_type.value_counts()


# In[201]:


zomato.location.value_counts()


# In[202]:


locations=zomato.location.value_counts()
locatons_lessthan250=locations[zomato.location.value_counts()<250]
locatons_lessthan250


# In[203]:


def location(x):
    if x in locatons_lessthan250:
        return 'others'
    else:
        return x


# In[204]:


zomato['location']=zomato['location'].apply(location)
zomato.location.value_counts()


# In[205]:


cusine=zomato.cuisines.value_counts()


# In[206]:


(cusine[zomato.cuisines.value_counts()<100].shape)[0]-(cusine[zomato.cuisines.value_counts()<50].shape)[0]


# In[208]:


cusine[zomato.cuisines.value_counts()<50]


# In[209]:


def cusine(x):
    if x in cusine_lessthan50:
        return 'others'
    else:
        return x
zomato['cuisines']=zomato.cuisines.apply(cusine)
zomato.cuisines.value_counts()


# In[210]:


zomato.head()


# In[211]:


zomato1=zomato[zomato['rate']>=4.0]


# In[212]:


zomato1.head()


# In[213]:


zomato1=zomato1.sort_values(by=['rate'],ascending=[False])


# In[214]:


zomato1.head()


# In[215]:


zomato1.info()


# In[216]:


zomato1.describe()


# In[219]:


zomato1[zomato1['cost_for_2']<=1000].sort_values(by=['cost_for_2']).head(20)


# In[ ]:





# In[36]:


zomato1[(zomato1['approx_cost(for two people)']<=1000) & (zomato1['rates']>'4.5')]


# In[37]:


c=zomato1.votes.value_counts().sum()


# In[38]:


zomato1.reviews_list


# In[39]:


zomato1['rates']=zomato1.rates.astype(float)


# In[40]:


zomato1['avg_ratings']=(zomato1['rates']*zomato1['votes'])/c


# In[41]:


zomato1.sort_values(by=['avg_ratings','approx_cost(for two people)']).tail()


# In[221]:


plt.figure(figsize = (16,10))
ax = sns.countplot(zomato['location'])
plt.xticks(rotation=90)


# In[223]:


plt.figure(figsize=(10,10))
sns.countplot(zomato.book_table,palette='rainbow')


# In[224]:


plt.figure(figsize = (10,10))
sns.boxplot(x = zomato.online_order, y = zomato.rate) 


# In[225]:


plt.figure(figsize = (10,10))
sns.boxplot(x = zomato.book_table, y = zomato.rate) 


# In[226]:


df=zomato.groupby(by=['location','online_order'])
df.head()  


# In[227]:


df=zomato.groupby(['location','online_order'])['name'].count()
df.to_csv('df.csv')
df=pd.read_csv('df.csv')
df=pd.pivot_table(df,index=['location'],columns=['online_order'],aggfunc=np.sum)


# In[228]:


df.plot(kind='bar',figsize=(15,15))


# In[229]:


df1=zomato.groupby(['location','book_table'])['name'].count()
df1.to_csv('df.csv')
df1=pd.read_csv('df.csv')
df1=pd.pivot_table(df1,index=['location'],columns=['book_table'],aggfunc=np.sum)
df1.plot(kind='bar',figsize=(15,10))


# In[232]:


plt.figure(figsize=(15,10))
sns.boxplot(x=zomato.type,y=zomato.rate,palette='rainbow')


# In[234]:


plt.figure(figsize=(30,10))
sns.boxplot(x=zomato.cuisines,y=zomato.rate,palette='inferno')
plt.xticks(rotation=90)


# In[ ]:




