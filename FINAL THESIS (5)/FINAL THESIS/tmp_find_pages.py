import subprocess

subprocess.run(['pdftotext', '-layout', 'main.pdf', 'tmp_full.txt'], check=True)
pages = open('tmp_full.txt', encoding='utf-8', errors='replace').read().split('\f')
print('physical pages:', len(pages))

targets = {
    'List of Tables': 'List of Tables',
    'Table 5.3 (caption)': 'Residual independence diagnostics',
    'Sensitivity 5.6.2': 'Sensitivity to unobserved confounding',
    'Graph falsification 5.6.3': 'Graph falsification',
}
for name, needle in targets.items():
    hits = [i + 1 for i, p in enumerate(pages) if needle in p]
    print(f'{name}: physical pages {hits}')

# find printed page numbers (last non-empty line) for those pages
for i, p in enumerate(pages):
    if i + 1 in (10, 48, 49, 55, 56, 57):
        lines = [l for l in p.splitlines() if l.strip()]
        print(f'physical {i+1} footer: {lines[-1].strip()!r}' if lines else f'physical {i+1}: empty')
