import pandas as pd

df = pd.read_excel('UAT.xlsx')
df.columns = [c.strip() for c in df.columns]

names = df['Nama'].tolist()
scores = df.iloc[:, 4:30].values

q_codes = [f'P{str(i).zfill(2)}' for i in range(1, 27)]

aspects = {
    'Kemudahan Penggunaan': [0, 1, 9, 11, 15, 16, 17, 19, 21],
    'Kejelasan Antarmuka':  [3, 4, 5, 7, 8, 13, 14],
    'Persepsi Kinerja':     [2, 6, 10, 18, 20],
    'Kualitas Informasi':   [12, 22],
    'Kepuasan Pengguna':    [23, 24, 25],
}

# Page geometry: inner=4cm, outer=3cm, A4 (21cm)
# textwidth = 21 - 4 - 3 = 14cm
# tabcolsep default = 6pt ~ 0.212cm
# arrayrulewidth default = 0.4pt ~ 0.0141cm
# For a table with N score cols + 1 resp col + 1 avg col = N+2 cols, N+3 borders
# textwidth = resp_w + N*q_w + avg_w + (N+2)*2*tabcolsep + (N+3)*arrayrulewidth
# q_w = (textwidth - resp_w - avg_w - (N+2)*0.424 - (N+3)*0.0141) / N
# We'll use \dimexpr in LaTeX for accuracy, substituting actual N values

def col_spec(N):
    """Returns LaTeX column spec using dimexpr to fill exactly \textwidth"""
    # Total fixed widths: resp=3.5cm, avg=1.5cm, sum=5.0cm
    # Separator: (N+2)*2\tabcolsep = (N+2)*12pt  (since \tabcolsep=6pt, 2*6=12pt per col)
    # Borders: (N+3)*\arrayrulewidth
    # q_w = (\textwidth - 5.0cm - (N+2)*12pt - (N+3)*\arrayrulewidth) / N
    n_tabcolsep = (N + 2) * 12  # in pt, multiply of \tabcolsep (6pt) * 2
    n_borders = N + 3
    qw = (f'\\dimexpr(\\textwidth - 5.0cm - {n_tabcolsep}\\tabcolsep - {n_borders}\\arrayrulewidth)/{N}\\relax')
    resp_col = '>{\raggedright\\arraybackslash}p{3.5cm}'
    q_col = f'>{{\\centering\\arraybackslash}}p{{{qw}}}'
    avg_col = '>{{\\centering\\arraybackslash}}p{{1.5cm}}'
    spec = '|' + resp_col + '|' + '|'.join([q_col] * N) + '|' + avg_col + '|'
    return spec

def gen_table(aspect_name, q_indices, scores, names, q_codes):
    cols = [q_codes[i] for i in q_indices]
    N = len(cols)
    spec = col_spec(N)

    lines = []
    lines.append(f'% ============================================================')
    lines.append(f'% {aspect_name}')
    lines.append(f'% ============================================================')
    lines.append(f'\\begin{{longtable}}{{{spec}}}')
    lines.append(f'\\caption*{{Tabel: Data Mentah UAT --- {aspect_name}}} \\\\')
    lines.append('\\hline')

    header = ('\\textbf{Responden} & '
              + ' & '.join([f'\\textbf{{{c}}}' for c in cols])
              + ' & \\textbf{Rata-\\newline rata} \\\\ \\hline')
    lines.append(header)
    lines.append('\\endfirsthead')
    lines.append('\\hline')
    lines.append(header)
    lines.append('\\endhead')
    lines.append('\\hline')
    lines.append('\\endfoot')
    lines.append('\\hline')
    lines.append('\\endlastfoot')
    lines.append('')

    col_totals = [0.0] * N

    for r_idx, name in enumerate(names):
        row_scores = [int(scores[r_idx][i]) for i in q_indices]
        row_avg = round(sum(row_scores) / len(row_scores), 2)
        for j, s in enumerate(row_scores):
            col_totals[j] += s
        row_str = (f'{name} & '
                   + ' & '.join([str(s) for s in row_scores])
                   + f' & {row_avg:.2f} \\\\ \\hline')
        lines.append(row_str)

    n = len(names)
    col_avgs = [round(t / n, 2) for t in col_totals]
    overall = round(sum(col_totals) / (n * N), 2)
    avg_row = ('\\textbf{Rata-rata} & '
               + ' & '.join([f'\\textbf{{{a:.2f}}}' for a in col_avgs])
               + f' & \\textbf{{{overall:.2f}}} \\\\ \\hline')
    lines.append(avg_row)
    lines.append('\\end{longtable}')
    lines.append('')
    return '\n'.join(lines)

output = []
output.append('\\cleardoublepage')
output.append('\\chapter{DATA MENTAH \\textit{USER ACCEPTANCE TESTING}}')
output.append('')
output.append('Lampiran ini menyajikan data mentah hasil kuesioner \\textit{User Acceptance Testing} (UAT) yang diisi oleh 35 responden. Data disajikan secara terperinci per aspek penilaian untuk setiap pernyataan (P01--P26) dengan skala Likert 1 hingga 5.')
output.append('')

for aspect_name, q_indices in aspects.items():
    output.append(gen_table(aspect_name, q_indices, scores, names, q_codes))

print('\n'.join(output))
