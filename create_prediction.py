
import pandas
columns=["Class","LineNumber"]
df_ = pd.DataFrame(columns=columns)

for i in range(14):
    filename="train_set.txt_14_cache/cluster_files/cluster_"+str(i)+".log"
    data = [line.strip() for line in open(filename, "r").readlines()]
    print(len(data))
    data = [{"LineNumber": line.split('~')[0],"Class":i+1} for line in data]
    data = pandas.DataFrame(data)
    df_=df_.append(data)
    print(df_)
    

df_['sorted_by']=[0 for i in range(df_.shape[0])] 
for i in range(df_.shape[0]):
    df_.iloc[i,2]=int(df_.iloc[i,1][1:])

df_.sort_values("sorted_by",inplace=True)
df_.drop(['sorted_by'],axis=1,inplace=True)
df_.to_csv('log.csv')



    

