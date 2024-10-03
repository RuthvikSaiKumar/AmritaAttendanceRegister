import pandas as pd
from fpdf import FPDF

# todo: handle long names with ellipsis

num_students = 62
days = 60

data = {
    'Roll No.': list(range(1, num_students + 1)),
    'Reg. No.': [f'BL.EN.U4RAE230{f"0{i}" if i < 10 else i}' for i in range(1, num_students + 1)],
    'Name of Student': ['Student Name'] * num_students
}

for i in range(1, days + 1):
    data[str(i)] = [''] * num_students

# Create the dataframe
data_frame = pd.DataFrame(data)


class PDF(FPDF):

    cell_h = 7

    def header(self):
        self.set_font('Arial', '', 6)
        self.cell(0, 8, f'ATTENDANCE SHEET Code No./ Course/ {"_" * 50} Sem / Section / Year {"_" * 70}',
                  border=0, ln=1, align='L')

    def table_header(self, columns, col_widths):

        self.set_font('Arial', 'B', 10)

        x = self.get_x()
        y = self.get_y()

        self.set_x(x)
        self.multi_cell(col_widths[0], 12, columns[0], border=1, align='C')
        self.set_xy(x + col_widths[0], y)

        for i in range(1, 3):
            self.cell(col_widths[i], 24, columns[i], border=1, align='C')
        for i in range(3, len(columns)-2):
            self.cell(col_widths[i], 16, '', border=1)
        self.ln()
        # Create empty cells for extra columns (attendance days)
        for i in range(3):
            self.cell(col_widths[i], 8, '', border=0)
        for i in range(3, len(columns)-2):
            self.cell(col_widths[i], 8, columns[i], border=1, align='C')

        self.set_xy(self.get_x(), y)
        self.multi_cell(col_widths[-2], 8, 'Classes\nConducted /\nScheduled', border=1, align='C')
        self.set_xy(self.get_x() + sum(col_widths[0:-1]), y)  # Move to the next cell
        self.multi_cell(col_widths[-1], 12, '% of\nAttend', border=1, align='C')

    def table_footer(self, chunk_cols, current_col_widths):
        """ Creates the footer with the 'Intls. of staff:' text merging the first three columns """
        self.set_font('Arial', 'B', 10)

        self.cell(sum(current_col_widths[:3]), self.cell_h, 'Intls. of staff:', border=1, align='L')

        for _ in chunk_cols:
            self.cell(6, self.cell_h, '', border=1)
        self.cell(30, self.cell_h, '', border=1)  # For 'Classes Conducted / Scheduled'
        self.cell(20, self.cell_h, '', border=1)  # For '% of Attend'
        self.ln()

    def draw_table(self, df, col_widths, split_at):

        fixed_cols = list(data_frame.columns[:3])
        extra_cols = [col for col in df.columns if col not in fixed_cols]

        for chunk_start in range(0, len(extra_cols), split_at):
            chunk_cols = extra_cols[chunk_start:chunk_start + split_at]

            # Add 'Classes Conducted / Scheduled' and '% of Attend' to the columns for each chunk
            current_col_widths = col_widths + [6] * len(chunk_cols) + [30, 20]

            self.add_page()

            # Include 'Classes Conducted / Scheduled' and '% of Attend' in the header
            self.table_header(fixed_cols + chunk_cols + ['Classes Conducted / Scheduled', '% of Attend'], current_col_widths)

            for idx, row in df.iterrows():
                # Print the main columns
                self.cell(current_col_widths[0], self.cell_h, str(row['Roll No.']), border=1, align='C')
                self.cell(current_col_widths[1], self.cell_h, str(row['Reg. No.']), border=1, align='C')
                self.cell(current_col_widths[2], self.cell_h, str(row['Name of Student']), border=1, align='L')
                
                
                for col in chunk_cols:
                    self.cell(6, self.cell_h, str(row[col]), border=1, align='C')

                
                self.cell(30, self.cell_h, '', border=1)  # Empty cell for 'Classes Conducted / Scheduled'
                self.cell(20, self.cell_h, '', border=1)  # Empty cell for '% of Attend'
                self.ln()

                if self.get_y() > 180:  # Approximate height for A4 in landscape mode
                    self.table_footer(chunk_cols, current_col_widths)
                    self.add_page()
                    self.table_header(fixed_cols + chunk_cols + ['Classes Conducted / Scheduled', '% of Attend'], current_col_widths)

            
            while self.get_y() < 185:
                for i in range(len(current_col_widths)):
                    self.cell(current_col_widths[i], self.cell_h, '', border=1)
                self.ln()

            self.table_footer(chunk_cols, current_col_widths)



max_columns_per_page = 20

pdf = PDF(orientation='L')
pdf.set_auto_page_break(auto=True, margin=10)


pdf.draw_table(data_frame, [10, 40, 60], max_columns_per_page)
pdf.output('attendance.pdf')

print("Table with column split, repeating header, and additional columns saved as PDF in landscape mode successfully.")
