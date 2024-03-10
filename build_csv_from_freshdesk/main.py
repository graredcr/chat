
#curl -v -u YilEgKUI6ZpJq63UQnB:X -H "Content-Type: application/json" -X GET 'https://newaccount1637835723861.freshdesk.com/api/v2/tickets'
 
import pandas as pd 

from langchain_community.document_loaders import JSONLoader


loader = JSONLoader(
    file_path='./data/Solutions.json',
    jq_schema='.[5].category.folders[1].articles[]', 
    text_content=False,
    json_lines=True
    )


"""

data = {}
df = pd.DataFrame()

for folder in folders:  
    #if folder['id'] != 101000429751: 
    print("Folder ID::",folder['id'])
    data[folder['id']] = folder
    print('paso1')
    files = getArticles(folder['id'])
    print(files)
    data[folder['id']]['files'] = {}
    for file in files:  
        data[folder['id']]['files'][file['id']] = file 
        print(file['id'],' ',file['title'])
        #if file['title'] != 'VERSION':
            #if file['id'] != 101000359992:
        index = str(file['title']).find('VERSION')
        if index == -1: 
            print('--> dins:: ',file['title'] )
            article = getArticle(file['id'])
        else:
            print('no cal')
        #print(article)
    time.sleep(10)

    #solo admin parapanda
    if folder['id'] == 101000429751:
        dataPanda = []  
        for file in files:  
            print(file['id'],' ',file['title']) 
            index = str(file['title']).find('VERSION')
            if index == -1: 
                print('--> dins:: ',file['title'] )
                article = getArticle(file['id'])
                print('--> ARTIVCLE:: *********************')
                print(article)
                print('--> dins:: *********************')
                # initialize list of lists
                dataPanda.append([file['title'], article] ); 
               
            else:
                print('no cal')

        # Create the pandas DataFrame
        df = pd.DataFrame(dataPanda, columns=['Title', 'Text'])

        #print(article)
        time.sleep(10)
        df.to_csv('./data/manual_'+str(folder['id'])+'.csv', index=False)
        


with open('./data/data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print('Backup creado, fichero data.json')"""
