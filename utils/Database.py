#############################################
## <실습18> 데이터베이스 제어 모듈 생성 
## 예제8-13 데이터베이스 제어 모듈
## /utils/Database.py
#############################################
import pymysql

class Database:
    '''
    데이터베이스 제어
    '''
    def __init__(self, host, user, password, db_name, charset='utf8'):
        self.host = host
        self.user = user
        self.password = password
        self.charset = charset
        self.db_name = db_name
        self.conn = None

    def connect(self):
        if self.conn != None:  # db가 이미 연결되어 있을 때?
            print("======  Database.py Database.connect 함수 ===========")
            print("@@ DB 연결 실패!")
            return

        print(self.db_name, "연결 시작")
        self.conn = pymysql.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            db = self.db_name,
            charset = self.charset
        )
        print("DB 연결 성공!!!")

    # DB 연결 닫기
    def close(self):
        if self.conn is None:  # 이미 close 상태이면 돌아감
            return

        if not self.conn.open:  # db가 open되어 있지 않다면
            self.conn = None
            return

        self.conn.close()       # db 닫고
        self.conn = None        # 변수를 None으로
        print("DB가 닫혔습니다.")

    # SELECT 구문 실행 후 단 1개의 데이터 ROW만 불러옴
    def select_one(self, sql):
        result = None
        print("============== Database.py ===================")
        print("## Database.py의 select_one함수, sql=")
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()   ### 데이터 하나만 가져옴

        except Exception as ex:
            print("select_one Error : ", ex)

        finally:
            return result

    # SELECT 구문 실행 후 전체 데이터 ROW를 불러옴
    def select_all(self, sql):
        result = None
        print("============== Database.py ===================")
        print("## Database.select_all 함수:  sql=", sql)
        try:
            #### pymysql.cursor가 아니라~ cursors 로 쓸것!!!!!!
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()  # 조회된 모든 데이터를 딕셔너리로...
        except Exception as ex:
            print("select_all Error : ", ex)
        finally:
            return result

