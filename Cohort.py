# import libraries 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import datetime as dt

# load in the data and take a look 
data = pd.read_excel("/Users/Asus/Downloads/Online Retail.xlsx")


#drop rows with no customer ID
data = data.dropna(subset=['CustomerID'])
#create an invoice month


#function for month
def get_month(x):
    return dt.datetime(x.year, x.month,1)
#apply the function 
data['InvoiceMonth'] = data['InvoiceDate'].apply(get_month)
#create a column index with the minimum invoice date, also know as first time customer was acquired
data['Cohort Month'] =  data.groupby('CustomerID')['InvoiceMonth'].transform('min')
#print(data.head(30))


# create a date element function to get a series for subtraction
def get_date_elements(df, column):
    #day = df[column].dt.day
    month = df[column].dt.month
    year = df[column].dt.year
    return  month, year 
#date dorkar nai tai nei nai
# get date elements for our cohort and invoice columns
Invoice_month,Invoice_year =  get_date_elements(data,'InvoiceMonth')
Cohort_month,Cohort_year =  get_date_elements(data,'Cohort Month')

#create a cohort index 
year_diff = Invoice_year - Cohort_year
month_diff = Invoice_month - Cohort_month
data['CohortIndex'] = year_diff*12+month_diff+1

#count the customer ID by grouping by Cohort Month  and Cohort Index 
cohort_data = data.groupby(['Cohort Month','CohortIndex'])['CustomerID'].apply(pd.Series.nunique).reset_index()
print(cohort_data)
# create a pivot table 
cohort_table = cohort_data.pivot(index='Cohort Month', columns=['CohortIndex'],values='CustomerID')

# change index
cohort_table.index = cohort_table.index.strftime('%B %Y')
#visualize our results in heatmap
plt.figure(figsize=(21,10))
sns.heatmap(cohort_table,annot=True,cmap='Blues')

#cohort table for percentage
new_cohort_table = cohort_table.divide(cohort_table.iloc[:,0],axis=0)
#create a percentages visual
plt.figure(figsize=(21,10))
print(sns.heatmap(new_cohort_table,annot=True,fmt='.0%'))
