import pandas as pd
import matplotlib.pyplot as plt

DEK = pd.read_excel('11_ДЭК_70_ээ_план_пок.xls')
DEK.columns = DEK.loc[0] # присваиваем столбцам имена из строки 0
DEK = DEK.drop([0,1,2]) # удаляем ненужные строки
DEK.columns # названия столбцов для дальнейшего использования в названиях

for column in DEK.columns:
    try:
        DEK[column] = DEK[column].astype(float)
    except:
        continue
        
Sfakt = DEK['Плановая стоимость потребления (с учетом средневзвешивания)'].sum()
Splan = DEK['Стоимость покупки\nэ/э в ГТП для средневзвешивания'].sum()
Snas = DEK['Стоимость покупки э/э\nдля населения в ГТПП\nдля средневзвешивания'].sum()
if (Splan-Snas) != 0 :
    Ksrvzv = (Sfakt - Snas)/(Splan-Snas)
else:
    Ksrvzv = 0
Tdgk = DEK['Средневзвешенный тариф ТЭС'].mean()*1000
Tsb = Tdgk*Ksrvzv
print('DEK', '\n Ksrvzv = ', round(Ksrvzv, 5), '\n Tdgk = ', round(Tdgk, 5), '\n Tsb = ', round(Tsb, 1))


for GTP in DEK['Код ГТП'].unique():
    GTP_pd = DEK[DEK['Код ГТП'] == GTP]
    Sfakt = GTP_pd['Плановая стоимость потребления (с учетом средневзвешивания)'].sum()
    Splan = GTP_pd['Стоимость покупки\nэ/э в ГТП для средневзвешивания'].sum()
    Snas = GTP_pd['Стоимость покупки э/э\nдля населения в ГТПП\nдля средневзвешивания'].sum()
    if (Splan-Snas) != 0 :
        Ksrvzv = (Sfakt - Snas)/(Splan-Snas)
    else:
        Ksrvzv = 0
    print(GTP, round(Ksrvzv, 3) )