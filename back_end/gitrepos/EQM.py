import argparse
from itertools import combinations 
import sqlite3


# other code. . .
def All_Pair_Check_Mode_0(DB):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM CC WHERE call_name LIKE 'MPI_Scatter()' OR call_name LIKE 'MPI_Scatterv()' ")
    rows = c.fetchall()
    idx = 0
    RANGE = 10
    hist = {}
    hist['mixed'] = 0 
    hist['pure'] = 0
    hist['pure-repeated'] = 0
    hist['mixed-repeated'] = 0
    while idx < (len(rows)):
        sub_idx = 1
        MIXED = False
        while((idx+ sub_idx < len(rows)) and rows[idx][0].decode() == rows[idx +sub_idx][0].decode()):
            sub_idx += 1
        for i, j in list(combinations(range(sub_idx), 2)):
            if(str(rows[idx+i][1]) == str(rows[idx+j][1])):
               if abs(rows[idx+i][2] - rows[idx+j][2]) < RANGE:
                   hist['pure-repeated'] += 1 
            else:
               if abs(rows[idx+i][2] - rows[idx+j][2]) < RANGE:
		   MIXED = True
                   hist['mixed-repeated'] += 1
        if MIXED:
            hist['mixed'] += 1
        else:
            hist['pure'] += 1
        idx += sub_idx
        
    print('Range: ' + str(RANGE))
    print('Total Mixed: ' + str(hist['mixed']))
    print('Total Pure: ' + str(hist['pure']))
    print('Total Chunks: ' + str(hist['pure'] + hist['mixed']))
    print('same %s-Repeated: ' % RANGE + str(hist['pure-repeated']))
    print('diff %s-Repeated: ' % RANGE + str(hist['mixed-repeated']))
       



    conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Elastic Query Manger for Probing the Database for Potential Complex Collectives')
    parser.add_argument('mode', type=int, help='Select Mode for Probing') 
    parser.add_argument('database', type=str, help='Database')
    args = parser.parse_args()
    
    if (args.mode == 0):
        All_Pair_Check_Mode_0(args.database)

