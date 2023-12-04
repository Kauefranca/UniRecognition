import psycopg2

class DatabaseConnection:
    def __init__(self, host, database, user, password, port='5432'):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            return True
        except psycopg2.Error as e:
            print(f"Erro ao conectar no banco de dados: {e}")
            return False

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Desconectado do banco de dados")

    def execute_query(self, query, parameters=None):
        if not self.connection:
            print("Conexão com o banco fechada. utilize connect() antes.")
            return None

        try:
            with self.connection.cursor() as cursor:
                if parameters:
                    cursor.execute(query, parameters)
                else:
                    cursor.execute(query)
                
                result = cursor.fetchall()
                return result
        except psycopg2.Error as e:
            print(f"Erro ao executar query: {e}")
            return None

    def execute_update(self, query, parameters=None):
        if not self.connection:
            print("Conexão com o banco fechada. utilize connect() antes.")
            return False

        try:
            with self.connection.cursor() as cursor:
                if parameters:
                    cursor.execute(query, parameters)
                else:
                    cursor.execute(query)
                
                self.connection.commit()
                return True
        except psycopg2.Error as e:
            print(f"Erro ao executar o update: {e}")
            return False