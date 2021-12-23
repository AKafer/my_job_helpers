import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time
from datetime import datetime, date
import os
import os.path
import zipfile
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import win32com.client
import shutil
import numpy
import pandas as pd

global SVOD_dev
SVOD_dev = []

def download(DZO, URL, FLAG1, name, codname, data, Nlink, driver, wait) : # функция скачивания по шаблону
        if FLAG1:    
            for i in range(1) :  
                try: # попытка скачивания
                    driver.get(URL)
                    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT,  name))).click()
                    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Сибирь"))).click()
                    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "."+data))).click()
                    element = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT,codname)))
                    items = driver.find_elements_by_partial_link_text(codname)
                    if len(items) > Nlink : print('По ' + DZO + ": "+ name + "продублирован")
                    for item in items :
                        item.click()
                except :
                    print('Не скачано:' + name + ' ' + DZO) 
                    continue
                
def LOAD(mesSTR, driver, wait): # основная функция скачивания
    mes = mesSTR
    year = godN.get()
    data = mes + '.' + year
    k = -1
    flagNBS = 1
    flagKEF = 0
    flagFSK = 0
    # делаем стандартную строку запроса на страницу АТС после ввода пароля - в пробелы вставляем логины и пароли
    with open('0_коды_АТС.txt', 'r') as filecod: # файл с кодами лежит в папке с программой
        for line in filecod: # построчно считываем файл в список d
              k += 1
              d = line.split() # список по текущей строке
              if cod[k].get() == 0 : continue
              if ot_FSK.get() and flagFSK == 0 :
                    flagFSK = 100  
                    for i in range(1) :
                        try: # скачиваем ставку ФСК
                            driver.get('https://www.atsenergo.ru/nreport?rname=FRSTF_ATS_REPORT_PUBLIC_FSK&rdate=' + year + mes + '01')
                            wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Европа"))).click()
                            element = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'FSK.xls')))
                            items = driver.find_elements_by_partial_link_text('FSK.xls')
                            if len(items) > 1 : print('Ставка тарифа ФСК продублирована')
                            for item in items :
                                item.click()
                        except :
                            print('Не скачано: ставка ФСК')
                            continue  
              KeyZap = 'https://www.atsenergo.ru/nauth/nreports?access=personal&partcode={}&username={}&password={}'.format(d[1],d[2],d[3]) 
              download(d[0], KeyZap, ot_51.get(), "51. Ежемесячный отчет", "consumer_power_buy_sell.", data, 1, driver, wait)  
              download(d[0], KeyZap, ot_56.get(), "56. Ежемесячный отчет", "consumer_power_buy_sell_maxh.", data, 1, driver, wait)
              download(d[0], KeyZap, ot_68.get(),  "68. Аналитический отчет", "fact_buy_sell_power_analytic.", data, 1, driver, wait)
              download(d[0], KeyZap, ot_69.get(),  "69. Аналитический отчет", "plan_hour_generation_energy_price.", data, 1, driver, wait)
              download(d[0], KeyZap, ot_70.get(),  "70. Аналитический отчет", "plan_hour_consumption_energy_price.", data, 1, driver, wait)
              download(d[0], KeyZap, ot_74.get(),  "74. Аналитический отчет", "analytic.xls", data, 1, driver, wait)
              download(d[0], KeyZap, ot_OTKL.get(),  "Итоговый почасовой отчет по определению обязательств/требований по оплате отклонений участника", "UPZ_DEV_COST.xls", data, 1, driver, wait)
              download(d[0], KeyZap, ot_DD.get(),  "Почасовой отчет о результатах расчета объемов электрической энергии по двухсторонним договорам в НЦЗ", "dd_post.xls", data, 1, driver, wait)
              download(d[0], KeyZap, ot_CFR.get(),  "ЦФР.027.Счет содержит фактические данные по неценовым зонам на месяц, включая стоимость", "FACT_NCZCFR", data, 2, driver, wait)
              download(d[0], KeyZap, ot_POK.get(),  "Расширенный отчет по ЭЭ комиссионера", "ENZ-V-KM-17", data, 1, driver, wait)  

              if  flagNBS == 0 :
                  flagNBS = 100    
                  download(d[0], KeyZap, ot_NBS.get(),  "Отчёт о почасовой разнице суммарных предварительных обязательств и суммарных предварительных требований по оплате отклонений в НЦЗ", "nebal.xls", data, 1, driver, wait)
             
              if ot_GTP.get() :   
                  for i in range(1) :
                      try: # скачиваем отчеты по ГТП
                                driver.get(KeyZap)  
                                driver.get('https://www.atsenergo.ru/nreport?rname=part_dev_ascue&rdate=' + year + mes + '01')
                                element = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT,"ascue.xls")))
                                items = driver.find_elements_by_partial_link_text("ascue.xls")
                                for item in items :
                                      item.click()
                      except :
                           print("Не скачано: отчеты по ГТП " + d[0])
                           continue
              if ot_KEF.get() and flagKEF == 0: 
                    flagKEF = 100
                    for i in range(1) :    
                        try: # скачиваем коэффициенты по инициативам
                            driver.get(KeyZap)
                            driver.get('https://www.atsenergo.ru/nreport?rname=NCZ_COEF_REPORT&rdate=' + year + mes + '01')
                            element = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT,"ZONE4")))
                            items = driver.find_elements_by_partial_link_text("ZONE4")
                            if len(items) > 1 : print("Коэффициенты по инициативам продублированы")
                            for item in items :
                                  item.click()
                        except :
                            print("Не скачано: Коэффициенты по инициативам")
                            continue
    time.sleep(100) # задержка для скачивания последнего файла

