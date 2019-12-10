import os

import altair as alt
import pandas as pd

df_list = []


# read multiple files
# add them to list of dfs
# then use plt to make viz
# files = ['./outputs/22d9fef70609bcf75ff47c330a722b40e2814b84_summary.csv',
# './outputs/31dbe3bb839c0c8b5bdb7d373a094c94136454a0_summary.csv',
# './outputs/61d652a21ec871b501ce45ba7e34dc10440714c7_summary.csv',
# './outputs/80f8244cf8b7959084652bd0618a60992928a84f_summary.csv',
# './outputs/c38ed7a48c216a296c6a2a19d3f837c8d1c03237_summary.csv'
#          ]
def absoluteFilePaths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


files = absoluteFilePaths('./outputs/')

for f in files:
    df = pd.read_csv(f)
    df_list.append(df)
    print(len(df.index))

data = df_list[0]
print(data['source'].unique())
i = 0

for data in df_list:
    chart = alt.Chart(data).transform_aggregate(
        count='count()',
        groupby=['source']
    ).transform_window(
        rank='rank(count)',
        sort=[alt.SortField('count', order='descending')]
    ).transform_filter(
        alt.datum.rank < 50
    ).mark_bar().encode(
        y=alt.Y('source:N',
                sort=alt.EncodingSortField(field='count', op='sum', order='descending')
                ),
        x='count:Q',
    )

    i += 1

    chart.save('chart' + str(i) + '.html')

# fig1 = plt.figure()
# ax1 = fig1.add_subplot(111)
# for df in df_list:
#
#     c = df.groupby(df['timeline']).count()
#     print(c)
#     ax1.plot(c)
#
# fig1.savefig('lol.png')
