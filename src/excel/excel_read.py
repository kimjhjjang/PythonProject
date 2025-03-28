import os
import csv
import logging as log
from openpyxl import Workbook

log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

csv_folder_path = r"C:\Users\admin\OneDrive\바탕 화면\건강관리협회"
excel_file_path = r"C:\Users\admin\OneDrive\바탕 화면\missing_dept_code.xlsx"

# 엑셀파일 쓰기
write_wb = Workbook()
write_ws = write_wb.active
write_ws.title = 'Missing DEPT_CODE'

# 엑셀 파일 헤더 추가
write_ws.append(["MSG_KEY", "YMD", "HM", "CORP_ID", "PROJECT_ID", "API_KEY", "DEPT_CODE"])

# CSV 파일 처리
for filename in os.listdir(csv_folder_path):
    if filename.endswith(".csv"):
        csv_file_path = os.path.join(csv_folder_path, filename)
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile)
            ymd_counts = {}
            for row in csvreader:
                ymd = row.get("YMD")
                if ymd not in ymd_counts:
                    ymd_counts[ymd] = {"total": 0, "missing_dept_code": 0}
                ymd_counts[ymd]["total"] += 1
                if not row.get("DEPT_CODE"):
                    ymd_counts[ymd]["missing_dept_code"] += 1
                    write_ws.append([row["MSG_KEY"], row["YMD"], row["HM"], row["CORP_ID"], row["PROJECT_ID"], row["API_KEY"], row["DEPT_CODE"]])
            for ymd, counts in ymd_counts.items():
                log.info(f'File: {filename}, YMD: {ymd}, Total rows: {counts["total"]}, Rows with missing DEPT_CODE: {counts["missing_dept_code"]}')

# 엑셀 파일 저장
write_wb.save(excel_file_path)
log.info(f'{excel_file_path} 파일이 저장되었습니다.')