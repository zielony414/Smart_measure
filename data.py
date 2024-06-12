import matplotlib.pyplot as plt
from openpyxl import Workbook, load_workbook
from openpyxl.drawing.image import Image
from openpyxl.chart import LineChart, Reference
import xlwings as xw
import os
import numpy as np


def import_data_to_sheet(ws, idx, path):
    ws.append(['I_in', 'U_in', 'I_out', 'U_out', 'P_in', 'P_out', 'n'])

    file_names = [
        f'inlet_amm{idx}.txt',
        f'inlet_volt{idx}.txt',
        f'out_amm{idx}.txt',
        f'out_volt{idx}.txt'
    ]

    for col_idx, file_name in enumerate(file_names, start=1):
        with open(path+'/' + file_name, 'r') as file:
            lines = file.readlines()
            for row_idx, line in enumerate(lines, start=2):
                data = line.split()
                if len(data) >= 2:
                    value = float(data[1])
                    ws.cell(row=row_idx, column=col_idx, value=value)


def calculate_and_create_chart(ws):
    for row in range(2, ws.max_row + 1):
        ws[f'E{row}'] = f"=A{row}*B{row}"
        ws[f'F{row}'] = f"=C{row}*D{row}"
        ws[f'G{row}'] = f"=F{row}/E{row}"

    chart = LineChart()
    chart.title = "Zależność sprawności od I_in"
    chart.x_axis.title = "I_in"
    chart.y_axis.title = "n"

    x_data = Reference(ws, min_col=1, min_row=2, max_row=ws.max_row)
    y_data = Reference(ws, min_col=7, min_row=2, max_row=ws.max_row)

    chart.add_data(y_data, titles_from_data=True)
    chart.set_categories(x_data)

    ws.add_chart(chart, "I10")


def data_analized(steps, path):
    # Tworzenie nowego pliku Excela
    wb = Workbook()

    # Listy przechowujące dane dla wykresu zbiorczego
    all_I_in = []
    all_n = []
    all_u_in_means = []

    for idx in range(steps):
        ws = wb.create_sheet(title=f"Data_Set_{idx}")
        import_data_to_sheet(ws, idx, path)
        calculate_and_create_chart(ws)

    # Usunięcie domyślnego arkusza
    wb.remove(wb['Sheet'])

    # Zapisanie pliku tymczasowego, aby xlwings mógł go otworzyć i przeliczyć formuły
    temp_filename = path + 'temp_dane_z_plikow_w_excelu_temp.xlsx'
    wb.save(temp_filename)

    # Otwieranie pliku i przeliczanie formuł za pomocą xlwings
    app = xw.App(visible=False)
    book = xw.Book(temp_filename)

    for sheet in book.sheets:
        sheet.api.Calculate()

    # Zbieranie przeliczonych danych
    for idx, sheet in enumerate(book.sheets):
        I_in = sheet.range('A2:A' + str(sheet.cells.last_cell.row)).value
        n = sheet.range('G2:G' + str(sheet.cells.last_cell.row)).value
        U_in = sheet.range('B2:B' + str(sheet.cells.last_cell.row)).value

        I_in = [i for i in I_in if i is not None]
        n = [i for i in n if i is not None]
        U_in = [u for u in U_in if u is not None]

        all_I_in.append(I_in)
        all_n.append(n)

        u_in_mean = np.mean(U_in)
        all_u_in_means.append(u_in_mean)

    # Zamknięcie i zapisanie pliku
    book.save()
    book.close()
    app.quit()

    # Tworzenie wykresu zbiorczego za pomocą matplotlib
    colors = plt.colormaps['tab10']  # Paleta kolorów

    plt.figure(figsize=(10, 6))
    for idx in range(steps):
        plt.plot(all_I_in[idx], all_n[idx], label=f'U_in ≈ {round(all_u_in_means[idx])}V', color=colors(idx / 7))

    plt.title('Zależność sprawności od I_in dla różnych zestawów danych')
    plt.xlabel('I_in')
    plt.ylabel('n')
    plt.legend()
    plt.grid(True)

    # Zapisanie wykresu jako plik PNG
    plt.savefig('combined_chart.png')
    plt.close()

    # Zaimportowanie wykresu do pliku Excela
    wb = load_workbook(temp_filename)
    combined_ws = wb.create_sheet(title="CombinedChart")
    img = Image('combined_chart.png')
    combined_ws.add_image(img, 'A1')

    # Zapisanie zmian do pliku Excela
    final_filename = path + 'dane_z_plikow_w_excelu.xlsx'
    wb.save(final_filename)

    # Usunięcie tymczasowego pliku
    os.remove(temp_filename)
