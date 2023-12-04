import json
import sqlite3

import pandas as pd


class DB():
    years = ["2018", "2019", "2020", "2021", "2022", "2023"]
    initial_path = "./static/"
    
    def InsertCsvViagem(self):
        for year in self.years:
            csv_file_path = f'{self.initial_path}csv/{year}_Viagem.csv'
            df = pd.read_csv(csv_file_path, encoding='latin-1', sep=';')
            
            sqlite_db_path = f'{self.initial_path}db/data.db'
            conn = sqlite3.connect(sqlite_db_path)
            df.to_sql(f'viagem_{year}', conn, index=False, if_exists='replace')
            
            conn.commit()
            conn.close()
            
    def InsertCsvTrecho(self):
        for year in self.years:
            csv_file_path = f'{self.initial_path}csv/{year}_Trecho.csv'
            df = pd.read_csv(csv_file_path, encoding='latin-1', sep=';')
            
            sqlite_db_path = f'{self.initial_path}db/data.db'
            conn = sqlite3.connect(sqlite_db_path)
            df.to_sql(f'trecho_{year}', conn, index=False, if_exists='replace')
            
            conn.commit()
            conn.close()
            
    def InsertCsvPagamento(self):
        for year in self.years:
            csv_file_path = f'{self.initial_path}csv/{year}_Pagamento.csv'
            df = pd.read_csv(csv_file_path, encoding='latin-1', sep=';')
            
            sqlite_db_path = f'{self.initial_path}db/data.db'
            conn = sqlite3.connect(sqlite_db_path)
            df.to_sql(f'pagamento_{year}', conn, index=False, if_exists='replace')
            
            conn.commit()
            conn.close()
            
    def InsertCsvPassagem(self):
        for year in self.years:
            csv_file_path = f'{self.initial_path}csv/{year}_Passagem.csv'
            df = pd.read_csv(csv_file_path, encoding='latin-1', sep=';')
            
            sqlite_db_path = f'{self.initial_path}db/data.db'
            conn = sqlite3.connect(sqlite_db_path)
            df.to_sql(f'passagem_{year}', conn, index=False, if_exists='replace')
            
            conn.commit()
            conn.close()    

    def InsertCsvAll(self):
        self.InsertCsvViagem()
        self.InsertCsvTrecho()
        self.InsertCsvPagamento()
        self.InsertCsvPassagem()
        
    def GetMostVisitedCities(self):
        most_visited_city_per_year = {}
        conn = sqlite3.connect(f'{self.initial_path}db/data.db')
        cursor = conn.cursor()
        for year in self.years:

            sql_query = """
            SELECT "Destino - Cidade", COUNT(*) AS visit_count
            FROM {}
            GROUP BY "Destino - Cidade"
            ORDER BY visit_count DESC
            LIMIT 3;
            """.format(f"trecho_{year}")

            cursor.execute(sql_query)

            results = cursor.fetchall()
            
            most_visited_city_per_year[year] = {}

            for row in results:
                city, visit_count = row
                most_visited_city_per_year[year][city] = visit_count
        conn.close()
        return most_visited_city_per_year
    
    def GetMostTicketsCostsOrg(self):
        most_tickets_costs_org_per_year = {}
        conn = sqlite3.connect(f'{self.initial_path}db/data.db')
        cursor = conn.cursor()
        for year in self.years:
            viagem_table = f"viagem_{year}"
            pagamento_table = f"pagamento_{year}"
            id_column = "Identificador do processo de viagem"
            valor_passagens_column = "Valor passagens"
            orgao_pagador_column = "Nome do órgao pagador"

            sql_query = f"""
            SELECT {pagamento_table}."{orgao_pagador_column}", SUM({viagem_table}."{valor_passagens_column}") AS total_valor_passagens
            FROM {viagem_table}
            INNER JOIN {pagamento_table} ON {viagem_table}."{id_column}" = {pagamento_table}."{id_column}"
            WHERE {pagamento_table}."{orgao_pagador_column}" != 'Sigiloso'
            GROUP BY {pagamento_table}."{orgao_pagador_column}"
            ORDER BY total_valor_passagens DESC
            LIMIT 1;
            """
            cursor.execute(sql_query)
            
            result = cursor.fetchone()
            
            most_tickets_costs_org_per_year[year] = {
                "orgao_pagador": result[0],
                "total_valor_passagens": result[1]
            }

        conn.close()
        return most_tickets_costs_org_per_year
    
    def GetExpensesPerOrg(self):
        most_expenses_per_org_per_year = {}
        conn = sqlite3.connect(f'{self.initial_path}db/data.db')
        cursor = conn.cursor()
        for year in self.years:
            viagem_table = f"viagem_{year}"
            pagamento_table = f"pagamento_{year}"
            id_column = "Identificador do processo de viagem"
            valor_passagens_column = "Valor passagens"
            orgao_pagador_column = "Nome do órgao pagador"

            sql_query = f"""
            SELECT {pagamento_table}."{orgao_pagador_column}", SUM({viagem_table}."{valor_passagens_column}"+ {viagem_table}."Valor Diárias" + {viagem_table}."Valor outros gastos") AS total_valor_passagens
            FROM {viagem_table}
            INNER JOIN {pagamento_table} ON {viagem_table}."{id_column}" = {pagamento_table}."{id_column}"
            WHERE {pagamento_table}."{orgao_pagador_column}" != 'Sigiloso'
            GROUP BY {pagamento_table}."{orgao_pagador_column}"
            ORDER BY total_valor_passagens DESC
            LIMIT 10;
            """
            cursor.execute(sql_query)
            
            result = cursor.fetchall()
            
            most_expenses_per_org_per_year[year] = result

        conn.close()
        return most_expenses_per_org_per_year   
        
    def GetMostExpensiveTripsPerMonth(self):
        most_expenses_per_month = {}
        conn = sqlite3.connect(f'{self.initial_path}db/data.db')
        cursor = conn.cursor()
        for year in self.years:
            sql_query = f"""
            SELECT
                SUBSTR("Período - Data de início", 4, 2) AS month_year,
                SUM("Valor Diárias" + "Valor passagens" + "Valor outros gastos") AS total_sum
            FROM
                viagem_{year}
            GROUP BY
                month_year
            ORDER BY
                total_sum DESC
            """
            cursor.execute(sql_query)
            
            result = cursor.fetchall()
            
            most_expenses_per_month[year] = result

        conn.close()
        return most_expenses_per_month 
    
    def GetMostStayCities(self):
        most_stay_cities_per_year = {}
        conn = sqlite3.connect(f'{self.initial_path}db/data.db')
        cursor = conn.cursor()
        for year in self.years:
            sql_query = f"""
            SELECT DISTINCT "Destino - cidade", SUBSTR("Origem - Data", 4, 2) AS month, SUM("Número Diárias") AS DIARIAS
            FROM trecho_{year}
            GROUP BY month
            ORDER BY DIARIAS DESC
            LIMIT 12
            """
            cursor.execute(sql_query)
            
            result = cursor.fetchall()
            
            most_stay_cities_per_year[year] = result

        conn.close()
        return most_stay_cities_per_year
    
    def GetMostExpensiveTripsPerMonth(self):
        most_expenses_per_month = {}
        conn = sqlite3.connect(f'{self.initial_path}db/data.db')
        cursor = conn.cursor()
        for year in self.years:
            sql_query = f"""
            SELECT
                SUBSTR("Período - Data de início", 4, 2) AS month_year,
                SUM("Valor Diárias" + "Valor passagens" + "Valor outros gastos") AS total_sum
            FROM
                viagem_{year}
            GROUP BY
                month_year
            ORDER BY
                total_sum DESC
            """
            cursor.execute(sql_query)
            
            result = cursor.fetchall()
            
            most_expenses_per_month[year] = result

        conn.close()
        return most_expenses_per_month 
    
    def GetMostExpensivePersonAndOrg(self):
        most_expenses_per_person_and_org = {}
        conn = sqlite3.connect(f'{self.initial_path}db/data.db')
        cursor = conn.cursor()
        for year in self.years:
            sql_query = f"""
            SELECT
                v."Nome",
                p."Nome da unidade gestora pagadora",
                (v."Valor Diárias" + v."Valor passagens" + v."Valor outros gastos") AS total_cost
            FROM
                viagem_{year} v
            JOIN
                pagamento_{year} p ON v."Identificador do processo de viagem" = p."Identificador do processo de viagem"
            WHERE
                p."Nome da unidade gestora pagadora" <> 'Sigilosa'
            ORDER BY
                total_cost DESC
            LIMIT 1;
            """
            cursor.execute(sql_query)
            
            result = cursor.fetchall()
            
            most_expenses_per_person_and_org[year] = result

        conn.close()
        
        json_data = json.dumps(most_expenses_per_person_and_org)
        with open(f'{self.initial_path}json/most_expenses_per_person_and_org.json', 'w') as f:
            f.write(json_data)
            
    def check_data(self):
        data = {}
        try:
            conn = sqlite3.connect(f'{self.initial_path}db/data.db')
            cursor = conn.cursor()
            for year in self.years:
                sql_query = f"""
                SELECT
                    *
                FROM
                    viagem_{year}
                LIMIT 1;
                """
                cursor.execute(sql_query)
                
                result = cursor.fetchone()
                data[year] = result

            conn.close()
            if result:
                return True
            else:
                self.InsertCsvAll()
                return False
        except:
            self.InsertCsvAll()
            return False