def DEVIATION(DZO, Kvplus, Kvpminus, Ksplus_g, Ksminus_g, Ksplus_p, Ksminus_p): #функция обработки файлов отклонений
    adress = os.getcwd()
    os.chdir(adress + '\\' +'ЗАГРУЗКА')
    L = os.listdir(".")
    DZO_file = 'пусто'
    for file in L : # Ищем файлы с отклонениями
        if '{}_Свод_откл.xls'.format(DZO) in file:
                DZO_file = file
                break
                
    DZO_pd = pd.read_excel(DZO_file)
          
    DZO_pd.columns = DZO_pd.loc[1] # присваиваем столбцам имена из строки 0
    DZO_pd = DZO_pd.drop([0,1,2,3]) # удаляем ненужные строки
    for column in DZO_pd.columns:# переводим данные в тим флоат
        try:
            DZO_pd[column] = DZO_pd[column].astype(float)
        except:
            continue
    
    L = []

    for GTP in DZO_pd['ГТП'].unique():
        post_plan = DZO_pd[DZO_pd['ГТП'] == GTP]['План/Плановый объем потерь\n'].sum()
        post_fact = DZO_pd[DZO_pd['ГТП'] == GTP]['Фактический объем\n (учетный показатель) '].sum()
        ivplus_o = DZO_pd[DZO_pd['ГТП'] == GTP]['ИВ+\n\nОбъем'].sum()
        ivminus_o = DZO_pd[DZO_pd['ГТП'] == GTP]['ИВ-\n\nОбъем'].sum()
        isplus_o = DZO_pd[DZO_pd['ГТП'] == GTP]['ИС+\n\nОбъем'].sum()
        isminus_o = DZO_pd[DZO_pd['ГТП'] == GTP]['ИС-\n\nОбъем'].sum()
        ivplus_s = DZO_pd[DZO_pd['ГТП'] == GTP]['ИВ+\n\nСтоимость'].sum()
        ivminus_s = DZO_pd[DZO_pd['ГТП'] == GTP]['ИВ-\n\nСтоимость'].sum()
        isplus_s = DZO_pd[DZO_pd['ГТП'] == GTP]['ИС+\n\nСтоимость'].sum()
        isminus_s = DZO_pd[DZO_pd['ГТП'] == GTP]['ИС-\n\nСтоимость'].sum()
        tip_GTP = 'не определен'
        if GTP[0:1] == 'G':
            tip_GTP = 'генерация'
        if GTP[0:1] == 'P':
            tip_GTP = 'потребление'
        L.append([GTP, tip_GTP, post_plan, post_fact, ivplus_o, ivminus_o, isplus_o, isminus_o, ivplus_s, ivminus_s, isplus_s, isminus_s])    

    DZO_otkl = pd.DataFrame(L)
    DZO_otkl.columns = ['ГТП', 'Тип ГТП','План', 'Факт', 'Объем ИВ+', 'Объем ИВ-', 'Объем ИС+', 'Объем ИС-', 'Стоим ИВ+', 'Стоим ИВ-', 'Стоим ИС+', 'Стоим ИС-']
    DZO_otkl['План'][DZO_otkl['Тип ГТП'] == 'потребление'] = DZO_otkl[DZO_otkl['Тип ГТП'] == 'потребление']['План']*-1
    DZO_otkl['Факт'][DZO_otkl['Тип ГТП'] == 'потребление'] = DZO_otkl[DZO_otkl['Тип ГТП'] == 'потребление']['Факт']*-1
    DZO_otkl['Ef_iv_plus'] = round(DZO_otkl['Стоим ИВ+']*(Kvplus-1)/Kvplus,2)
    DZO_otkl['Ef_iv_minus'] = round(DZO_otkl['Стоим ИВ-']*(1-Kvpminus)/Kvpminus,2)
    DZO_otkl['Ef_is_plus'] = 0
    DZO_otkl['Ef_is_plus'][DZO_otkl['Тип ГТП'] == 'генерация'] = round(DZO_otkl[DZO_otkl['Тип ГТП'] == 'генерация']['Стоим ИС+']*(1-Ksplus_g)/Ksplus_g,2)
    DZO_otkl['Ef_is_plus'][DZO_otkl['Тип ГТП'] == 'потребление'] = round(DZO_otkl['Стоим ИС+'][DZO_otkl['Тип ГТП'] == 'потребление']*(Ksplus_p-1)/Ksplus_p,2)
    DZO_otkl['Ef_is_minus'] = 0
    DZO_otkl['Ef_is_minus'][DZO_otkl['Тип ГТП'] == 'генерация'] = round(DZO_otkl['Стоим ИС-'][DZO_otkl['Тип ГТП'] == 'генерация']*(Ksminus_g-1)/Ksminus_g,2)
    DZO_otkl['Ef_is_minus'][DZO_otkl['Тип ГТП'] == 'потребление'] = round(DZO_otkl['Стоим ИС-'][DZO_otkl['Тип ГТП'] == 'потребление']*(1-Ksminus_p)/Ksminus_p,2)
    DZO_otkl.to_excel("Свод_откл_{}.xlsx".format(DZO))
    global SVOD_dev
    SVOD_dev.append([DZO, DZO_otkl['План'].sum(), DZO_otkl['Факт'].sum(), DZO_otkl['Объем ИВ+'].sum(), DZO_otkl['Объем ИВ-'].sum(), DZO_otkl['Объем ИС+'].sum(), DZO_otkl['Объем ИС-'].sum(), DZO_otkl['Стоим ИВ+'].sum(), DZO_otkl['Стоим ИВ-'].sum(), DZO_otkl['Стоим ИС+'].sum(), DZO_otkl['Стоим ИС-'].sum(),  DZO_otkl['Ef_iv_plus'].sum(), DZO_otkl['Ef_iv_minus'].sum(), DZO_otkl['Ef_is_plus'].sum(), DZO_otkl['Ef_is_minus'].sum()])
    os.chdir(adress)
    return SVOD_dev
    
