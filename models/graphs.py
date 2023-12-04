import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class Graphs():
    years = ["2018", "2019", "2020", "2021", "2022", "2023"]
    months = {"01": "Janeiro", "02": "Fevereiro", "03": "Março", "04": "Abril", "05": "Maio", "06": "Junho", "07": "Julho", "08": "Agosto", "09": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro"}
    initial_path = "./static/"
    
    def __init__(self, data):
        self.data = data    
                
    def MostVisitedCitiesGraph(self):
        for year, cities in self.data.items():
            cities_list = list(cities.keys())
            visit_counts = list(cities.values())

            fig = px.bar(x=cities_list, y=visit_counts, labels={'x':'Cidades', 'y':'Visitas Feitas'},
                         title=f"Cidades mais visitadas em {year}")

            fig.write_html(f"./templates/most_visited_cities_{year}.html")
            
                    
    def ExpensesInTicketsGraph(self):
        df = pd.DataFrame(self.data)
        data_dict = self.data

        data_list = [{"Year": year, "Órgao Pagador": entry["orgao_pagador"], "Total Valor Passagens": entry["total_valor_passagens"]} for year, entry in data_dict.items()]

        df = pd.DataFrame(data_list)

        fig = px.bar(df, x="Year", y="Total Valor Passagens", color="Órgao Pagador",
             labels={"Total Valor Passagens": "Custo total das passagens", "Year": "Ano", "Órgao Pagador": "Órgão Pagador"})
        fig.write_html(f"./templates/MostCostsInTicketsOrg.html")
        
    def MostExpensesPerOrgGraph(self):
        for year, data in self.data.items():
            data_list = [{"orgao": entry[0], "total_valor_passagens": entry[1]} for entry in data]
            df = pd.DataFrame(data_list)

            fig = px.bar(df, x='total_valor_passagens', y='Órgao', orientation='h', title=f'Top 10 organizações com maior custo - {year}')
            fig.update_layout(xaxis_title='Total Valor Passagens', yaxis_title='Órgão Pagador')
            fig.write_html(f"./templates/MostCostsPerOrg_{year}.html")
            
    def MostExpensiveTripsPerMonthGraph(self):
        
        
        for year, data in self.data.items():
            data_list = [{"Mês": self.months[str(entry[0])], "Custo total": entry[1]} for entry in data]
            df = pd.DataFrame(data_list)

            fig = px.bar(df, x='Mês', y='Custo total', orientation='v', title=f'Custos de cada mês - {year}')
            fig.update_layout(xaxis_title='Mês', yaxis_title='Custo total')
            fig.write_html(f"./templates/MostExpensiveTripsPerMonth_{year}.html")
            
    def MostStayCitiesGraph(self):
        for year, data in self.data.items():
            data_list = [{"Cidade": entry[0], "Mês": self.months[str(entry[1])], "Diárias": int(entry[2])} for entry in data]
            df = pd.DataFrame(data_list)

            fig = px.bar(df, x='Mês', y='Diárias', orientation='v', title=f'Cidades com maior número de diárias - {year}', color='Cidade')
            fig.update_layout(xaxis_title='Mês', yaxis_title='Diárias')
            fig.write_html(f"./templates/MostStayCities_{year}.html")