import pandas as pd
from fpdf import FPDF


class PDF(FPDF):
    cell_h = 7

    def header(self):
        self.set_font('Arial', 'B', 8)
        self.cell(0, 8, 'MARKS SHEET', border=0, ln=1, align='C')
        self.cell(0, 8, 'M.S. = Mid Sem, E.M. = End Sem, Q = Quiz, A = Assignment', border=0, ln=1, align='C')

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

    def table_header(self, df, col_widths):
        self.set_font('Arial', 'B', 7)

        x = self.get_x()
        y = self.get_y()

        self.set_x(x)
        self.multi_cell(col_widths[0], self.cell_h * 1.5, df[0], border=1, align='C')
        self.set_xy(x + col_widths[0], y)

        self.cell(col_widths[1], self.cell_h * 3, df[1], border=1, align='C')
        self.cell(col_widths[2] - 15, self.cell_h * 3, df[2], border=1, align='C')

        self.cell(15, self.cell_h, 'Evaluation:', border=1)

        for i in range(3, len(df)):
            self.cell(col_widths[i], self.cell_h, df[i], border=1, align='C')

        self.ln()

        self.cell(col_widths[0], self.cell_h, '', border=0)
        self.cell(col_widths[1], self.cell_h, '', border=0)
        self.cell(col_widths[2] - 15, self.cell_h, '', border=0)

        self.cell(15, self.cell_h, 'Date:', border=1)

        for i in range(3, len(df)):
            self.cell(col_widths[i], self.cell_h, '', border=1, align='L')

        self.ln()

        self.cell(col_widths[0], self.cell_h, '', border=0)
        self.cell(col_widths[1], self.cell_h, '', border=0)
        self.cell(col_widths[2] - 15, self.cell_h, '', border=0)

        self.cell(15, self.cell_h, 'Max Marks:', border=1)

        for i in range(3, len(df)):
            self.cell(col_widths[i], self.cell_h, '', border=1, align='L')

        self.ln()

    def table_footer(self, chunk_cols, chunk_col_widths):
        self.set_font('Arial', 'B', 10)
        self.cell(sum(chunk_col_widths[:3]), self.cell_h, 'Intls. of staff:', border=1, align='L')
        for _, width in zip(chunk_cols, chunk_col_widths[3:]):
            self.cell(width, self.cell_h, '', border=1)
        self.ln()

    def _compute_chunks(self, extra_cols, extra_col_widths, fixed_col_widths):
        page_w = self.w - self.l_margin - self.r_margin
        fixed_w = sum(fixed_col_widths)
        available = page_w - fixed_w

        if not extra_cols:
            return [([], list(fixed_col_widths))]

        total_natural_w = sum(extra_col_widths)

        # Single page: scale proportionally to fill available width
        if total_natural_w <= available:
            scale = available / total_natural_w
            scaled_widths = [w * scale for w in extra_col_widths]
            return [(extra_cols, list(fixed_col_widths) + scaled_widths)]

        # Multi-page: group cols using natural widths
        raw_chunks = []
        max_day_count = 0
        start = 0

        while start < len(extra_cols):
            total = 0
            end = start
            for i in range(start, len(extra_cols)):
                if total + extra_col_widths[i] > available:
                    break
                total += extra_col_widths[i]
                end = i + 1

            if end == start:
                end = start + 1

            c_cols = extra_cols[start:end]
            raw_chunks.append(c_cols)
            if len(c_cols) > max_day_count:
                max_day_count = len(c_cols)
            start = end

        # Second pass: all full chunks use uniform width based on max_day_count
        # last chunk fills independently — both preserve relative proportions
        chunks = []
        for i, c_cols in enumerate(raw_chunks):
            is_last = (i == len(raw_chunks) - 1)

            if is_last and len(c_cols) < max_day_count:
                # last chunk: fill available independently
                chunk_target_total = available
            else:
                # full chunks: all same total width = available
                # but scaled so col density matches max_day_count
                chunk_target_total = available * len(c_cols) / max_day_count

            chunk_natural = [extra_col_widths[extra_cols.index(c)] for c in c_cols]
            chunk_natural_total = sum(chunk_natural)
            scaled = [w * chunk_target_total / chunk_natural_total for w in chunk_natural]

            chunks.append((c_cols, list(fixed_col_widths) + scaled))

        return chunks

    def draw_table(self, df, col_widths):
        fixed_cols = list(df.columns[:3])
        extra_cols = list(df.columns[3:])
        fixed_col_widths = col_widths[:3]
        extra_col_widths = col_widths[3:]

        chunks = self._compute_chunks(extra_cols, extra_col_widths, fixed_col_widths)

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

                if self.get_y() > bottom_limit and idx < len(df) - 1:
                    self.table_footer(chunk_cols, chunk_col_widths)
                    self.add_page()
                    self.table_header(all_cols, chunk_col_widths)
                    self.set_font('Arial', '', 10)

            while self.get_y() + self.cell_h <= bottom_limit:
                for i in range(len(all_cols)):
                    self.cell(chunk_col_widths[i], self.cell_h, '', border=1)
                self.ln()

            self.table_footer(chunk_cols, chunk_col_widths)


def generate_marks_sheet(students: pd.DataFrame, requirements: dict, filename='marks_sheet.pdf'):
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
    pdf.draw_table(data_frame, widths)
    pdf.output(filename)

    print("Marks sheet saved successfully.")


if __name__ == '__main__':
    end_sem_type = 'Written'

    requirements_dict = {
        'Roll No.': (1, 10),
        'Reg. No.': (1, 40),
        'Name of Student': (1, 60),
        'M.S.': (1, 10),
        'Missed M.S.': (1, 20),
        'Q': (3, 10),
        'Missed Q': (1, 15),
        'A': (1, 10),
        'Sessional': (1, 15),
        f'E.M. ({end_sem_type})': (1, 20),
        'Total': (1, 15),
        'Grade': (1, 15)
    }

    generate_marks_sheet(pd.read_csv('./students.csv'), requirements_dict)