def click_button1(): # по нажатию кнопки функция запускает процесс скачивания выбранных файлов
      adress = os.getcwd()
      print(adress)  
      if os.path.exists(adress + '\\' +'ЗАГРУЗКА'):
          os.chdir(adress + '\\' +'ЗАГРУЗКА')
          L = os.listdir(".") # цикл очистки папки загруки
          for x in L :
             os.remove(x)
      else:
          os.mkdir('ЗАГРУЗКА')
      
      os.chdir(adress)
     
      chrome_options = webdriver.ChromeOptions()
      chrome_options.headless = True 
      prefs = {'download.default_directory' : adress + '\\' +'ЗАГРУЗКА'}
      chrome_options.add_experimental_option('prefs', prefs)
      driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options) 
          
      wait = WebDriverWait(driver, 10) # установка ожидания

      for i in range(int(mesN.get()), int(mesN2.get())+1) :
              if len(str(i)) == 1 : LOAD('0'+str(i), driver, wait)
              else : LOAD(str(i), driver, wait)
      driver.quit() # закрываем драйвер
      os.chdir(adress) # возврат в каталог программы
      messagebox.showinfo("Инфо", 'Скачиание завершено')  
       
def click_button2(): # по нажатию кнопки актививируется процесс переименования файла
      adress = os.getcwd()  
      os.chdir(adress + '\\' +'ЗАГРУЗКА')
      L = os.listdir(".")
      for x in L : # распаковка архивов
          if '.zip' in x :
              y = zipfile.ZipFile(x)
              y.extractall('.')
              y.close()
      time.sleep(2) #задержка для распаковки
      L = os.listdir(".")
      
      for x in L : # цикл перименования файлов
        for O_name in Name_pd['Origin_name']: 
            if O_name in x:
                flag = 0
                try:
                    for GTP in ATS_pd['GTP1']:
                        if GTP != None:
                            if GTP.upper() in x :
                                os.rename(x, x[4:6] + '_' + ATS_pd[ATS_pd['GTP1'] == GTP]['Name'].iloc[0] + Name_pd[Name_pd['Origin_name'] == O_name]['New_name'].iloc[0]+'.xls')
                                flag = 1
                                break
                    if flag == 0:
                        os.rename(x, x[4:6] + Name_pd[Name_pd['Origin_name'] == O_name]['New_name'].iloc[0]+'.xls')
                    break
                except:
                    for GTP in ATS_pd['GTP1']:
                        if GTP != None:
                            if GTP.upper() in x :
                                os.rename(x, x[4:6] + '_' + ATS_pd[ATS_pd['GTP1'] == GTP]['Name'].iloc[0] + Name_pd[Name_pd['Origin_name'] == O_name]['New_name'].iloc[0]+'2.xls')
                                flag = 1
                                break
                    if flag == 0:
                        os.rename(x, x[4:6] + Name_pd[Name_pd['Origin_name'] == O_name]['New_name'].iloc[0]+'2.xls')
                    break
    
      os.chdir(adress) # возращаем исходную начальную папку 
      messagebox.showinfo("Инфо", 'Переименование завершено')
       
