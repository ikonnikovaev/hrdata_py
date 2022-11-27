import pandas as pd
import requests
import os

# scroll down to the bottom to implement your solution

if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('A_office_data.xml' not in os.listdir('../Data') and
        'B_office_data.xml' not in os.listdir('../Data') and
        'hr_data.xml' not in os.listdir('../Data')):
        print('A_office_data loading.')
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('B_office_data loading.')
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('hr_data loading.')
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)
        print('Loaded.')

        # All data in now loaded to the Data folder.

    a_file_path = '../Data/A_office_data.xml'
    b_file_path = '../Data/B_office_data.xml'
    hr_file_path = '../Data/hr_data.xml'

    a_df = pd.read_xml(a_file_path)
    b_df = pd.read_xml(b_file_path)
    hr_df = pd.read_xml(hr_file_path)

    # print('Data from office A:')
    # print(a_df.axes)
    # print(a_df.shape)
    # print(a_df.info)
    #
    # print('Data from office B:')
    # print(b_df.axes)
    # print(b_df.shape)
    # print(b_df.info)
    #
    # print('HR data:')
    # print(hr_df.axes)
    # print(hr_df.shape)
    # print(hr_df.info)

    a_df['employee_office_id'] = 'A' + a_df['employee_office_id'].astype(str)
    b_df['employee_office_id'] = 'B' + b_df['employee_office_id'].astype(str)
    a_df.set_index('employee_office_id', inplace=True)
    b_df.set_index('employee_office_id', inplace=True)
    hr_df.set_index('employee_id', inplace=True)

    # print(a_df.head())
    # print(b_df.head())

    # print(list(a_df.index.values))
    # print(list(b_df.index.values))
    # print(list(hr_df.index.values))

    office_df = pd.concat([a_df, b_df])
    # print(office_df)

    merged_df = office_df.merge(hr_df, left_index=True, right_index=True, indicator=True)
    merged_df.drop(columns=['_merge'], inplace=True)
    merged_df.sort_index(inplace=True)
    # print(merged_df)

    # print(list(merged_df.index.values))
    # print(list(merged_df.columns.values))
    # print(merged_df.nlargest(10, 'average_monthly_hours')['Department'].tolist())
    print(merged_df.sort_values('average_monthly_hours', ascending=False).head(10)['Department'].tolist())
    print(merged_df.query("Department == 'IT' & salary == 'low'").number_project.sum())
    print(merged_df.loc[['A4', 'B7064', 'A3033'], ['last_evaluation', 'satisfaction_level']].values.tolist())

