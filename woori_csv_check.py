import os
import pandas as pd
import logging as log

# Set up logging
log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define paths
msg_hub_path = r'C:\Users\admin\OneDrive\바탕 화면\메시지허브\운영업무\우리은행\메시지허브발송결과'
biz_talk_path = r'C:\Users\admin\OneDrive\바탕 화면\메시지허브\운영업무\우리은행\비즈톡발송결과'
result_path = r'C:\Users\admin\OneDrive\바탕 화면\메시지허브\운영업무\우리은행\결과'

# Create result directory if it doesn't exist
os.makedirs(result_path, exist_ok=True)

# Define date range
date_range = pd.date_range(start="2025-02-01", end="2025-03-10")

# Initialize a list to store summary data
summary_data = []

for date in date_range:
    date_str = date.strftime("%Y%m%d")
    msg_hub_file = os.path.join(msg_hub_path, f"msghub_{date_str}.csv")
    biz_talk_file = os.path.join(biz_talk_path, f"{date_str}.csv")
    result_file = os.path.join(result_path, f"result_{date_str}.csv")

    if os.path.exists(msg_hub_file) and os.path.exists(biz_talk_file):

        # Read CSV files
        msg_hub_df = pd.read_csv(msg_hub_file)
        biz_talk_df = pd.read_csv(biz_talk_file, low_memory=False)

        log.info(f"data read start for date {date_str} MSG_HUB={len(msg_hub_df)}, BIZ_TALK={len(biz_talk_df)}")

        # Merge dataframes on MSG_KEY and msgIdx
        merged_df = pd.merge(msg_hub_df, biz_talk_df, left_on='MSG_KEY', right_on='msgIdx', how='outer', indicator=True)

        # Initialize result_status column
        merged_df['result_status'] = merged_df['_merge']

        # Update result_status column for different EXT_RESULT_CODE and res values
        def update_result_status(row):
            if row['_merge'] == 'both':
                ext_result_code = str(int(float(row['EXT_RESULT_CODE'])))
                res = str(row['res']).replace('.0', '')
                if ext_result_code == res:
                    return 'true'
                else:
                    # log.info(f"EXT_RESULT_CODE and res mismatch for MSG_KEY={row['MSG_KEY']}: EXT_RESULT_CODE={ext_result_code}, res={res}")
                    return 'false'
            return row['_merge']

        merged_df['result_status'] = merged_df.apply(update_result_status, axis=1)

        # Log discrepancies
        if len(msg_hub_df) != len(biz_talk_df):
            log.warning(f"Data count mismatch for date {date_str}: MSG_HUB={len(msg_hub_df)}, BIZ_TALK={len(biz_talk_df)}")

        # Log missing keys
        missing_keys = merged_df[~merged_df['result_status'].isin(['true', 'false'])]
        missing_msg_keys = []
        missing_msg_idxs = []
        for index, row in missing_keys.iterrows():
            if row['result_status'] == 'left_only':
                log.warning(f"Missing msgIdx in BIZ_TALK for MSG_KEY={row['MSG_KEY']}")
                missing_msg_keys.append(row['MSG_KEY'])
            elif row['result_status'] == 'right_only':
                log.warning(f"Missing MSG_KEY in MSG_HUB for msgIdx={row['msgIdx']}")
                missing_msg_idxs.append(row['msgIdx'])

        # Save merged dataframe to new CSV
        merged_df.to_csv(result_file, index=False)

        # Collect summary data
        summary_data.append({
            'date': date_str,
            'msg_hub_total_count': len(msg_hub_df),
            'biz_talk_total_count': len(biz_talk_df),
            'true_count': merged_df['result_status'].eq('true').sum(),
            'false_count': merged_df['result_status'].eq('false').sum(),
            'left_only_count': merged_df['result_status'].eq('left_only').sum(),
            'right_only_count': merged_df['result_status'].eq('right_only').sum(),
            'missing_msg_keys': ','.join(map(str, missing_msg_keys)),
            'missing_msg_idxs': ','.join(map(str, missing_msg_idxs))
        })

        log.info(f" --------------------------data read end for date {date_str} --------------------------")
    else:
        log.warning(f"Files for date {date_str} do not exist in both directories.")

# Save summary data to CSV
summary_df = pd.DataFrame(summary_data)
summary_df.to_csv(os.path.join(result_path, 'summary.csv'), index=False)