def click_button3(): # по нажанию кнопки функция проставляет или снимает все флажки во второй рамке
    M = ot_FSK.get() + ot_51.get()+ ot_56.get()+ ot_68.get()+ ot_69.get()+ ot_70.get()+ ot_74.get()+ ot_DD.get() + ot_GTP.get()+ ot_CFR.get() + ot_POK.get()+ ot_KEF.get()
    if M > 11/2 :
        ot_FSK.set(0)
        ot_51.set(0)
        ot_56.set(0)
        ot_68.set(0)
        ot_69.set(0)
        ot_70.set(0)
        ot_74.set(0)
        ot_DD.set(0)
        ot_OTKL.set(0)
        ot_GTP.set(0)
        ot_CFR.set(0)
        ot_POK.set(0)
        ot_KEF.set(0)
    else :
        ot_FSK.set(1)
        ot_51.set(1)
        ot_56.set(1)
        ot_68.set(1)
        ot_69.set(1)
        ot_70.set(1)
        ot_74.set(1)
        ot_DD.set(1)
        ot_OTKL.set(1)
        ot_GTP.set(1)
        ot_CFR.set(1)
        ot_POK.set(1)
        ot_KEF.set(1)
        
def click_button4(): # по нажатию кнопки запускается процесс обработки файлов отклонений выбранный компаний
        # из файла "m_Коэффициенты_отчет" выбираем коэффициенты по собственным и внешним инициативам
        adress = os.getcwd()  
        os.chdir(adress + '\\' +'ЗАГРУЗКА')
        L = os.listdir(".")
        koef_file = 'пусто'
        for file in L : # Ищем файл с коэффициентами
            if 'Коэффициенты_отчет' in file:
                koef_file = file
                break
      
        Excel = win32com.client.Dispatch("Excel.Application")
        
        if koef_file != 'пусто':
            wb = Excel.Workbooks.Open(adress + '\\' +'ЗАГРУЗКА' +'\\'+ koef_file)
            Kvplus = wb.Sheets(1).Cells(13,1).value
            Kvpminus = wb.Sheets(1).Cells(13,2).value
            Ksplus_p = wb.Sheets(1).Cells(8,3).value
            Ksminus_p = wb.Sheets(1).Cells(8,4).value
            Ksplus_g = wb.Sheets(1).Cells(8,1).value
            Ksminus_g = wb.Sheets(1).Cells(8,2).value
            wb.Save()
            wb.Close()
            Excel.Quit()
        else:
            messagebox.showinfo("Ошибка", 'Файл m_Коэффициенты_отчет не найден')
        
        os.chdir(adress)
        
        # заполняемс словарь с названиями ДЗО и галочками
        k = -1
        Ksh={}
        with open('0_коды_АТС.txt', 'r') as filecod: # файл с кодами лежит в папке с программой
                for line in filecod: # построчно считываем файл в список d
                      k += 1
                      d = line.split()[0] # список по текущей строке
                      Ksh[d] = cod[k].get() # смотрим где стоят галки
        
        # обрабатываем словарь и запускаем функцию обработки файлов с отклонениями DEVIATION
        for key, value in Ksh.items():
            if value == 1:
                progress_label.config(text = 'Обработка файла:\n' + key)
                root.update()   
                DEVIATION(key, Kvplus, Kvpminus, Ksplus_g, Ksminus_g, Ksplus_p, Ksminus_p)
        
        # делаем итоговый датасет с отклонениями. SVOD_dev - глобальная переменная.
        SVOD_pd = pd.DataFrame(SVOD_dev)
        SVOD_pd.columns = ['ДЗО', 'План', 'Факт', 'Объем ИВ+', 'Объем ИВ-', 'Объем ИС+', 'Объем ИС-', 'Стоим ИВ+', 'Стоим ИВ-', 'Стоим ИС+', 'Стоим ИС-', 'Ef_iv_plus', 'Ef_iv_minus', 'Ef_is_plus','Ef_is_minus']
        adress = os.getcwd()
        os.chdir(adress + '\\' +'ЗАГРУЗКА')
        SVOD_pd.to_excel('Итог_свод_откл.xls')
        os.chdir(adress)
        messagebox.showinfo("Шаблон", 'Шаблон готов')
        progress_label.config(text = '')
        root.update()
        
