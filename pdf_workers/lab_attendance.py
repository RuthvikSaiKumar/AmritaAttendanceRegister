import math
import pandas as pd
from fpdf import FPDF


class PDF(FPDF):
    cell_h = 7

    def header(self):
        self.set_font('Arial', '', 10)
        self.cell(0, 8, f'ATTENDANCE SHEET(Practical Subject) Code No./ Course/ Catg. {"_" * 30} '
                        f'Sem / Section / Year {"_" * 35}',
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
        self.cell(sum(col_widths[3:]) if col_widths[-2] == 6 else sum(col_widths[3:-2]),
                  8, 'DATE', border=1, align='C')

        self.ln()

        for i in range(3):
            self.cell(col_widths[i], 8, '', border=0)
        for i in range(3, len(columns) if col_widths[-2] == 6 else len(columns) - 2):
            self.cell(col_widths[i], 8, '', border=1)
        self.ln()

        if col_widths[-2] == 6:
            for i in range(3):
                self.cell(col_widths[i], 8, '', border=0)
            for i in range(3, len(columns)):
                self.cell(col_widths[i], 8, columns[i], border=1, align='C')
        else:
            for i in range(3):
                self.cell(col_widths[i], 8, '', border=0)
            for i in range(3, len(columns) - 2):
                self.cell(col_widths[i], 8, columns[i], border=1, align='C')

            self.set_xy(self.get_x(), y)
            self.multi_cell(col_widths[-2], 8, columns[-2], border=1, align='C')
            self.set_xy(self.get_x() + sum(col_widths[:-1]), y)
            self.multi_cell(col_widths[-1], 12, columns[-1], border=1, align='C')

        if col_widths[-2] == 6:
            self.ln()

    def table_footer(self, chunk_cols, chunk_col_widths):
        self.set_font('Arial', 'B', 10)
        self.cell(sum(chunk_col_widths[:3]), self.cell_h, 'Intls. of staff:', border=1, align='L')
        for _, width in zip(chunk_cols, chunk_col_widths[3:]):
            self.cell(width, self.cell_h, '', border=1)
        self.ln()

    def _fit_text(self, text: str, max_width: float) -> str:
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

    def _compute_chunks(self, extra_cols, fixed_col_widths, tail_col_widths):
        """
        extra_cols      : day columns only (no tail cols like 'Classes Conducted', '% Attend')
        fixed_col_widths: widths of Roll No., Reg. No., Name
        tail_col_widths : widths of the trailing summary columns (always on last chunk)
        """
        page_w = self.w - self.l_margin - self.r_margin
        fixed_w = sum(fixed_col_widths)
        tail_w = sum(tail_col_widths)
        available = page_w - fixed_w  # space for day cols (tail handled separately)

        if not extra_cols:
            return [([], list(fixed_col_widths) + list(tail_col_widths))]

        # How many day cols fit per page (last page reserves space for tail cols)
        min_day_w = 6  # mm
        cols_per_full_page = max(1, int(available / min_day_w))
        cols_per_last_page = max(1, int((available - tail_w) / min_day_w))

        total_cols = len(extra_cols)

        # Figure out number of chunks needed
        if total_cols <= cols_per_last_page:
            num_chunks = 1
        else:
            remaining_after_last = total_cols - cols_per_last_page
            num_chunks = 1 + math.ceil(remaining_after_last / cols_per_full_page)

        # Distribute day cols evenly across all chunks except the last
        # Last chunk always gets tail cols appended
        if num_chunks == 1:
            day_w = (available - tail_w) / total_cols
            return [(
                extra_cols,
                list(fixed_col_widths) + [day_w] * total_cols + list(tail_col_widths)
            )]

        # For multi-chunk: split evenly across first (num_chunks-1) chunks
        cols_in_full_chunks = total_cols - cols_per_last_page
        base = cols_in_full_chunks // (num_chunks - 1)
        remainder = cols_in_full_chunks % (num_chunks - 1)

        chunks = []
        start = 0

        for i in range(num_chunks - 1):
            count = base + (1 if i < remainder else 0)
            c_cols = extra_cols[start:start + count]
            day_w = available / len(c_cols)
            chunks.append((c_cols, list(fixed_col_widths) + [day_w] * len(c_cols)))
            start += count

        # Last chunk: remaining day cols + tail cols
        c_cols = extra_cols[start:]
        day_w = (available - tail_w) / len(c_cols) if c_cols else 0
        last_widths = list(fixed_col_widths) + [day_w] * len(c_cols) + list(tail_col_widths)
        chunks.append((c_cols, last_widths))

        return chunks

    def draw_table(self, df, col_widths, tail_count=2):
        fixed_cols = list(df.columns[:3])
        day_cols = list(df.columns[3:-tail_count])
        tail_cols = list(df.columns[-tail_count:])

        fixed_col_widths = col_widths[:3]
        tail_col_widths = col_widths[-tail_count:]

        chunks = self._compute_chunks(day_cols, fixed_col_widths, tail_col_widths)

        bottom_limit = self.h - self.b_margin - (self.cell_h * 2)

        for chunk_idx, (chunk_day_cols, chunk_col_widths) in enumerate(chunks):
            is_last_chunk = (chunk_idx == len(chunks) - 1)

            if is_last_chunk:
                all_cols = fixed_cols + chunk_day_cols + tail_cols
            else:
                all_cols = fixed_cols + chunk_day_cols

            self.add_page()
            self.table_header(all_cols, chunk_col_widths)

            self.set_font('Arial', '', 10)

            for idx, row in df.iterrows():
                self.cell(chunk_col_widths[0], self.cell_h, str(row['Roll No.']), border=1, align='C')

                reg = self._fit_text(str(row['Reg. No.']), chunk_col_widths[1] - 2)
                self.cell(chunk_col_widths[1], self.cell_h, reg, border=1, align='C')

                name = self._fit_text(str(row['Name of Student']), chunk_col_widths[2] - 2)
                self.cell(chunk_col_widths[2], self.cell_h, name, border=1, align='L')

                for col, width in zip(all_cols[3:], chunk_col_widths[3:]):
                    self.cell(width, self.cell_h, str(row[col]), border=1, align='C')
                self.ln()

                if self.get_y() > bottom_limit and idx < len(df) - 1:
                    self.table_footer(all_cols[3:], chunk_col_widths)
                    self.add_page()
                    self.table_header(all_cols, chunk_col_widths)
                    self.set_font('Arial', '', 10)

            while self.get_y() + self.cell_h <= bottom_limit:
                for i in range(len(all_cols)):
                    self.cell(chunk_col_widths[i], self.cell_h, '', border=1)
                self.ln()

            self.table_footer(all_cols[3:], chunk_col_widths)


def generate_attendance_sheet(students: pd.DataFrame, days: int, filename='lab_attendance.pdf'):
    requirements = {
        'Roll No.': (1, 10),
        'Reg. No.': (1, 40),
        'Name of Student': (1, 60),
    }

    for day in range(1, days + 1):
        requirements[str(day)] = (1, 6)

    requirements['Classes Conducted / Scheduled'] = (1, 25)
    requirements['% of Attend'] = (1, 20)

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
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.draw_table(data_frame, widths, tail_count=2)
    pdf.output(filename)

    print("Lab attendance sheet saved successfully.")


if __name__ == '__main__':
    generate_attendance_sheet(pd.read_csv('students.csv'), 20)