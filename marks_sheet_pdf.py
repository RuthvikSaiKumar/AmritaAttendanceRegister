import pandas as pd
from fpdf import FPDF

# todo: handle long names with ellipsis

num_students = 62
data = {
    'Roll No.': list(range(1, num_students + 1)),
    'Reg. No.': [f'BL.EN.U4RAE230{f"0{i}" if i < 10 else i}' for i in range(1, num_students + 1)],
    'Name of Student': ['Student Name'] * num_students,
    'Mid Sem (50)': [''] * num_students,
    'T3 (50)': [''] * num_students,
    'Q1 (10)': [''] * num_students,
    'Q2 (10)': [''] * num_students,
    'Q3 (10)': [''] * num_students,
    'Q4 (10)': [''] * num_students,
    'Quiz (15)': [''] * num_students,
    'Sessional marks (max. 50)': [''] * num_students,
    'End Sem Exam': [''] * num_students,
    'Total Marks': [''] * num_students,
    'Grade': [''] * num_students
}

data_frame = pd.DataFrame(data)


class PDF(FPDF):
    cell_h = 7

    def header(self):
        self.set_font('Arial', 'B', 8)
        self.cell(0, 8, 'MARKS SHEET', border=0, ln=1, align='C')

    def table_header(self, columns, col_widths):
        # sourcery skip: extract-duplicate-method

        self.set_font('Arial', '', 7)

        # roll no.
        x = self.get_x()
        y = self.get_y()

        self.set_x(x)
        self.multi_cell(col_widths[0], self.cell_h*1.5, columns[0], border=1, align='C')
        self.set_xy(x + col_widths[0], y)

        # reg no. and name
        for i in range(1, 3):
            self.cell(col_widths[i], self.cell_h*3, columns[i], border=1, align='C')
        for i in range(3, 10):
            self.cell(col_widths[i], self.cell_h, columns[i], border=1)

        # sessional
        x = self.get_x()
        y = self.get_y()

        self.set_x(x)
        self.multi_cell(col_widths[10], self.cell_h, columns[10], border=1, align='C')
        self.set_xy(x + col_widths[10], y)

        # end sem exam
        self.cell(col_widths[11], self.cell_h, columns[11], border=1, align='C')
        # total marks
        self.cell(col_widths[12], self.cell_h*3, columns[12], border=1, align='C')
        # grade # todo: make grade column longer
        self.cell(col_widths[13], self.cell_h, '', border='TR', align='C')

        self.ln()
        ####################################################################################

        for i in range(3):
            self.cell(col_widths[i], self.cell_h, '', border=0)
        for i in range(3, 10):
            self.cell(col_widths[i], self.cell_h, 'Date:', border=1)
        self.cell(col_widths[10], 8, '', border=0)
        # end sem exam
        self.cell(col_widths[11], self.cell_h, 'Date:', border=1, align='L')
        # total marks
        self.cell(col_widths[12], self.cell_h, '', border=0)
        # grade
        self.cell(col_widths[13], self.cell_h, 'Grade', border='R', align='C')

        self.ln()
        ########################################################################################

        for i in range(3):
            self.cell(col_widths[i], self.cell_h, '', border=0)
        for i in range(3, 10):
            self.cell(col_widths[i], self.cell_h, 'Obtained:', border=1, align='L')
        self.cell(col_widths[10], 8, '', border=0)
        # end sem exam
        self.cell(col_widths[11], self.cell_h, 'Obtained (100)', border=1, align='L')
        # total marks
        self.cell(col_widths[12], self.cell_h, '', border=0)
        # grade
        self.cell(col_widths[13], self.cell_h, '', border='RB', align='C')

        self.ln()

    def table_footer(self, current_col_widths):
        """ Creates the footer with the 'Intls. of staff:' text merging the first three columns """
        self.set_font('Arial', 'B', 10)

        self.cell(sum(current_col_widths[:3]), self.cell_h, 'Intls. of staff:', border=1, align='L')

        for i in current_col_widths[3:]:
            self.cell(i, self.cell_h, '', border=1)
        self.ln()

    def draw_table(self, df, col_widths):

        fixed_cols = list(df.columns[:3])
        extra_cols = [col for col in df.columns if col not in fixed_cols]

        current_col_widths = col_widths + [20] + [13] * 6 + [15] + [20] + [15] + [15]

        self.add_page()

        self.table_header(fixed_cols + extra_cols, current_col_widths)

        for idx, row in df.iterrows():
            self.set_font('Arial', '', 10)

            self.cell(current_col_widths[0], self.cell_h, str(row['Roll No.']), border=1, align='C')
            self.cell(current_col_widths[1], self.cell_h, str(row['Reg. No.']), border=1, align='C')
            self.cell(current_col_widths[2], self.cell_h, str(row['Name of Student']), border=1, align='L')
            for i, col in enumerate(extra_cols):
                self.cell(current_col_widths[3 + i], self.cell_h, str(row[col]), border=1, align='C')
            self.ln()

            if self.get_y() > 180:  # Approximate height for A4 in landscape mode
                self.table_footer(current_col_widths)
                self.add_page()
                self.table_header(fixed_cols + extra_cols, current_col_widths)

        # keep adding empty rows to fill the page
        while self.get_y() < 180:
            for i in range(len(current_col_widths)):
                self.cell(current_col_widths[i], self.cell_h, '', border=1)
            self.ln()

        self.table_footer(current_col_widths)


max_columns_per_page = 20

pdf = PDF(orientation='L')
pdf.set_auto_page_break(auto=True, margin=10)
pdf.draw_table(data_frame, [10, 40, 60])
pdf.output('marks_sheet.pdf')

print("Table with column split and repeating header saved as PDF in landscape mode successfully.")