def click_button5():
        messagebox.showinfo("Бля", 'Вот ты пидарас...')

def click_checkbutton(): # функция проверяет сколько переключков включено и принудительно сохраняет включенным последний который  мы хотим отключить
    NULL = 0
    for i in range(N) :
        if PAM[i] != cod[i].get() : ind = i
        if cod [i].get() == 0 : NULL += 1
    if NULL > N - 1 : cod[ind].set(1) 
    else :
        for i in range(N):
           PAM[i] = int(cod[i].get())
  
    
# задаем параметры пользовательской формы
root = Tk()
root.title("Скачивание отчетов с сайта АТС")
root.geometry("400x550")
root.resizable(False, False)

# выбор компаний для скачивания (Рамка 1)
frame1 = LabelFrame(root, text = 'Компашки')

i = -1
cod = []
L1 = []
with open('0_коды_АТС.txt', 'r') as filecod: # файл с кодами лежит в папке с программой
        for line in filecod: # построчно считываем файл в список d
              i += 1
              d = line.split()
              L1.append(d)  
              cod.append(IntVar())
              cod[i].set(1)
              cod_btn = Checkbutton(frame1, text=d[0], variable = cod[i], command = click_checkbutton)
              cod_btn.pack(anchor=W)

ATS_pd = pd.DataFrame(L1)
ATS_pd.columns = ['Name', 'GTP1', 'GTP2', 'Password']

