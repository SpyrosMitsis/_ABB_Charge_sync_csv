import PySimpleGUI as sg
import pandas as pd

price = 0.25

sg.theme('Dark Grey 4')

layout = [[ sg.Text('Enter price per kW*h: '), sg.Input(size=(12,1))],
          [sg.Text('Output file name: '), sg.Input(size=(20,1))],
          [sg.Input(), sg.FileBrowse()],
          [sg.OK(), sg.Cancel()]]

window = sg.Window('Get filename example', layout)


event, values = window.read()
price = float(values[0])
output_file_name = values[1]
file_path = values[2]

#print(price, file_path)
df = pd.read_csv(file_path)
df['Total Charge(€)'] = df['Energy Delivered(kW·h)'] * price
df_sum = df.groupby(['Charger Alias'] ).sum()

df_names = df['NAMES'].drop_duplicates()
df_sn = df['SN'].drop_duplicates()
df_charger  = df['Charger Alias'].drop_duplicates()

horizontal_concat = pd.concat([df_names, df_sn, df_charger], axis=1)

final_concat = pd.merge(df_sum,horizontal_concat, on='Charger Alias', how='outer')
final_df = final_concat.reindex(columns= ['NAMES', 'SN', 'Charger Alias', 'Energy Delivered(kW·h)', 'Total Charge(€)'])

print(final_df)

final_df.to_csv( output_file_name + '.csv', index=False )

print(df_sum)

window.close()