import warnings

import openpyxl
import pandas as pd
from tqdm import tqdm


class ExtractorXl:
    def __init__(self):
        """
        Initialize the XlDataExtractor.
        """
        self.combined_df = pd.DataFrame()
        warnings.filterwarnings(
            "ignore", category=UserWarning, module="openpyxl")

    def process_data(self, file_path):
        """
        Process data from an Excel file.

        Args:
            file_path (str): The path to the Excel file.
        """
        workbook = openpyxl.load_workbook(file_path)

        for sheet_name in tqdm(workbook.sheetnames, desc='Processando abas'):
            df = pd.read_excel(
                file_path, sheet_name=sheet_name, skiprows=11, nrows=366)

            series = [''] * df.shape[0]
            for i in range(1, 9):
                if f'Ponto {i}' not in df:
                    df.insert(i, f'Ponto {i}', series)

            # unnamed_columns = [
            #     col for col in df.columns if col.startswith('Unnamed:')]
            # if unnamed_columns:
            #     df = df.drop(columns=unnamed_columns)
            print(file_path, sheet_name)

            df = self.remove_colunas_ponto(df)

            df.columns = [
                'data', 'ponto_1', 'ponto_2', 'ponto_3', 'ponto_4', 'ponto_5',
                'ponto_6', 'ponto_7', 'ponto_8', 'observacao', 'exclusao',
                'CH', 'HT', 'EX', 'TN', 'AnAe', 'AT', 'FA'
            ]

            df.drop('exclusao', axis=1, inplace=True)

            df.insert(1, 'dia_semana', series)
            df[['data', 'dia_semana']] = df['data'].str.split(
                ' - ', expand=True)

            aba = workbook[sheet_name]
            nome = aba['B2'].value
            cargo = aba['B3'].value
            setor = aba['B4'].value
            matricula = aba['B5'].value

            # Adicione informações como colunas ao DataFrame da aba
            df['nome'] = nome
            df['cargo'] = cargo
            df['setor'] = setor
            df['matricula'] = matricula

            # Concatene o DataFrame da aba atual ao DataFrame combinado
            self.combined_df = pd.concat(
                [self.combined_df, df], ignore_index=True)

    def save_to_csv(self, output_file):
        """
        Save the combined DataFrame to a CSV file.

        Args:
            output_file (str): The path to the output CSV file.
        """
        self.combined_df.to_csv(output_file, index=False)

    def remove_colunas_ponto(self, df):

        colunas_ponto = [
            coluna for coluna in df.columns if coluna.startswith('ponto_')
        ]

        for coluna in colunas_ponto:
            numero = int(coluna.split('_')[1])
            if numero > 8:
                df.drop(columns=coluna, inplace=True)

        return df


if __name__ == '__main__':
    pass
