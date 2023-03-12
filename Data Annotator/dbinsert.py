#Insert the original reviews data to the postgresql database

import pandas as pd
import sqlalchemy #for postgresql connection

df0=pd.read_csv('Industrial_and_Scientific.csv')
df = df0[df0.verified == True]
df = df[df['reviewText'].notnull()]
df = df[df['reviewText'].apply(lambda x: len(x.split()) > 3)]
df = df[['overall', 'reviewText' ,'summary']]
df.rename(columns = {'reviewText':'reviewtext'}, inplace = True)
df2 = df[df.overall <= 4]
df2 = df2.dropna()
df7 = df[df.overall == 5]
df7 = df7.dropna()
df8 = df7.head(df2.shape[0])
frames = [df2, df8]
result = pd.concat(frames)
result = result.sample(frac = 1)


username = 'ravi'  # change this
password = 'ravi'  # change this
host = 'localhost'  # change this
port = 5432  # change this
database = 'datamanagment'
database_type = 'postgresql'

engine = sqlalchemy.create_engine("{}://{}:{}@{}:{}/{}".format(database_type, username, password, host, str(port), database))
result.to_sql('reviewsoriginal', engine, if_exists='append', index=False)

print('Done')