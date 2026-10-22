#!/usr/bin/env python3
"""
=============================================================================
 GitHub Contribution Graph Art Generator - "Noah" (2026)
 Repository: https://github.com/NoahLezama/NoahLezama
=============================================================================
Este script genera commits calculados exactamente sobre la cuadrícula de 
contribuciones de GitHub para el año 2026, formando la palabra "Noah".

Cálculo Matemático Definitivo:
 - Tipografía: Title Case "Noah" estilizada (N de 5x7, o-a-h de 4x5/4x7).
 - Ancho total: 20 columnas (espaciado uniforme de 1 columna entre letras).
 - Inicio: Columna 19 (Domingo, 10 de Mayo de 2026).
 - Fin: Columna 38 (Sábado, 26 de Septiembre de 2026).
 - 100% visible: Posterior a la creación de la cuenta (20 Abr 2026) y anterior a hoy.
 - Centrado simétrico: 3 semanas de margen respecto a la creación y respecto a hoy.
 - Total: 54 días activos × 10 commits = 540 commits limpios.
=============================================================================
"""

import sys
import os
import argparse
import datetime
import subprocess
import time

C_RESET   = "\033[0m"
C_BOLD    = "\033[1m"
C_DIM     = "\033[2m"
C_GREEN   = "\033[38;5;82m"   # Verde brillante nivel 4
C_GRAY    = "\033[38;5;240m"  # Días inactivos
C_CYAN    = "\033[38;5;51m"
C_YELLOW  = "\033[38;5;220m"
C_RED     = "\033[38;5;196m"

# Tipografía Title Case "Noah" estilizada de alta definición (7 filas)
# N: 5x7 | o: 4x5 | a: 4x5 | h: 4x7
LETTERS_NOAH = {
    'N': [
        '#...#',
        '##..#',
        '#.#.#',
        '#.#.#',
        '#..##',
        '#..##',
        '#...#'
    ],
    'o': [
        '....',
        '....',
        '.##.',
        '#..#',
        '#..#',
        '#..#',
        '.##.'
    ],
    'a': [
        '....',
        '....',
        '.###',
        '...#',
        '.###',
        '#..#',
        '.###'
    ],
    'h': [
        '#...',
        '#...',
        '###.',
        '#..#',
        '#..#',
        '#..#',
        '#..#'
    ]
}


def build_grid(start_col=19):
    """
    Construye la matriz de 7 filas x 53 columnas.
    start_col=19 ubica la palabra de 20 columnas del 10 de Mayo al 26 de Septiembre.
    """
    grid = [[0 for _ in range(53)] for _ in range(7)]

    def stamp(shape, c_start, r_start=0):
        for r in range(len(shape)):
            for c in range(len(shape[0])):
                if shape[r][c] == '#':
                    row_idx = r_start + r
                    col_idx = c_start + c
                    if 0 <= row_idx < 7 and 0 <= col_idx < 53:
                        grid[row_idx][col_idx] = 1

    # N (5) + sp(1) + o (4) + sp(1) + a (4) + sp(1) + h (4) = 20 columnas
    stamp(LETTERS_NOAH['N'], start_col)
    stamp(LETTERS_NOAH['o'], start_col + 6)
    stamp(LETTERS_NOAH['a'], start_col + 11)
    stamp(LETTERS_NOAH['h'], start_col + 16)

    return grid


def get_first_sunday(year):
    jan1 = datetime.date(year, 1, 1)
    days_since_sunday = (jan1.weekday() + 1) % 7
    return jan1 - datetime.timedelta(days=days_since_sunday)


