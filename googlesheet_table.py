import pygsheets
from typing import List, Union

class GoogleTable:
    def __init__(
        self, credence_service_file: str = "", googlesheet_file_url: str = ""
    ) -> None:
        self.credence_service_file = credence_service_file
        self.googlesheet_file_url = googlesheet_file_url

    def _get_googlesheet_by_url(
        self, googlesheet_client: pygsheets.client.Client
    ) -> pygsheets.Spreadsheet:
        """Get Google.Docs Table sheet by document url"""
        sheets: pygsheets.Spreadsheet = googlesheet_client.open_by_url(
            self.googlesheet_file_url
        )
        return sheets.sheet1

    def _get_googlesheet_client(self):
        """It is authorized using the service key and returns the Google Docs client object"""
        return pygsheets.authorize(
            service_file=self.credence_service_file
        )

    def search_abonement(
        self,
        data: List[List[Union[str, bool]]],
        search_col: int = 1,
        balance_col: int = 4,
        end_date_col: int = 5
    ) -> int:
        googlesheet_client: pygsheets.client.Client = self._get_googlesheet_client()
        wks: pygsheets.Spreadsheet = self._get_googlesheet_by_url(googlesheet_client)
        try:
            find_cell = wks.find(data, matchEntireCell=True, cols=(search_col, search_col))[0]
        except:
            return -1
        find_cell_row = find_cell.row
        end_date = wks.get_value((find_cell_row, end_date_col))
        balance = wks.get_value((find_cell_row, balance_col))
        return [end_date, balance]