#!/usr/bin/env python
# coding: utf-8

# In[1]:


from load_data import get_data_from_db


# In[2]:


import pandas as pd
from imblearn.under_sampling import NearMiss
from datetime import datetime
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder


# In[3]:


data = get_data_from_db(query="select * from filtered_weather_with_count_incidents")


# In[4]:


data


# Extract features and target variable

# In[5]:


X = data.drop(columns=['has_incident', 'grid_id'])
y = data['has_incident']


# Label encode datetime columns

# In[6]:


label_encoder = LabelEncoder()
X['dt_iso'] = label_encoder.fit_transform(X['dt_iso'])


# One-hot encode categorical columns

# In[7]:


X = pd.get_dummies(X, columns=['weather_main'])


# In[9]:


X


# Initialize NearMiss

# In[10]:


nm = NearMiss(sampling_strategy=0.3, version=1) 


# Fit and transform the dataset

# In[11]:


X_resampled, y_resampled = nm.fit_resample(X, y)


# Combine the resampled features and target variable into a new dataframe

# In[12]:


df_resampled = pd.concat([X_resampled, y_resampled], axis=1)


# In[13]:


print(df_resampled)