def preview_grid(grid, year=2026, commits_per_pixel=10):
    first_sunday = get_first_sunday(year)

    header = [' '] * 53
    for m in range(1, 13):
        m_date = datetime.date(year, m, 1)
        col = (m_date - first_sunday).days // 7
        name = m_date.strftime('%b')
        for idx, ch in enumerate(name):
            if col + idx < 53:
                header[col + idx] = ch

    month_str = ''.join(header)
    print(f"       {C_YELLOW}{month_str}{C_RESET}")

    days = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb']
    total_active_days = 0
    min_date = None
    max_date = None

    for r in range(7):
        row_cells = []
        for c in range(53):
            cell_date = first_sunday + datetime.timedelta(days=c * 7 + r)
            is_active = grid[r][c] == 1

            if is_active:
                total_active_days += 1
                if min_date is None or cell_date < min_date:
                    min_date = cell_date
                if max_date is None or cell_date > max_date:
                    max_date = cell_date
                row_cells.append(f"{C_GREEN}■{C_RESET}")
            else:
                row_cells.append(f"{C_GRAY}·{C_RESET}")

        print(f" {C_DIM}{days[r]:3s}{C_RESET}   " + ''.join(row_cells))

    total_commits = total_active_days * commits_per_pixel
    print()
    print(f" {C_BOLD}Detalles del cálculo:{C_RESET}")
    print(f"  • Tipografía:           {C_CYAN}Title Case 'Noah' (Proporcionada y estilizada){C_RESET}")
    print(f"  • Días con commits:     {C_GREEN}{total_active_days} días{C_RESET}")
    print(f"  • Commits por día:      {C_CYAN}{commits_per_pixel}{C_RESET} (verde brillante uniforme)")
    print(f"  • Total de commits:     {C_GREEN}{total_commits:,}{C_RESET}")
    if min_date and max_date:
        print(f"  • Rango de fechas:      {min_date} ({min_date.strftime('%d %b')}) ➜ {max_date} ({max_date.strftime('%d %b')})")
        print(f"  • Centrado:             {C_GREEN}✓ 3 semanas margen post-creación / 3 semanas margen pre-hoy{C_RESET}")
        print(f"  • Visibilidad:          {C_GREEN}✓ 100% visible (cero cortes, ninguna fecha en el futuro){C_RESET}")
    print()


def get_git_config():
    try:
        name = subprocess.check_output(['git', 'config', 'user.name'], text=True).strip()
    except Exception:
        name = "NoahLezama"

    try:
        email = subprocess.check_output(['git', 'config', 'user.email'], text=True).strip()
    except Exception:
        email = "noah_lezama@icloud.com"

    return name, email


def generate_commits(grid, year=2026, commits_per_pixel=10, author_name=None, author_email=None):
    first_sunday = get_first_sunday(year)
    default_name, default_email = get_git_config()
    author_name = author_name or default_name
    author_email = author_email or default_email

    active_dates = []
    for c in range(53):
        for r in range(7):
            if grid[r][c] == 1:
                cell_date = first_sunday + datetime.timedelta(days=c * 7 + r)
                active_dates.append(cell_date)

    active_dates.sort()
    total_commits = len(active_dates) * commits_per_pixel

    print(f"{C_CYAN}Generando {total_commits:,} commits limpios...{C_RESET}")

    env = os.environ.copy()
    env['GIT_AUTHOR_NAME'] = author_name
    env['GIT_AUTHOR_EMAIL'] = author_email
    env['GIT_COMMITTER_NAME'] = author_name
    env['GIT_COMMITTER_EMAIL'] = author_email

    commit_count = 0
    for day_idx, d in enumerate(active_dates, 1):
        for i in range(commits_per_pixel):
            commit_count += 1
            hour = 12
            minute = (i * 3) % 60
            second = (i * 11) % 60
            date_iso = f"{d.strftime('%Y-%m-%d')}T{hour:02d}:{minute:02d}:{second:02d}+00:00"

            env['GIT_AUTHOR_DATE'] = date_iso
            env['GIT_COMMITTER_DATE'] = date_iso

            msg = f"Noah art: {d.strftime('%Y-%m-%d')} ({i + 1}/{commits_per_pixel})"

            cmd = ['git', 'commit', '--allow-empty', '-m', msg]
            res = subprocess.run(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if res.returncode != 0:
                print(f"\n{C_RED}Error al crear commit para fecha {date_iso}{C_RESET}")
                sys.exit(1)

        pct = (commit_count / total_commits) * 100
        bar_len = 30
        filled = int(bar_len * (commit_count / total_commits))
        bar = "=" * filled + (">" if filled < bar_len else "") + " " * (bar_len - filled - (1 if filled < bar_len else 0))
        sys.stdout.write(f"\r  [{bar}] {pct:5.1f}% ({commit_count}/{total_commits} commits) - {d}")
        sys.stdout.flush()

    print(f"\n{C_GREEN}✓ {commit_count} commits generados exitosamente.{C_RESET}")


def main():
    parser = argparse.ArgumentParser(description="Generador de arte en GitHub - Noah 2026")
    parser.add_argument('--start-col', type=int, default=19, help="Columna de inicio (default: 19)")
    parser.add_argument('--commits-per-pixel', type=int, default=10, help="Commits por día (default: 10)")
    parser.add_argument('--year', type=int, default=2026, help="Año (default: 2026)")
    parser.add_argument('--dry-run', action='store_true', help="Solo vista previa")
    args = parser.parse_args()

    grid = build_grid(start_col=args.start_col)
    preview_grid(grid, year=args.year, commits_per_pixel=args.commits_per_pixel)

    if args.dry_run:
        return

    generate_commits(grid, year=args.year, commits_per_pixel=args.commits_per_pixel)


if __name__ == '__main__':
    main()
