#!/usr/bin/env python
# coding: utf-8

# In[477]:


# curl -A 'random' https://old.reddit.com/r/mechmarket/new/.json > r-mm-test.json 
# must be ran before script can run

import json
import html
import datetime
import pandas as pd
import re

f = open('r-mm-test.json')

d = json.load(f)


# In[478]:


id_import = pd.read_csv('rmm_id.csv')
id_import['id'].tolist()


# ## Data frame logic

# In[479]:


#pd.read_json('r-mm-test.json')

df = pd.DataFrame.from_dict(d['data']['children'])

#df.apply(lambda row: df['data'][row.name]['author'], axis = 1)
#df['data'][0]


# In[480]:


df2 = pd.concat(
    [
        df
        , df.apply(lambda row: bool(re.match('.*\[US.*\]\s*\[H\].*[Gg][Mm][Kk].*\[W\].*', df['data'][row.name]['title'])), axis = 1)
        , df.apply(lambda row: df['data'][row.name]['title'], axis = 1)
        , df.apply(lambda row: df['data'][row.name]['url'], axis = 1)
        , df.apply(lambda row: df['data'][row.name]['author'], axis = 1)
        , df.apply(lambda row: df['data'][row.name]['id'], axis = 1)
        , df.apply(lambda row: datetime.datetime.fromtimestamp(int(df['data'][row.name]['created_utc'])).strftime('%m/%d %a -- %I:%M:%S %p'), axis = 1)
        , df.apply(lambda row: df['data'][row.name]['selftext_html'], axis = 1)
    ]
    , axis=1, join='inner'
)


# In[481]:


df2.columns = ['kind', 'data', 'hasPattern', 'title', 'url', 'user', 'id', 'ts', 'body']
# df2


# In[482]:


# df3 = df2.loc[df2['hasPattern'] == True]

# check for GMK pattern and is not in the ID list
df3 = df2.loc[~df2['id'].isin(id_import['id'].tolist()) & df2['hasPattern'] == True]
#id_import['id'].tolist()


# In[486]:


#df3.shape[0]


# In[471]:


if df3.shape[0] == 0:
    exit()


# In[468]:


# df3.apply(lambda row: re.sub("[Gg][Mm][Kk]", '<mark style="background-color: orange;">GMK</mark>', html.unescape(row['body'])), axis = 1)[7]


# In[469]:


df4 = pd.concat(
    [
        df3
        , df3.apply(lambda row: """
<tr style="color:white;background-color:#404040">
<td>{}</td>
<td><a style="color:#d9d9d9" href="{}">{}</a></td>
<td><a style="color:#d9d9d9" href="https://old.reddit.com/message/compose/?to={}">/u/{}</a></td>
<td><a style="color:#d9d9d9" href="https://old.reddit.com/user/{}">/u/{}</a></td>
</tr>
<tr>
<td colspan="4">
{}
</td>
</tr>
        """.format(
            row['ts']
            , row['url']
            , row['title'] if len(row['title']) <= 25 else row['title'][0:50] + '...'
            , row['user']
            , row['user']
            , row['user']
            , row['user']
            , re.sub("[Gg][Mm][Kk]",'<mark style="background-color: orange;">GMK</mark>',html.unescape(row['body']))
        ), axis = 1
        )
    ]
    , axis=1, join='inner'
)

df4.columns = ['kind', 'data', 'hasPattern', 'title', 'url', 'user', 'id', 'ts', 'body', 'html']
#df4


# In[ ]:


html_body = '\n'.join(df4['html'].tolist())


# In[ ]:


#id_list =
#.tolist()
df4['id'].to_csv('rmm_id.csv', index=False)


# ## HTML Build and write out

# In[ ]:


html_string="""
<table>
  <tr>
    <th align="left">Posted</th>
    <th align="left">Title</th>
    <th align="left">PM User</th>
    <th align="left">User Profile</th>
  </tr>
{}
</table>
""".format(
    html_body
)


# In[ ]:


# print(html_string)


# In[ ]:


f = open("mutt_test_rmm.html", "w")
f.write(html_string)
#f.write(df3.apply(lambda row: re.sub("[Gg][Mm][Kk]", '<mark style="background-color: orange;">GMK</mark>', html.unescape(row['body'])), axis = 1)[2])

f.close()

# mutt -s "Get your raspberry pi" cris.manlangit@gmail.com < test_body.html

