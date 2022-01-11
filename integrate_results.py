import os
import pandas as pd

ID_COLUMN_TITLE = 'user_id'
BLOCK_NUM_TITLE = 'block_num'

FINAL_RESULT_FILENAME = 'all_results.csv'

RES_PATH = './results' 

def main():
  os.chdir(RES_PATH)
  csv_filenames = os.listdir()
  all_dfs = []
  for f in csv_filenames:
    if 'csv' not in f or f == FINAL_RESULT_FILENAME:
      continue
    id_block, _ = f.split('.')
    id, block = id_block.split('_')
    df = pd.read_csv(f)
    df[ID_COLUMN_TITLE] = int(id)
    df[BLOCK_NUM_TITLE] = int(block)
    all_dfs.append(df)

  combined_results = pd.concat(all_dfs, sort=False)

  combined_results.to_csv(FINAL_RESULT_FILENAME, index=False, encoding='utf-8-sig')

if __name__ == '__main__':
  main()

