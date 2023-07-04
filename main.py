from sec_filings import SECExtractor
import time
import json
import concurrent.futures
from collections import defaultdict
tickers = ['TSLA','AAPL']
amount = 2
se = SECExtractor(tickers,amount,'10-K',end_date="2022-12-31")

def multiprocess_run(tic):
    print(f"Started for {tic}")
    tic_dict = se.get_accession_numbers(tic)
    text_dict = defaultdict(list)
    for tic,fields in tic_dict.items():
        for field in fields:
            all_text,filing_type = se.get_text_from_acc_num(field['url'])
            text_dict[tic].append({"year":field['year'],"ticker":tic,"all_texts":all_text,"filing_type":filing_type})
    return text_dict
if __name__ =="__main__":           
    start = time.time()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(multiprocess_run,tickers)

    final_dict = []
    for res in results:
        final_dict.append(res)
    json.dump(final_dict, open( "section_text_single.json", 'a' ) )
    # print(final_dict)
    print(f"It took {round(time.time()-start,2)} seconds")