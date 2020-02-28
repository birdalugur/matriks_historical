# Put each test result in a separate column and sort from smallest to largest.


import pandas as pd

# path to the file to be read
file_name = 'results/statistics.csv'

# path to the results to be stored
export_path = 'results/ordered_result.csv'

stats = pd.read_csv(file_name, index_col=0)

stats = stats.drop(['dof', 'chi2', 'oddsratio','pair'])

data = stats.reset_index()

x = stats.stack().reset_index()

x.columns = ['test', 'symbol', 'value']

y = x.sort_values(['test', 'value'], ascending=False)

y = y.reset_index(drop=True)

group = y.groupby('test')

group_name = list(group.groups.keys())

list_test = []

for name in group_name:
    res = group.get_group(name).pivot(index='symbol', columns='test',
                                      values='value').sort_values(by=name).reset_index()
    col_names = list(res.columns)
    col_names[0] = col_names[0] + '_' + \
                   ''.join([word[0] for word in col_names[1].split('_')])
    res.columns = col_names
    list_test.append(res)

result = pd.concat(list_test, axis=1)

column_order = result.columns[-4:].append(result.columns[:-4])

ordered_result = result[column_order]

ordered_result.to_csv(export_path, index=False)
