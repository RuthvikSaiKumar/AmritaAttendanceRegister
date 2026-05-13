import pandas as pd
from fpdf import FPDF


class PDF(FPDF):
    cell_h = 7

    def header(self):
        self.set_font('Arial', '', 6)
        self.cell(0, 8, f'ATTENDANCE SHEET Code No./ Course/ {"_" * 50} Sem / Section / Year {"_" * 70}',
                  border=0, ln=1, align='L')

    def table_header(self, df, col_widths):
        self.set_font('Arial', 'B', 10)

        x = self.get_x()
        y = self.get_y()

        self.set_x(x)
        self.multi_cell(col_widths[0], self.cell_h, df[0], border=1, align='C')
        self.set_xy(x + col_widths[0], y)

        for i in range(1, 3):
            self.cell(col_widths[i], self.cell_h * 2, df[i], border=1, align='C')

        for i in range(3, len(df)):
            self.cell(col_widths[i], self.cell_h, '', border=1)

        self.ln()

        for i in range(3):
            self.cell(col_widths[i], self.cell_h, '', border=0)

        for i in range(3, len(df)):
            self.cell(col_widths[i], self.cell_h, df[i], border=1, align='C')

        self.ln()

    def table_footer(self, chunk_cols, chunk_col_widths):
        self.set_font('Arial', 'B', 10)
        self.cell(sum(chunk_col_widths[:3]), self.cell_h, 'Intls. of staff:', border=1, align='L')
        for _, width in zip(chunk_cols, chunk_col_widths[3:]):
            self.cell(width, self.cell_h, '', border=1)
        self.ln()

    def _fit_text(self, text: str, max_width: float) -> str:
        """Truncate text with '...' so it fits within max_width at the current font size."""
        if self.get_string_width(text) <= max_width:
            return text
        ellipsis_w = self.get_string_width('...')
        lo, hi = 0, len(text)
        while lo < hi - 1:
            mid = (lo + hi) // 2
            if self.get_string_width(text[:mid]) + ellipsis_w <= max_width:
                lo = mid
            else:
                hi = mid
        return text[:lo] + '...'

    def _compute_chunks(self, extra_cols, extra_col_widths, fixed_col_widths):
        page_w = self.w - self.l_margin - self.r_margin
        fixed_w = sum(fixed_col_widths)
        available = page_w - fixed_w

        if not extra_cols:
            return [([], list(fixed_col_widths))]

        total_cols = len(extra_cols)

        # Figure out how many columns fit per page using a minimum readable width
        min_col_w = 8  # mm, same as original
        cols_per_page = max(1, int(available / min_col_w))

        # How many pages do we need?
        import math
        num_chunks = math.ceil(total_cols / cols_per_page)

        # Distribute columns as evenly as possible across all chunks
        base_count = total_cols // num_chunks
        remainder = total_cols % num_chunks

        chunks = []
        start = 0
        for i in range(num_chunks):
            # First `remainder` chunks get one extra column
            count = base_count + (1 if i < remainder else 0)
            c_cols = extra_cols[start:start + count]
            # Each chunk fills the full available width
            day_w = available / len(c_cols)
            chunks.append((c_cols, list(fixed_col_widths) + [day_w] * len(c_cols)))
            start += count

        return chunks

    def draw_table(self, df, col_widths):
        fixed_cols = list(df.columns[:3])
        extra_cols = list(df.columns[3:])
        fixed_col_widths = col_widths[:3]
        extra_col_widths = col_widths[3:]

        chunks = self._compute_chunks(extra_cols, extra_col_widths, fixed_col_widths)

        # Bottom limit: leave room for footer row
        bottom_limit = self.h - self.b_margin - (self.cell_h * 2)

        for chunk_cols, chunk_col_widths in chunks:
            all_cols = fixed_cols + chunk_cols

            self.add_page()
            self.table_header(all_cols, chunk_col_widths)

            self.set_font('Arial', '', 10)

            for idx, row in df.iterrows():
                self.cell(chunk_col_widths[0], self.cell_h,
                          str(row['Roll No.']), border=1, align='C')

                reg = self._fit_text(str(row['Reg. No.']), chunk_col_widths[1] - 2)
                self.cell(chunk_col_widths[1], self.cell_h, reg, border=1, align='C')

                name = self._fit_text(str(row['Name of Student']), chunk_col_widths[2] - 2)
                self.cell(chunk_col_widths[2], self.cell_h, name, border=1, align='L')

                for col, width in zip(chunk_cols, chunk_col_widths[3:]):
                    self.cell(width, self.cell_h, str(row[col]), border=1, align='C')

                self.ln()

                # Mid-table page break
                if self.get_y() > bottom_limit and idx < len(df) - 1:
                    self.table_footer(chunk_cols, chunk_col_widths)
                    self.add_page()
                    self.table_header(all_cols, chunk_col_widths)
                    self.set_font('Arial', '', 10)

            # Pad remaining space with empty rows
            while self.get_y() + self.cell_h <= bottom_limit:
                for i in range(len(all_cols)):
                    self.cell(chunk_col_widths[i], self.cell_h, '', border=1)
                self.ln()

            self.table_footer(chunk_cols, chunk_col_widths)


def generate_attendance_sheet(students: pd.DataFrame, days: int, filename='attendance.pdf'):
    requirements = {
        'Roll No.': (1, 10),
        'Reg. No.': (1, 40),
        'Name of Student': (1, 60),
    }

    for day in range(1, days + 1):
        requirements[str(day)] = (1, 8)

    num_students = len(students)
    data = {}
    widths = []

    for name, (count, width) in requirements.items():
        for k in range(count):
            col_name = name if count == 1 else f'{name} {k + 1}'
            data[col_name] = [''] * num_students
            widths.append(width)

    data_frame = pd.DataFrame(data)
    data_frame['Roll No.'] = data_frame.index + 1
    data_frame['Reg. No.'] = students.iloc[:, 0].values
    data_frame['Name of Student'] = students.iloc[:, 1].values

    pdf = PDF(orientation='L')
    pdf.set_auto_page_break(auto=True, margin=20)  # manual page breaks for full control
    pdf.draw_table(data_frame, widths)
    pdf.output(filename)

    print("Attendance sheet saved successfully.")


if __name__ == '__main__':
    generate_attendance_sheet(pd.read_csv('./students.csv'), 60)