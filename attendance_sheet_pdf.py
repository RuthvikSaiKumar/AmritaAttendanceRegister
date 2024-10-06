import contextlib
import pandas as pd
from fpdf import FPDF

# todo: handle long names with ellipsis

num_students = 62
days = 50

requirements = {
    'Roll No.': (1, 10),
    'Reg. No.': (1, 40),
    'Name of Student': (1, 60),
}

for day in range(1, days + 1):
    requirements[str(day)] = (1, 8)

data = {}
widths = []

for name, value in requirements.items():
    for count in range(value[0]):
        data[f'{name}{"" if value[0] == 1 else f" {count + 1}"}'] = [''] * num_students
        widths.append(value[1])

data_frame = pd.DataFrame(data)


class PDF(FPDF):
    cell_h = 7

    def header(self):
        self.set_font('Arial', '', 6)
        self.cell(0, 8, f'ATTENDANCE SHEET Code No./ Course/ {"_" * 50} Sem / Section / Year {"_" * 70}',
                  border=0, ln=1, align='L')

    def table_header(self, df, col_widths):

        self.set_font('Arial', '', 10)

        # roll no.
        x = self.get_x()
        y = self.get_y()

        self.set_x(x)
        self.multi_cell(col_widths[0], self.cell_h, df[0], border=1, align='C')
        self.set_xy(x + col_widths[0], y)

        # reg no. and name
        for i in range(1, 3):
            self.cell(col_widths[i], self.cell_h * 2, df[i], border=1, align='C')

        # days (chunk)
        for i in range(3, len(df)):
            self.cell(col_widths[i], self.cell_h, '', border=1)

        self.ln()

        # empty for the first three columns
        for i in range(3):
            self.cell(col_widths[i], self.cell_h, '', border=0)

        # days (chunk)
        for i in range(3, len(df)):
            self.cell(col_widths[i], self.cell_h, df[i], border=1, align='C')

        self.ln()

    def table_footer(self, chunk_cols, chunk_col_widths):
        """ Creates the footer with the 'Intls. of staff:' text merging the first three columns """
        self.set_font('Arial', 'B', 10)

        self.cell(sum(chunk_col_widths[:3]), self.cell_h, 'Intls. of staff:', border=1, align='L')

        for _, width in zip(chunk_cols, chunk_col_widths[3:]):
            self.cell(width, self.cell_h, '', border=1)
        self.ln()

    @staticmethod
    def find_max_index(nums, threshold):
        """
        Find the maximum index x such that the sum of values from 0 to x is less than the given threshold.

        Args:
            nums (list): A list of numbers.
            threshold (int): The threshold value.

        Returns:
            int: The maximum index x.
        """
        total_sum = 0
        max_index = -1

        for i, num in enumerate(nums):
            total_sum += num
            if total_sum < threshold:
                max_index = i
            else:
                break

        return max_index

    def draw_table(self, df, col_widths):
        """
        Draws a table in a PDF document with column splitting and repeating headers in landscape mode.

        Args:
            df: A pandas DataFrame containing the data to be displayed in the table.
            col_widths: A list of integers representing the widths of each column in the table.

        Returns:
            None
        """

        fixed_cols = list(df.columns[:3])
        extra_cols = list(df.columns[3:])

        fixed_col_widths = col_widths[:3]
        extra_col_widths = col_widths[3:]

        split_at = 0
        if sum(col_widths) + pdf.l_margin + pdf.r_margin > pdf.w:
            split_at = self.find_max_index(extra_col_widths,
                                           pdf.w - pdf.l_margin - pdf.r_margin - sum(col_widths[:3])) + 1

        # noinspection PyUnusedLocal
        iterations = 0
        with contextlib.suppress(ZeroDivisionError):
            iterations = len(extra_cols) // split_at
        iterations += 1

        chunk_start = 0

        for _ in range(iterations):
            if split_at == 0:
                chunk_cols = extra_cols[chunk_start:]
                chunk_col_widths = fixed_col_widths + extra_col_widths[chunk_start:]
            else:
                chunk_cols = extra_cols[chunk_start:chunk_start + split_at]
                chunk_col_widths = fixed_col_widths + extra_col_widths[chunk_start:chunk_start + split_at]

            self.add_page()

            self.table_header(fixed_cols + chunk_cols, chunk_col_widths)

            for idx, row in df.iterrows():

                self.cell(chunk_col_widths[0], self.cell_h, str(row['Roll No.']), border=1, align='C')
                self.cell(chunk_col_widths[1], self.cell_h, str(row['Reg. No.']), border=1, align='C')
                self.cell(chunk_col_widths[2], self.cell_h, str(row['Name of Student']), border=1, align='L')

                for col, width in zip(chunk_cols, chunk_col_widths[3:]):
                    self.cell(width, self.cell_h, str(row[col]), border=1, align='C')
                self.ln()

                if self.get_y() > 180:
                    self.table_footer(chunk_cols, chunk_col_widths)
                    self.add_page()
                    self.table_header(fixed_cols + chunk_cols, chunk_col_widths)

            # keep adding empty rows to fill the page
            while self.get_y() < 180:
                for i in range(len(fixed_cols) + len(chunk_cols)):
                    self.cell(chunk_col_widths[i], self.cell_h, '', border=1)
                self.ln()

            self.table_footer(chunk_cols, chunk_col_widths)

            chunk_start += split_at


pdf = PDF(orientation='L')
pdf.set_auto_page_break(auto=True, margin=10)
pdf.draw_table(data_frame, widths)
pdf.output('attendance.pdf')

print("Table with column split and repeating header saved as PDF in landscape mode successfully.")
