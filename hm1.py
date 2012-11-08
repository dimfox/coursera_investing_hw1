import os
from datetime import date
import math
import numpy

path = "C:/Users/wei/Downloads/QSData/Yahoo"

all_stocks = {}
all_sharpo = {}

def read_files(path):
    for fname in os.listdir(path):
        if not fname.endswith('.csv'): continue
        rec = get_adj_close(os.path.join(path,fname))
        if len(rec) != 252: continue
        all_stocks[fname[:-4]] = rec
        

def get_adj_close(filename):
    with open(filename) as f:
        recs =[(p[0].strip(), p[6].strip()) for p in 
              (line.split(",") for line in f)]
        def to_date(dstr):
            parts = dstr.split('-')
            parts = [int(p) for p in parts]
            return date(*parts)
            
        recs = [(to_date(a[0]), float(a[1])) for a in recs[1:]
                if date(2011,1,1) <= to_date(a[0]) <= date(2011,12,31)]
        f.close()
        return sorted(recs)
      
def extract_adj_close(ticker):
    return [a[1] for a in all_stocks[ticker]]
    
def get_sharpo(adj_close):
    
    adj_close_diff = []
    for i in range(1, len(adj_close)):
        adj_close_diff.append(adj_close[i] - adj_close[i-1])
        
    avg = numpy.average(adj_close_diff)
    std = numpy.std(adj_close_diff)
    return math.sqrt(len(adj_close)) * avg/std
    
def get_combine_sharpo(tickers, init_invest=None):
    """evenly spread the money between input tickers
    and calculate sharpo ration"""
        
    adj_closes = [
        extract_adj_close(ticker)
        for ticker in tickers]
    
    first_day_close = [close[0] for close in adj_closes]
    if not init_invest:
        # evenly split if not specified
        init_invest = [1 for _ in tickers]
        
    shares = [init/close for (init, close) in zip(init_invest, first_day_close)]
    
    n_of_days = len(adj_closes[0])
        
    fund_total = []
    for i in range(n_of_days):
        day_total = sum(close[i] * share for (close, share) in zip(adj_closes, shares))
        fund_total.append(day_total)
    
    daily_chg = [(day2-day1)/fund_total[0] for (day2, day1) 
                 in zip(fund_total[1:], fund_total[0:-1])]
                 
    daily_chg = [0.0] + daily_chg # add first day's change (0.00% chg)
    
    avg = numpy.average(daily_chg)
    std = numpy.std(daily_chg)
    return math.sqrt(len(daily_chg)) * avg/std
  
def two_cmb_sharpo(tickers):
    combs = []
    for i in range(len(tickers)):
        s1 = tickers[i]
        for j in range(i+1, len(tickers)):
            s2 = tickers[j]
            cmb_ratio = get_combine_sharpo([s1,s2])
            combs.append((cmb_ratio, s1, s2))
    combs.sort(reverse=True)
    return combs
    
def three_cmb_sharpo(two_cmbs, one_stocks):
    combs = [tuple(sorted((s1, s2, s3)))
             for s1, s2 in two_cmbs
             for s3 in one_stocks
             if s3 not in (s1, s2)]
    combs = set(combs)
    combs2 = [(get_combine_sharpo(r),) + r for r in combs]
    combs2.sort(reverse=True)
    return combs2
    
def four_cmb_sharpo(three_cmbs, one_stocks):
    combs = set(tuple(sorted((s1, s2, s3, s4)))
             for s1, s2, s3 in three_cmbs
             for s4 in one_stocks
             if s4 not in (s1, s2, s3))
             
    combs2 = [(get_combine_sharpo(r),) + r
              for r in combs]
    combs2.sort(reverse=True)
    return combs2
    
def write_cmb_to_file(file_name, combs):
    output_file = open(file_name,'w')
    for r in combs:
        output_file.write(",".join(str(a) for a in r))
        output_file.write('\n')
    output_file.close()
    
def read_cmb_from_file(file_name):
    f = open(file_name)
    def parse_line(line):
        parts = [p.strip() for p in line.split(",")]
        return tuple([float(parts[0])] + parts[1:])
    
    return [parse_line(line) for line in f]
    