L2 = []
with open('0_Имена_фалов.txt', 'r') as filecod: # файл с кодами лежит в папке с программой
        for line in filecod: # построчно считываем файл в список d
              line1 = line.split()
              L2.append(line1)  

Name_pd = pd.DataFrame(L2)
Name_pd.columns = ['Origin_name', 'New_name']
                   
            
frame1.place(relx = 0.01, rely = 0, relheight = 0.7, relwidth = 0.35 )
N = i+1
PAM = [] # список значений переключателей компаний до изменения значения какого-либо переключателя ("память до")
for i in range(N) : PAM.append(cod[i].get())

# выбор отчетов для скачивания (Рамка 2)
frame2 = LabelFrame(root, text = 'Отчеты')
ot_FSK = IntVar()
ot_FSK.set(1)
ot_FSK_checkbutton = Checkbutton(frame2, text="Ставка ФСК в Амурской области", variable = ot_FSK)
ot_51 = IntVar()
ot_51.set(1)
ot_51_checkbutton = Checkbutton(frame2,  text="Отчет 51 (покупка мощности)", variable = ot_51)
ot_56 = IntVar()
ot_56.set(1)
ot_56_checkbutton = Checkbutton(frame2,  text="Отчет 56 (Пиковые часы)", variable = ot_56)
ot_68 = IntVar()
ot_68.set(1)
ot_68_checkbutton = Checkbutton(frame2,  text="Отчет 68 (Стоимость мощности)", variable = ot_68)
ot_69 = IntVar()
ot_69.set(1)
ot_69_checkbutton = Checkbutton(frame2,  text="Отчет 69 (Стоимость ПДГ)", variable = ot_69)
ot_70 = IntVar()
ot_70.set(1)
ot_70_checkbutton = Checkbutton(frame2,  text="Отчет 70 (Стоимость ППП)", variable = ot_70)
ot_74 = IntVar()
ot_74.set(1)
ot_74_checkbutton = Checkbutton(frame2,  text="Отчет 74 (Фактическая стоимость ЭЭ)", variable = ot_74)
ot_DD = IntVar()
ot_DD.set(1)
ot_DD_checkbutton = Checkbutton(frame2,  text="Отчет ДД", variable = ot_DD)
ot_OTKL = IntVar()
ot_OTKL.set(1)
ot_OTKL_checkbutton = Checkbutton(frame2,  text="Свод отклонений", variable = ot_OTKL)
ot_GTP = IntVar()
ot_GTP.set(1)
ot_GTP_checkbutton = Checkbutton(frame2,  text="Объемы по ГТП", variable = ot_GTP)
ot_CFR = IntVar()
ot_CFR.set(1)
ot_CFR_checkbutton = Checkbutton(frame2,  text="Фактические счета ЦФР", variable = ot_CFR)
ot_POK = IntVar()
ot_POK.set(1) # полный отчет комиссионера
ot_POK_checkbutton = Checkbutton(frame2,  text="Отчет комиссионера", variable = ot_POK)
ot_KEF = IntVar()
ot_KEF.set(1)
ot_KEF_checkbutton = Checkbutton(frame2,  text="Коэффициенты по инициативам", variable = ot_KEF)
frame2.place(relx = 0.35, rely = 0, relheight = 0.7, relwidth = 1-0.35)
ot_FSK_checkbutton.pack(anchor=W)
ot_51_checkbutton.pack(anchor=W)
ot_56_checkbutton.pack(anchor=W)
ot_68_checkbutton.pack(anchor=W)
ot_69_checkbutton.pack(anchor=W)
ot_70_checkbutton.pack(anchor=W)
ot_74_checkbutton.pack(anchor=W)
ot_DD_checkbutton.pack(anchor=W)
ot_OTKL_checkbutton.pack(anchor=W)
ot_GTP_checkbutton.pack(anchor=W)
ot_CFR_checkbutton.pack(anchor=W)
ot_POK_checkbutton.pack(anchor=W)
ot_KEF_checkbutton.pack(anchor=W)

