import pyodbc
import pandas as pd # type: ignore
import math as m
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

SERVER = '<server-adress>'
DATABASE = '<database-name>'

string_connection = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER=RAFAEL_SIMAS4\MSSQLSERVER01;DATABASE=DADOS;Trusted_Connection=yes;TrustServerCertificate=yes;'
connection = pyodbc.connect(string_connection)

con1 = connection.cursor()
con1.execute("""
SELECT D.PROFUNDIDADE,
	   COUNT(*) TOTAL,
	   (SELECT COUNT(*) FROM DBO.DADOS_DIAMETRO_PROFUNDIDADE) AS ACUMULADO
FROM DBO.DADOS_DIAMETRO_PROFUNDIDADE AS D
GROUP BY D.PROFUNDIDADE
             """)
query = con1.fetchall()
d1 = []
con1.close()

for i in query:
    profundidade = float(i.PROFUNDIDADE)
    total = float(i.TOTAL)
    acumulado = float(i.ACUMULADO)
    d1.append([profundidade,total,acumulado])
    
dados1 = pd.DataFrame(d1,columns=['PROFUNDIDADE','TOTAL','ACUMULADO'])

### heatmap com a concentração de informação

con2 = connection.cursor()
con2.execute("""
SELECT D.PROFUNDIDADE,
	   COUNT(*) TOTAL,
	   AVG(D.DIAMETRO) AS MEDIA,
	   (SELECT COUNT(*) FROM DBO.DADOS_DIAMETRO_PROFUNDIDADE) AS ACUMULADO
FROM DBO.DADOS_DIAMETRO_PROFUNDIDADE AS D
GROUP BY D.PROFUNDIDADE
             """)
query2 = con2.fetchall()
con2.close()
d2 = []

for i in query2:
    profundidade = float(i.PROFUNDIDADE)
    total = float(i.TOTAL)
    media = float(i.MEDIA)
    acumulado = float(i.ACUMULADO)
    d2.append([profundidade,total,media,acumulado])
    
dados2 = pd.DataFrame(d2,columns=['PROFUNDIDADE','TOTAL','MEDIA','ACUMULADO'])
pivot2 = dados2.pivot_table(index='PROFUNDIDADE',columns='TOTAL',values='MEDIA')


plt.figure(figsize=(10,8))
sns.heatmap(pivot2, cmap='viridis',annot=True,fmt='.2f')
plt.title('concentração de informação')
plt.xlabel('TOTAL')
plt.ylabel('PROFUNDIDADE')
plt.show()


con3 = connection.cursor()
con3.execute("""
SELECT D.PROFUNDIDADE,
	   COUNT(*) TOTAL,
	   AVG(D.DIAMETRO) AS MEDIA,
	   (SELECT COUNT(*) FROM DBO.DADOS_DIAMETRO_PROFUNDIDADE) AS ACUMULADO,
	   CAST(COUNT(*) AS FLOAT(2)) / CAST((SELECT COUNT(*) FROM DBO.DADOS_DIAMETRO_PROFUNDIDADE) AS FLOAT(2)) AS PERCENTUAL
FROM DBO.DADOS_DIAMETRO_PROFUNDIDADE AS D
GROUP BY D.PROFUNDIDADE
             """)
query3 = con3.fetchall()
con3.close()
d3 = []
for i in query3:
    profundidade = float(i.PROFUNDIDADE)
    total = float(i.TOTAL)
    media = float(i.MEDIA)
    acumulado = float(i.ACUMULADO)
    percentual = float(i.PERCENTUAL)
    d3.append([profundidade,total,media,acumulado,percentual])
    
dados3 = pd.DataFrame(d3,columns=['profundidade','total','media','acumulado','percentual'])
dados_pivot3 = dados3.pivot_table(columns='profundidade',index='media',values='percentual')

plt.figure(figsize=(10,8))
sns.heatmap(dados_pivot3,cmap='viridis',annot=True,fmt='.2f')
plt.title('concentração de informação')
plt.xlabel('TOTAL')
plt.ylabel('PROFUNDIDADE')
plt.show()
### percentis com a primeira profundidade