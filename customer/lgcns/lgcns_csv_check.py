import os
import pandas as pd
import logging as log

# Set up logging
log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define paths
msg_hub_path = r'C:\Users\admin\OneDrive\바탕 화면\cmmsg_2025-01-24\메시지허브자료'
lgcns_path = r'C:\Users\admin\OneDrive\바탕 화면\cmmsg_2025-01-24\LGCNS자료'
result_path = r'C:\Users\admin\OneDrive\바탕 화면\cmmsg_2025-01-24\검토결과'

# Create result directory if it doesn't exist
os.makedirs(result_path, exist_ok=True)

# Define date range
date_range = pd.date_range(start="2025-01-24", end="2025-01-24")

# Initialize a list to store summary data
summary_data = []

for date in date_range:
    date_str = date.strftime("%Y%m%d")
    msg_hub_file = os.path.join(msg_hub_path, f"{date_str}.csv")
    lgcns_file = os.path.join(lgcns_path, f"{date_str}.csv")
    result_file = os.path.join(result_path, f"result_20250327.csv")

    if os.path.exists(msg_hub_file) and os.path.exists(lgcns_file):

        # Read CSV files
        msg_hub_df = pd.read_csv(msg_hub_file, low_memory=False)
        lgcns_df = pd.read_csv(lgcns_file, low_memory=False)

        log.info(f"data read start for date {date_str} MSG_HUB={len(msg_hub_df)}, LGCNS={len(lgcns_df)}")

        # Merge dataframes on MSG_KEY and MESSAGE_ID
        merged_df = pd.merge(lgcns_df,msg_hub_df , left_on='MESSAGE_ID', right_on='MSG_KEY', how='outer', indicator=True)

        # Initialize result_status column
        merged_df['result_status'] = merged_df['_merge']

        # Update result_status column for different EXT_RESULT_CODE and res values
        def update_result_status(row):
            if row['_merge'] == 'both':
                code = row['CODE']
                ext_result_code = row['EXT_RESULT_CODE']
                if ext_result_code == code:
                    return 'true'
                else:
                    return 'false'
            return row['_merge']

        merged_df['result_status'] = merged_df.apply(update_result_status, axis=1)

        # 전체 저장
        #merged_df.to_csv(result_file, index=False)

        # 실패건만 저장
        # Filter rows where result_status is 'false'
        #false_results_df = merged_df[merged_df['result_status'] == 'false']
        false_results_df = merged_df[merged_df['result_status'].isin(['false', 'left_only', 'right_only'])]

        # Save filtered dataframe to new CSV
        false_results_df.to_csv(result_file, index=False)

        # Log discrepancies
        if len(msg_hub_df) != len(lgcns_df):
            log.warning(f"Data count mismatch for date {date_str}: MSG_HUB={len(msg_hub_df)}, LGCNS={len(lgcns_df)}")

        # Log missing keys
        missing_keys = merged_df[~merged_df['result_status'].isin(['true', 'false'])]
        missing_msg_keys = []
        missing_msg_idxs = []
        for index, row in missing_keys.iterrows():
            if row['result_status'] == 'left_only':
                log.warning(f"Missing MSG_KEY in MSG_HUB for MESSAGE_ID={row['MESSAGE_ID']}")
                missing_msg_idxs.append(row['MESSAGE_ID'])
            elif row['result_status'] == 'right_only':
                log.warning(f"Missing MESSAGE_ID in LGCNS for MSG_KEY={row['MSG_KEY']}")
                missing_msg_keys.append(row['MSG_KEY'])

        # # Save merged dataframe to new CSV
        # merged_df.to_csv(result_file, index=False)

        # Collect summary data
        summary_data.append({
            'date': date_str,
            'msg_hub_total_count': len(msg_hub_df),
            'lgcns_total_count': len(lgcns_df),
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