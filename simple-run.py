from requests import get    
from bs4 import BeautifulSoup 

BASE_URL = "http://localhost:8983/solr/trec-covid/select?q="
ID = "cord_uid"
FIELDS = "&fl=" + ID + ",score"
ROWS = "&rows="
rows = 1000
RUN_FILE = 'baseline-title-query.run'
TAG = 'solr-bm25'

with open('topics/topics-rnd5.xml', 'r') as f:
    data = f.read() 

bs_data = BeautifulSoup(data, 'xml') 

topics = bs_data.find_all('topic')

with open(RUN_FILE, 'w') as f_out:
    for topic in topics:
        num = topic.get('number')
        q = "title: (" + topic.query.text.replace(' ', '%20') + ")^2" + topic.query.text.replace(' ', '%20')
        
        url = ''.join([BASE_URL, q, FIELDS, ROWS, str(rows)])
        r = get(url)
        json = r.json()
        
        rank = 1
        
        docs = set()
        
        for doc in json.get('response').get('docs'):
            docid = doc.get('cord_uid')
            if docid not in docs and len(docs) < 1000:
                docs.add(docid)
                score = doc.get('score')
                out_str = '\t'.join([num, 'Q0', docid, str(rank), str(score), TAG])
                f_out.write(out_str + '\n')
                rank += 1