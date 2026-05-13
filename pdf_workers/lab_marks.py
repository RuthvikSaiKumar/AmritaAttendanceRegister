import math
import pandas as pd
from fpdf import FPDF


class PDF(FPDF):
    cell_h = 7

    def header(self):
        self.set_font('Arial', 'B', 8)
        self.cell(0, 8, 'MARKS SHEET', border=0, ln=1, align='C')

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

    def table_header(self, df, col_widths, is_last_chunk, tail_count):
        self.set_font('Arial', '', 7)

        x = self.get_x()
        y = self.get_y()

        self.set_x(x)
        self.multi_cell(col_widths[0], self.cell_h * 2, df[0], border=1, align='C')
        self.set_xy(x + col_widths[0], y)

        self.cell(col_widths[1], self.cell_h * 4, df[1], border=1, align='C')
        self.cell(col_widths[2] - 15, self.cell_h * 4, df[2], border=1, align='C')

        self.cell(15, self.cell_h, 'Experiment:', border=1)

        exp_cols_count = len(df) - 3 - (tail_count if is_last_chunk else 0)

        for i in range(3, 3 + exp_cols_count):
            self.cell(col_widths[i], self.cell_h, df[i], border=1, align='C')

        if is_last_chunk:
            for i in range(3 + exp_cols_count, len(df)):
                self.cell(col_widths[i], self.cell_h * 3, df[i], border=1, align='C')
            self.set_y(y + self.cell_h)

        # middle row
        self.cell(col_widths[0], self.cell_h, '', border=0)
        self.cell(col_widths[1], self.cell_h, '', border=0)
        self.cell(col_widths[2] - 15, self.cell_h, '', border=0)
        self.cell(15, self.cell_h, 'Date:', border=1)
        for i in range(3, 3 + exp_cols_count):
            self.cell(col_widths[i], self.cell_h, '', border=1)
        self.ln()

        # bottom row
        self.cell(col_widths[0], self.cell_h, '', border=0)
        self.cell(col_widths[1], self.cell_h, '', border=0)
        self.cell(col_widths[2] - 15, self.cell_h, '', border=0)
        self.cell(15, self.cell_h, 'Max Marks:', border=1)
        for i in range(3, 3 + exp_cols_count):
            self.cell(col_widths[i], self.cell_h, '', border=1)
        self.ln()

        # division row
        self.cell(col_widths[0], self.cell_h, '', border=0)
        self.cell(col_widths[1], self.cell_h, '', border=0)
        self.cell(col_widths[2] - 15, self.cell_h, '', border=0)
        self.cell(15, self.cell_h, 'Division:', border=1)
        self.set_font('Arial', 'B', 5)
        for i in range(3, len(df)):
            w = col_widths[i]
            if i < 3 + exp_cols_count:
                for j in range(4):
                    label = 'Total' if j == 3 else ''
                    self.cell(w / 4, self.cell_h, label, border=1, align='L')
            else:
                self.cell(w, self.cell_h, '', border=1)
        self.set_font('Arial', 'B', 10)
        self.ln()

    def table_footer(self, all_display_cols, chunk_col_widths, exp_cols_count):
        self.set_font('Arial', 'B', 10)
        self.cell(sum(chunk_col_widths[:3]), self.cell_h, 'Intls. of staff:', border=1, align='L')
        for i, (col, width) in enumerate(zip(all_display_cols[3:], chunk_col_widths[3:])):
            if i < exp_cols_count:
                for _ in range(4):
                    self.cell(width / 4, self.cell_h, '', border=1)
            else:
                self.cell(width, self.cell_h, '', border=1)
        self.ln()

    def _compute_chunks(self, exp_cols, exp_col_widths, fixed_col_widths, tail_cols, tail_col_widths):
        page_w = self.w - self.l_margin - self.r_margin
        fixed_w = sum(fixed_col_widths)
        tail_w = sum(tail_col_widths)
        available = page_w - fixed_w

        if not exp_cols:
            return [([], list(fixed_col_widths) + list(tail_col_widths), True)]

        total_natural_w = sum(exp_col_widths)

        # Single page: everything fits with tail
        if total_natural_w + tail_w <= available:
            scale = (available - tail_w) / total_natural_w
            scaled = [w * scale for w in exp_col_widths]
            return [(
                exp_cols,
                list(fixed_col_widths) + scaled + list(tail_col_widths),
                True
            )]

        # Multi-page
        min_exp_w = 28
        cols_per_full_page = max(1, int(available / min_exp_w))
        cols_per_last_page = max(1, int((available - tail_w) / min_exp_w))

        total_cols = len(exp_cols)

        if total_cols <= cols_per_last_page:
            num_chunks = 1
        else:
            remaining = total_cols - cols_per_last_page
            num_chunks = 1 + math.ceil(remaining / cols_per_full_page)

        if num_chunks == 1:
            day_w = (available - tail_w) / total_cols
            return [(
                exp_cols,
                list(fixed_col_widths) + [day_w] * total_cols + list(tail_col_widths),
                True
            )]

        # First pass: group cols evenly across chunks
        cols_in_full = total_cols - cols_per_last_page
        base = cols_in_full // (num_chunks - 1)
        remainder = cols_in_full % (num_chunks - 1)
        start = 0
        raw_chunks = []

        for i in range(num_chunks - 1):
            count = base + (1 if i < remainder else 0)
            raw_chunks.append(('full', exp_cols[start:start + count]))
            start += count

        raw_chunks.append(('last', exp_cols[start:]))

        # Second pass: uniform width across all full chunks based on the largest
        max_day_count = max(len(c) for t, c in raw_chunks if t == 'full')
        full_day_w = available / max_day_count
        last_day_w = (available - tail_w) / len(raw_chunks[-1][1]) if raw_chunks[-1][1] else 0

        chunks = []
        for chunk_type, c_cols in raw_chunks:
            if chunk_type == 'full':
                chunks.append((c_cols, list(fixed_col_widths) + [full_day_w] * len(c_cols), False))
            else:
                last_widths = list(fixed_col_widths) + [last_day_w] * len(c_cols) + list(tail_col_widths)
                chunks.append((c_cols, last_widths, True))

        return chunks

    def draw_table(self, df, col_widths, tail_count=4):
        fixed_cols = list(df.columns[:3])
        exp_cols = list(df.columns[3:-tail_count])
        tail_cols = list(df.columns[-tail_count:])
        fixed_col_widths = col_widths[:3]
        tail_col_widths = col_widths[-tail_count:]
        exp_col_widths = col_widths[3:-tail_count]

        chunks = self._compute_chunks(exp_cols, exp_col_widths, fixed_col_widths, tail_cols, tail_col_widths)

        # Cross-chunk uniform width: all full chunks use the same day_w
        # based on the chunk with the most experiment columns
        full_chunks = [(c, w, l) for c, w, l in chunks if not l]
        if full_chunks:
            max_exp_count = max(len(c) for c, w, l in full_chunks)
            page_w = self.w - self.l_margin - self.r_margin
            available = page_w - sum(fixed_col_widths)
            uniform_day_w = available / max_exp_count
            rebuilt = []
            for c_cols, c_widths, is_last in chunks:
                if not is_last:
                    new_widths = list(fixed_col_widths) + [uniform_day_w] * len(c_cols)
                    rebuilt.append((c_cols, new_widths, False))
                else:
                    rebuilt.append((c_cols, c_widths, True))
            chunks = rebuilt

        bottom_limit = self.h - self.b_margin - (self.cell_h * 2)

        for chunk_exp_cols, chunk_col_widths, is_last in chunks:
            all_cols = fixed_cols + chunk_exp_cols + (tail_cols if is_last else [])
            exp_cols_count = len(chunk_exp_cols)

            self.add_page()
            self.table_header(all_cols, chunk_col_widths, is_last, tail_count)

            self.set_font('Arial', '', 10)

            for idx, row in df.iterrows():
                self.cell(chunk_col_widths[0], self.cell_h, str(row['Roll No.']), border=1, align='C')

                reg = self._fit_text(str(row['Reg. No.']), chunk_col_widths[1] - 2)
                self.cell(chunk_col_widths[1], self.cell_h, reg, border=1, align='C')

                name = self._fit_text(str(row['Name of Student']), chunk_col_widths[2] - 2)
                self.cell(chunk_col_widths[2], self.cell_h, name, border=1, align='L')

                for i, (col, width) in enumerate(zip(all_cols[3:], chunk_col_widths[3:])):
                    if i < exp_cols_count:
                        for _ in range(4):
                            self.cell(width / 4, self.cell_h, str(row[col]), border=1, align='C')
                    else:
                        self.cell(width, self.cell_h, str(row[col]), border=1, align='C')
                self.ln()

                if self.get_y() > bottom_limit and idx < len(df) - 1:
                    self.table_footer(all_cols, chunk_col_widths, exp_cols_count)
                    self.add_page()
                    self.table_header(all_cols, chunk_col_widths, is_last, tail_count)
                    self.set_font('Arial', '', 10)

            while self.get_y() + self.cell_h <= bottom_limit:
                for j, col in enumerate(all_cols):
                    w = chunk_col_widths[j]
                    if j >= 3 and j < 3 + exp_cols_count:
                        for _ in range(4):
                            self.cell(w / 4, self.cell_h, '', border=1)
                    else:
                        self.cell(w, self.cell_h, '', border=1)
                self.ln()

            self.table_footer(all_cols, chunk_col_widths, exp_cols_count)


def generate_marks_sheet(students: pd.DataFrame, requirements: dict, filename='lab_marks_sheet.pdf'):
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
    pdf.draw_table(data_frame, widths, tail_count=4)
    pdf.output(filename)

    print("Lab marks sheet saved successfully.")


if __name__ == '__main__':
    requirements_dict = {
        'Roll No.': (1, 10),
        'Reg. No.': (1, 38),
        'Name of Student': (1, 60),
    }

    number_of_experiments = 12

    for k in range(1, number_of_experiments + 1):
        requirements_dict[str(k)] = (1, 28)

    requirements_dict['Mid Sem'] = (1, 28)
    requirements_dict['End Sem'] = (1, 28)
    requirements_dict['Total'] = (1, 14)
    requirements_dict['Grade'] = (1, 14)

    generate_marks_sheet(pd.read_csv('students.csv'), requirements_dict)