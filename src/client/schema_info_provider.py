from src.database import Mysql

class SchemaInfoProvider(object):

    def __init__(self):
        self.mysql = Mysql()


    def get_tables(self, schema):

        query = '''
            SELECT
                TABLE_SCHEMA AS schema_name,
                TABLE_NAME AS table_name
            FROM
                INFORMATION_SCHEMA.TABLES
            WHERE
                TABLE_TYPE = 'BASE TABLE' and TABLE_SCHEMA = '{}'
            ORDER BY
                TABLE_SCHEMA,
                TABLE_NAME
        '''.format(schema)

        return self.mysql.gets(query)


    def get_table_details(self, schema, table_name):

        query = '''
            SELECT
                UPPER(COLUMN_NAME) AS '필드명(영문)\n(용어 통일성)',
                COLUMN_COMMENT AS '필드(한글)\n(용어 통일성)',
                UPPER(SUBSTRING_INDEX(COLUMN_TYPE, '(', 1)) AS 'TYPE\n(타입 통일성)',
                CHARACTER_MAXIMUM_LENGTH AS '길이\n(길이 통일성)',
                IF(IS_NULLABLE = 'NO', 'N', 'Y') AS 'NULL',
                IF(COLUMN_KEY = 'PRI', 'PK', '') AS 'PK',
                COLUMN_DEFAULT AS '디폴트 값'
            FROM
                INFORMATION_SCHEMA.COLUMNS
            WHERE
                TABLE_SCHEMA = '{}' AND TABLE_NAME = '{}'
            ORDER BY
                ORDINAL_POSITION
        '''.format(schema, table_name)

        return self.mysql.gets(query)


    def get_table_index(self, schema, table_name):
        query = '''
            SELECT
                s.INDEX_NAME AS 인덱스명,
                GROUP_CONCAT(
                    CONCAT(
                        s.COLUMN_NAME, 
                        ' (', 
                        CASE s.COLLATION 
                            WHEN 'A' THEN 'ASC' 
                            WHEN 'D' THEN 'DESC' 
                            ELSE 'NONE' 
                        END, 
                        ')'
                    ) ORDER BY s.SEQ_IN_INDEX ASC
                ) AS 인덱스_칼럼, -- 필드별 순서와 정렬 기준
                CASE
                    WHEN s.INDEX_NAME = 'PRIMARY' THEN '글로벌 (PK)'
                    WHEN s.NON_UNIQUE = 0 THEN '글로벌 (UK)'
                    ELSE '글로벌 (NUK)'
                END AS 인덱스_종류,
                GROUP_CONCAT(DISTINCT s.COLUMN_NAME) AS 주요_컬럼,
                CASE
                    WHEN AVG(s.CARDINALITY / t.TABLE_ROWS) > 0.8 THEN '좋음'
                    WHEN AVG(s.CARDINALITY / t.TABLE_ROWS) BETWEEN 0.4 AND 0.8 THEN '보통'
                    ELSE '나쁨'
                END AS 컬럼분포도
            FROM
                INFORMATION_SCHEMA.STATISTICS s
            LEFT JOIN
                INFORMATION_SCHEMA.TABLES t ON s.TABLE_SCHEMA = t.TABLE_SCHEMA AND s.TABLE_NAME = t.TABLE_NAME
            LEFT JOIN
                INFORMATION_SCHEMA.COLUMNS c ON s.TABLE_SCHEMA = c.TABLE_SCHEMA AND s.TABLE_NAME = c.TABLE_NAME AND s.COLUMN_NAME = c.COLUMN_NAME
            WHERE
                s.TABLE_SCHEMA = '{}' -- 대상 데이터베이스 이름
                AND s.TABLE_NAME = '{}' -- 대상 테이블 이름
            GROUP BY
                s.INDEX_NAME
            ORDER BY
                FIELD(INDEX_NAME, 'PRIMARY') DESC, -- PRIMARY를 먼저 정렬
                s.INDEX_NAME, s.SEQ_IN_INDEX
        '''.format(schema, table_name)

        return self.mysql.gets(query)


    def get_columns(self, schema, table_name):

        query = '''
            SELECT
                COLUMN_NAME
            FROM
                INFORMATION_SCHEMA.COLUMNS
            WHERE
                TABLE_SCHEMA = '{}' AND TABLE_NAME = '{}'
            ORDER BY
                ORDINAL_POSITION
        '''.format(schema, table_name)

        return self.mysql.gets(query)


    def get_data(self, schema, table_name, count):
        query = '''
            SELECT
                *
            FROM
                {}.{}
            LIMIT {}
        '''.format(schema, table_name, count)

        return self.mysql.gets(query)

    def get_daily_data(self):
        query = '''
            SELECT 
                B.CORP_ID, 
                B.CORP_NAME, 
                B.MON_SENDER_LIMIT_AMOUNT AS '월발송한도금액', 
                ROUND(A.USE_AMOUNT,2) AS '사용금액',
                ROUND((A.USE_AMOUNT / B.MON_SENDER_LIMIT_AMOUNT) * 100, 2) AS percent
            FROM (
                SELECT
                    S.CORP_ID,
                    SUM(
                        CASE 
                            WHEN S.PRODUCT_CODE = 'SMS' THEN S.SUCC_CNT * COALESCE(JSON_UNQUOTE(JSON_EXTRACT(U.POST_FEE_INFO, '$[0].POST_FEE')), 9)
                            WHEN S.PRODUCT_CODE = 'LMS' THEN S.SUCC_CNT * COALESCE(JSON_UNQUOTE(JSON_EXTRACT(U.POST_FEE_INFO, '$[0].POST_FEE')), 27)
                            WHEN S.PRODUCT_CODE = 'MMS' THEN S.SUCC_CNT * COALESCE(JSON_UNQUOTE(JSON_EXTRACT(U.POST_FEE_INFO, '$[0].POST_FEE')), 85)
                            WHEN S.PRODUCT_CODE = 'MMSMO' THEN S.SUCC_CNT * COALESCE(JSON_UNQUOTE(JSON_EXTRACT(U.POST_FEE_INFO, '$[0].POST_FEE')), 50)
                            WHEN S.PRODUCT_CODE = 'SMSMO' THEN S.SUCC_CNT * COALESCE(JSON_UNQUOTE(JSON_EXTRACT(U.POST_FEE_INFO, '$[0].POST_FEE')), 7)
                            WHEN S.PRODUCT_CODE = 'KALT1' THEN S.SUCC_CNT * COALESCE(JSON_UNQUOTE(JSON_EXTRACT(U.POST_FEE_INFO, '$[0].POST_FEE')), 6.5)
                            WHEN S.PRODUCT_CODE = 'KALT2' THEN S.SUCC_CNT * COALESCE(JSON_UNQUOTE(JSON_EXTRACT(U.POST_FEE_INFO, '$[0].POST_FEE')), 8)
                            WHEN S.PRODUCT_CODE = 'KFRT1' THEN S.SUCC_CNT * COALESCE(JSON_UNQUOTE(JSON_EXTRACT(U.POST_FEE_INFO, '$[0].POST_FEE')), 12)
                            WHEN S.PRODUCT_CODE = 'KFRM2' THEN S.SUCC_CNT * COALESCE(JSON_UNQUOTE(JSON_EXTRACT(U.POST_FEE_INFO, '$[0].POST_FEE')), 20)
                            WHEN S.PRODUCT_CODE = 'KFRM3' THEN S.SUCC_CNT * COALESCE(JSON_UNQUOTE(JSON_EXTRACT(U.POST_FEE_INFO, '$[0].POST_FEE')), 22)
                            WHEN S.PRODUCT_CODE = 'PUSH' THEN S.SUCC_CNT * COALESCE(JSON_UNQUOTE(JSON_EXTRACT(U.POST_FEE_INFO, '$[0].POST_FEE')), 0.5)
                            WHEN S.PRODUCT_CODE = 'RLMS' THEN S.SUCC_CNT * COALESCE(JSON_UNQUOTE(JSON_EXTRACT(U.POST_FEE_INFO, '$[0].POST_FEE')), 27)
                            WHEN S.PRODUCT_CODE = 'RSMS' THEN S.SUCC_CNT * COALESCE(JSON_UNQUOTE(JSON_EXTRACT(U.POST_FEE_INFO, '$[0].POST_FEE')), 17)
                            WHEN S.PRODUCT_CODE = 'RTPL' THEN S.SUCC_CNT * COALESCE(JSON_UNQUOTE(JSON_EXTRACT(U.POST_FEE_INFO, '$[0].POST_FEE')), 8)
                            WHEN S.PRODUCT_CODE = 'RMMS' THEN S.SUCC_CNT * COALESCE(JSON_UNQUOTE(JSON_EXTRACT(U.POST_FEE_INFO, '$[0].POST_FEE')), 85)
                            WHEN S.PRODUCT_CODE = 'RIMG' THEN S.SUCC_CNT * COALESCE(JSON_UNQUOTE(JSON_EXTRACT(U.POST_FEE_INFO, '$[0].POST_FEE')), 40)
                            ELSE 0
                        END
                    ) AS USE_AMOUNT
                FROM 
                    cm.CM_STAT_CH_DAY S
                LEFT JOIN 
                    cm_console.CM_CORP_PRODUCT_UNIT U 
                    ON S.CORP_ID = U.CORP_ID AND S.PRODUCT_CODE = U.PRODUCT_CODE 
                WHERE
                    S.YMD BETWEEN DATE_FORMAT(NOW(), '%Y-%m-01') AND LAST_DAY(NOW())
                    AND S.CORP_ID IN (
                        SELECT
                            CORP_ID
                        FROM
                            cm_console.CM_CORP
                        WHERE
                            FEE_TYPE = 'POST'
                            AND STATUS = 'USE'
                            AND MON_SENDER_LIMIT_YN = 'Y'
                    )
                GROUP BY
                    S.CORP_ID
            ) A
            JOIN 
                cm_console.CM_CORP B 
                ON A.CORP_ID = B.CORP_ID
            ORDER BY 
                PERCENT DESC;
        '''

        return self.mysql.gets(query)

    def get_dormant_data(self):
        query = '''
            SELECT
                recent_reg.KKO_CH_ID,
                recent_reg.TMPLT_CODE,
                recent_reg.TMPLT_KEY AS recent_reg_TMPLT_KEY,
                recent_reg.DORMANT AS recent_reg_DORMANT,
                recent_reg.USE_YN AS recent_reg_USE_YN,
                recent_upd.TMPLT_KEY AS recent_upd_TMPLT_KEY,
                recent_upd.DORMANT AS recent_upd_DORMANT,
                recent_upd.USE_YN AS recent_upd_USE_YN
            FROM
                (SELECT
                    KKO_CH_ID,
                    TMPLT_CODE,
                    TMPLT_KEY,
                    JSON_UNQUOTE(JSON_EXTRACT(TMPLT_INFO, '$.dormant')) AS DORMANT,
                    USE_YN,
                    REG_DT,
                    ROW_NUMBER() OVER (PARTITION BY TMPLT_CODE ORDER BY REG_DT DESC) AS reg_rank
                FROM CM_KKO_TMPLT_INFO) recent_reg
            JOIN
                (SELECT
                    KKO_CH_ID,
                    TMPLT_CODE,
                    TMPLT_KEY,
                    JSON_UNQUOTE(JSON_EXTRACT(TMPLT_INFO, '$.dormant')) AS DORMANT,
                    USE_YN,
                    UPD_DT,
                    ROW_NUMBER() OVER (PARTITION BY TMPLT_CODE ORDER BY UPD_DT DESC) AS upd_rank
                FROM CM_KKO_TMPLT_INFO) recent_upd
            ON recent_reg.TMPLT_CODE = recent_upd.TMPLT_CODE
                AND recent_reg.reg_rank = 1
                AND recent_upd.upd_rank = 1
                AND (
                    recent_reg.TMPLT_KEY != recent_upd.TMPLT_KEY AND recent_reg.DORMANT != recent_upd.DORMANT AND
                    recent_reg.DORMANT = 'false' and recent_upd.DORMANT = 'true'
                )
            WHERE recent_reg.TMPLT_CODE IN (
                SELECT TMPLT_CODE
                FROM CM_KKO_TMPLT_INFO
                GROUP BY TMPLT_CODE
                HAVING COUNT(*) >= 2
            );
        '''

        return self.mysql.gets(query)


    def get_cmMsg_data(self, ymd, corpId, relay):
        query = '''
            SELECT 
                YMD, 
                MSG_KEY,
                FINAL_CH,
                REG_DT,
                REQ_DT,
                DONE_DT,
            FROM cm.CM_MSG
            WHERE 
                YMD = {}
                AND CORP_ID = {}
                AND RELAY = {}
        '''.format(ymd, corpId, relay)

        return self.mysql.gets(query)