def get_all_sharpo():
    all_sharpo = {}
    for ticker in all_stocks:
        all_sharpo[ticker] = get_sharpo(extract_adj_close(ticker))
        good_stock.append((ticker, sharpo))
        
    good_stock.sort(key=lambda x: x[1])    
    return good_stock
    
def split_shares(n_of_stocks, total_parts, cur=()):
    """yield a list of numbers that sum up to 'total_parts'
    """
    if n_of_stocks == 0 and total_parts == 0:
        yield cur
        
    if n_of_stocks > 0 and total_parts > 0:
        for to_take in range(1, total_parts  - n_of_stocks + 1 + 1):
            for res in split_shares(n_of_stocks - 1, total_parts - to_take, cur + (to_take,)):
                yield res
      
def improve_share_split(stocks, total_shares=8):
    return max((get_combine_sharpo(stocks, shares), shares)
               for shares in split_shares(len(stocks), total_shares))
      
def best_splits(cmbs, total_shares=8):

    output_threshold = 4.4
    for cmb in cmbs:
        stocks = cmb[1:]
        (sharpo, share_split) = improve_share_split(stocks, total_shares)
        if sharpo >= output_threshold:
            print stocks, sharpo, share_split
            
def printlog(*s):
    from datetime import datetime
    print str(datetime.now()), ":",
    for a in s:
        print a,
    print

def write_adj_close_to_file(ticker):
    file_name = '%s.csv' % ticker
    f = open(file_name, 'w')
    for day, price in all_stocks[ticker]:
        f.write('%s,%s\n' % (day, price))
    f.close()
    
def main(steps=(2, 3, 4, 'improve')):
    # read files from disk
    read_files(path)
    printlog("all stocks: ", len(all_stocks))
    
    # cal sharpo for all stocks
    for ticker in all_stocks:
        all_sharpo[ticker] = get_sharpo(extract_adj_close(ticker))
    printlog("done with sharpo for one stock.")
    
    # -------------------------------------------------
    # One stock
    # -------------------------------------------------
    # get stocks with sharpo ration > 0
    good_stock = [ (t, all_sharpo[t]) for t in all_sharpo
                  if all_sharpo[t] > 0]
    good_stock.sort(key=lambda x: x[1])
    printlog("done with filter out good stock. Good stocks: ", len(good_stock))
    
    # -------------------------------------------------
    # two stock with good ones only
    # -------------------------------------------------
    two_cmb_file = 'two_cmbs.csv'
    if 2 in steps:
        # calculate sharpo ratio for all combination of two stocks
        # evenly split the money
        two_cmbs = two_cmb_sharpo([stock[0] for stock in good_stock])
        write_cmb_to_file(two_cmb_file, two_cmbs)
    else:
        # read from the file
        two_cmbs = read_cmb_from_file(two_cmb_file)
    printlog("done with two stock combinations.")
    
    # -------------------------------------------------
    # three stock
    # -------------------------------------------------
    three_cmb_file = 'three_cmbs.csv'
    if 3 in steps:
        three_cmbs = three_cmb_sharpo(
            [(p[1], p[2]) for p in two_cmbs[:250]],
            [p[0] for p in good_stock])
        write_cmb_to_file(three_cmb_file, three_cmbs)
    else:
        three_cmbs = read_cmb_from_file(three_cmb_file)
    printlog("done with three stock combinations.")
    
    # -------------------------------------------------
    # four stocks
    # -------------------------------------------------
    four_cmb_file = 'four_cmbs.csv'
    if 4 in steps:
        four_cmbs = four_cmb_sharpo(
            [(p[1], p[2], p[3]) for p in three_cmbs[:600]],
            [p[0] for p in good_stock])
        write_cmb_to_file(four_cmb_file, four_cmbs)
    else:
        four_cmbs = read_cmb_from_file(four_cmb_file)
    printlog("done with four stock combinations.")
    
    if 'improve' in steps:
        best_splits(four_cmbs[:400], 20)
    
if __name__ == '__main__':
    main((2,3,4,'improve',))
        
    #stocks = ('PGN', 'PM', 'ROST', 'UST')
    #for ticker in stocks:
    #    write_adj_close_to_file(ticker)
    
    #print stocks, improve_share_split(stocks, 20)

    