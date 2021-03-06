import numpy as np
import pandas as pd

contacts = pd.read_csv('../../resource/CleansedData/ModifiedData/Contacts_001_deleted_korean.csv')
accounts = pd.read_csv('../../resource/CleansedData/ModifiedData/Accounts_001_concat_state.csv')
potentials = pd.read_csv('../../resource/CleansedData/ParsedData/Potentials_001_droppedCol.csv')

# print(accounts['Territories'].unique())

# 3134/7088
# print(accounts['Territories'].isna().sum())
# 1338/4070
# print(contacts['Territories'].isna().sum())


# 23 'Arun Sharma' 'Mahesh Gulwani' 'Taukheer Ahmed' 'Karn Sharma'
#  'Ashwini Dixit' 'Anees Mukhtar' 'Shubham Tonk' 'Ayan' 'CS/Amazon/Other'
#  'Nasir' 'Nihal Pawar' 'Dixiata Sharma' 'Aaruni Sinha' 'Chris Shin'
#  'Mrunal Sardar' 'Mohammad Afnan' 'Gurraj Singh' 'Kenneth Cha'
#  'Prasad Gosavi' 'Ankita' 'Abhinanda Ghosh' 'Puneet Shukla'
#  'Neelabh Kashyap'
# print(accounts['Sales Person'].nunique(),accounts['Sales Person'].unique())

# 22 'Karn Sharma' 'Arun Sharma' 'Mahesh Gulwani' 'Taukheer Ahmed'
#  'Kenneth Cha' 'Anees Mukhtar' 'Shubham Tonk' 'Ashwini Dixit'
#  'Nihal Pawar' 'Nasir' 'Dixita Sharma' 'Ayan' 'Chris Shin' 'Mrunal Sardar'
#  'Afnan Mohammed' 'Gurraj Singh' 'Aaruni Sinha' 'Prasad Gosavi'
#  'Puneet Shukla' 'Ankita' 'Neelabh Kashyap' 'Abhinanda Ghosh'
# print(contacts['Sales Person'].nunique(), contacts['Sales Person'].unique())

territories = {}
owner_id = {}

# 1. 직원별 territory dict 저장
for i in contacts.index:
    if pd.notnull(contacts.loc[i, 'Sales Person']) and pd.notnull(contacts.loc[i, 'Territories']):
        name = contacts.loc[i, 'Sales Person']
        territory = contacts.loc[i, 'Territories']
        if name not in territories:
            territories[name] = []
        territories[name].append(territory)

# territory dict 출력 - 8개
name_list = []
for name in territories:
    if len(set(territories[name])) == 1:
        # print(name, ':', set(territories[name]))
        name_list.append(name)


# 2. id 별 territory
for i in contacts.index:
    if pd.notnull(contacts.loc[i, 'Territories']):
        id = contacts.loc[i, 'Customer Owner ID']
        territory = contacts.loc[i, 'Territories']
        if id not in owner_id:
            owner_id[id] = []
        owner_id[id].append(territory)

# territory dict 출력 - 9개
id_dict = {}
for id in owner_id:
    if len(set(owner_id[id])) == 1:
        # print(id, ':', set(owner_id[id]))
        id_dict[id] = owner_id[id][0]

# 1. 직원별 territory dict 고유값 채워주기 - 3개
for i in contacts.index:
    if contacts.loc[i, 'Sales Person'] in name_list and pd.isnull(contacts.loc[i, 'Territories']):
        person_name = contacts.loc[i, 'Sales Person']
        if person_name in ['Taukheer Ahmed', 'Dixita Sharma']:
            contacts.loc[i, 'Territories'] = 'South'
        elif person_name in ['Ayan', 'Afnan Mohammed', 'Gurraj Singh', 'Neelabh Kashyap', 'Abhinanda Ghosh']:
            contacts.loc[i, 'Territories'] = 'West 1'
        elif person_name == 'Prasad Gosavi':
            contacts.loc[i, 'Territories'] = 'North'

# 2. id별 territory dict 고유값 채워주기 - 10개
for i in contacts.index:
    if contacts.loc[i, 'Customer Owner ID'] in id_dict and pd.isnull(contacts.loc[i, 'Territories']):
        contacts['Territories'][i] = id_dict[contacts.loc[i, 'Customer Owner ID']]
        # print(id_dict[contacts.loc[i, 'Customer Owner ID']], contacts['Territories'][i])


# 3. deal의 CompanyID와 연동하여 territory 찾기
count=0
company_id = {}
for i in contacts.index:
    if pd.isna(contacts["Territories"][i]):
        count+=1
        c_id = contacts.loc[i, 'Company ID']
        company_id[c_id] = []

# print('no territory:',len(company_id))
# 964 territory가 없는 고유 company id 개수
# print('count:',count)
# 1325 territory가 없는 총 company id 개수 (중복있는 company id 362개)

for i in potentials.index:
    if potentials.loc[i]['Company ID'] in company_id and pd.notnull(potentials['Territory'][i]):
        id = potentials['Company ID'][i]
        territory = potentials['Territory'][i]
        company_id[id].append(territory)

company_id_new = {}
for id in company_id:
    if len(set(company_id[id])) == 1:
        # print(id, ':', set(owner_id[id]))
        company_id_new[id] = company_id[id][0]

# 3.  CompanyID별 고유 territory 채우기
for i in contacts.index:
    if contacts.loc[i, 'Company ID'] in company_id_new and pd.isnull(contacts.loc[i, 'Territories']):
        contacts['Territories'][i] = company_id_new[contacts.loc[i, 'Company ID']]
# null 1319개
# print(contacts['Territories'].isnull().sum())



# 4. company id가 없는 데이터 175개

no_company =[]
for i in contacts.index:
    if pd.isnull(contacts.loc[i, 'Company ID']):
        no_company.append(contacts.loc[i, 'Record Id'])

# print(no_company)
# print(len(set(no_company)))


# contacts에서 no_company_id 중 deal에 company id가 있는 customer id
# contacts company id 채우기
comp_custom = {}
for i in potentials.index:
    if potentials.loc[i, 'Customer ID'] in no_company and pd.notnull(potentials.loc[i, 'Company ID']):
        custom_id = potentials.loc[i, 'Customer ID']
        com_id = potentials.loc[i, 'Company ID']
        comp_custom[custom_id] = com_id

for i in contacts.index:
    if contacts.loc[i, 'Record Id'] in comp_custom and pd.isnull(contacts.loc[i, 'Company ID']):
        contacts.loc[i, 'Company ID'] = comp_custom[contacts['Record Id'][i]]

# Parsing the dataset
contacts.to_csv('../resource/CleansedData/Contacts_001_fillTerritory_ver1.csv', index=False)