# метки месяца и года
mes_label = Label(text = 'Месяцы')
mes_label.place(relx = 0.35, rely = 0.71)
god_label = Label(text = 'Год')
god_label.place(relx = 0.63, rely = 0.71)
s_label = Label(text = 'c')
s_label.place(relx = 0.26, rely = 0.75)
po_label = Label(text = 'по')
po_label.place(relx = 0.40, rely = 0.75)
  
#выпадающие списки месяца и года
def TextBoxUpdate1(event) :
        if int(mesN2.get()) < int(mesN.get()) : mesN2.set(mesN.get())
def TextBoxUpdate2(event) :
        if int(mesN2.get()) < int(mesN.get()) : mesN2.set(mesN.get())
        
godnow = datetime.now() # текущая дата
mesN = ttk.Combobox(root,values = ["01","02","03","04","05","06","07","08","09","10","11","12"],height=12)
mesN.set(str(godnow.month-1) if len(str(godnow.month))== 2 else '0'+ str(godnow.month-1)) # по умолчанию назнаем прошлый месяц
mesN.place(relx = 0.29, rely = 0.75, relwidth = 0.1)
mesN.bind("<<ComboboxSelected>>", TextBoxUpdate1)
mesN2 = ttk.Combobox(root,values = ["01","02","03","04","05","06","07","08","09","10","11","12"],height=12)
mesN2.set(mesN.get()) # по умолчанию назнаем прошлый месяц
mesN2.place(relx = 0.46, rely = 0.75, relwidth = 0.1)
mesN2.bind("<<ComboboxSelected>>", TextBoxUpdate2)
godN = ttk.Combobox(root,values = [str(godnow.year-4), str(godnow.year-3),str(godnow.year-2),str(godnow.year-1),str(godnow.year-0)],height=5)
godN.set(godnow.year) # по умолчанию назначаем текущий год
godN.place(relx = 0.6, rely = 0.75, relwidth = 0.15)

btn1 = Button(text= 'Скачать \nвыбранные отчеты', command=click_button1)
btn1.place(relx=0.13, rely=0.82, relheight = 0.07 , relwidth = 0.32)
btn2 = Button(text = 'Переименовать \nфайлы', command=click_button2)
btn2.place(relx=0.13, rely=0.91, relheight = 0.07, relwidth = 0.32)
btn3 = Button(frame2, text = 'Все снять/поставить', command=click_button3)
btn3.pack(anchor=W)
btn4 = Button(text= 'Шаблоны', command=click_button4)
btn4.place(relx=0.55, rely=0.82, relheight = 0.07, relwidth = 0.32)
btn5 = Button(text = 'Не нажимай!', command=click_button5)
btn5.place(relx=0.55, rely=0.91, relheight = 0.07, relwidth = 0.32)
progress_label = Label(frame1, text = '', justify=LEFT, fg = 'BLUE', wraplength = 120)
progress_label.pack(anchor=W)

root.mainloop()