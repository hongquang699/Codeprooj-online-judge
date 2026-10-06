"""
VNOI Problem Package Manager
Manages problem package directory in problem-data/problems/{CODE}/
Handles problem.yml, statements, testcases, checkers, validators, and solution testing
"""

import os
import sys
import shutil
import zipfile
import io
import time
import subprocess
from django.conf import settings

def get_problem_dir(code):
    return os.path.join(settings.DMOJ_PROBLEM_DATA_ROOT, code)

def init_package(code, meta=None):
    base_dir = get_problem_dir(code)
    subdirs = ['statement', 'cases', 'validators', 'checkers', 'solutions', 'attachments']
    for s in subdirs:
        os.makedirs(os.path.join(base_dir, s), exist_ok=True)

    meta = meta or {}
    name = meta.get('name') or meta.get('title') or code
    time_limit = float(meta.get('time_limit') or 1.0)
    memory_limit = int(meta.get('memory_limit') or 256)
    points = float(meta.get('points') or 100.0)
    difficulty = meta.get('difficulty') or 'medium'
    status = meta.get('status') or 'draft'

    # Write problem.yml
    yml_path = os.path.join(base_dir, 'problem.yml')
    if not os.path.exists(yml_path):
        yml_content = f"""code: {code}
name: "{name}"
time_limit: {time_limit}
memory_limit: {memory_limit}
points: {points}
difficulty: {difficulty}
status: {status}
checker: standard
validator: standard
"""
        with open(yml_path, 'w', encoding='utf-8') as f:
            f.write(yml_content)

    # Write initial statement if missing
    md_path = os.path.join(base_dir, 'statement', 'statement.md')
    if not os.path.exists(md_path):
        sample_md = f"""# {name}

## Đề bài
Cho dữ liệu đầu vào. Hãy giải quyết bài toán theo đúng yêu cầu và in kết quả ra màn hình.

## Dữ liệu vào
Dòng đầu tiên chứa các số nguyên...

## Dữ liệu ra
In ra kết quả của bài toán.

## Ví dụ
### Input
```
2 3
```
### Output
```
5
```

## Giới hạn
- $1 \\le N \\le 10^5$
- Thời gian chạy: {time_limit}s
- Bộ nhớ: {memory_limit}MB
"""
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(sample_md)

    return base_dir

def get_statement(code):
    base_dir = get_problem_dir(code)
    md_path = os.path.join(base_dir, 'statement', 'statement.md')
    html_path = os.path.join(base_dir, 'statement', 'statement.html')

    markdown = ''
    html = ''
    if os.path.exists(md_path):
        with open(md_path, 'r', encoding='utf-8', errors='ignore') as f:
            markdown = f.read()
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()

    return {
        'markdown': markdown,
        'html': html or markdown
    }

def save_statement(code, markdown_content, html_content=None):
    base_dir = get_problem_dir(code)
    stmt_dir = os.path.join(base_dir, 'statement')
    os.makedirs(stmt_dir, exist_ok=True)

    md_path = os.path.join(stmt_dir, 'statement.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    html_path = os.path.join(stmt_dir, 'statement.html')
    final_html = html_content or markdown_content
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

    return True

def get_testcases(code):
    base_dir = get_problem_dir(code)
    cases_dir = os.path.join(base_dir, 'cases')
    if not os.path.exists(cases_dir):
        return []

    tests = []
    seen = set()
    for f in sorted(os.listdir(cases_dir)):
        if f.endswith('.in'):
            tid = f[:-3]
            seen.add(tid)

    for tid in sorted(seen):
        in_f = os.path.join(cases_dir, f"{tid}.in")
        out_f = os.path.join(cases_dir, f"{tid}.out")

        in_size = os.path.getsize(in_f) if os.path.exists(in_f) else 0
        has_out = os.path.exists(out_f)
        out_size = os.path.getsize(out_f) if has_out else 0

        # Sample snippet
        in_preview = ''
        out_preview = ''
        try:
            with open(in_f, 'r', encoding='utf-8', errors='ignore') as fi:
                in_preview = fi.read(200)
            if has_out:
                with open(out_f, 'r', encoding='utf-8', errors='ignore') as fo:
                    out_preview = fo.read(200)
        except Exception:
            pass

        tests.append({
            'id': tid,
            'has_in': True,
            'has_out': has_out,
            'in_size': in_size,
            'out_size': out_size,
            'in_preview': in_preview,
            'out_preview': out_preview,
            'points': 10
        })

    return tests

def save_testcase(code, tid, input_data, output_data, points=10):
    base_dir = get_problem_dir(code)
    cases_dir = os.path.join(base_dir, 'cases')
    os.makedirs(cases_dir, exist_ok=True)

    in_path = os.path.join(cases_dir, f"{tid}.in")
    out_path = os.path.join(cases_dir, f"{tid}.out")

    with open(in_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(input_data)
    with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(output_data)

    return True

def delete_testcase(code, tid):
    base_dir = get_problem_dir(code)
    cases_dir = os.path.join(base_dir, 'cases')
    in_path = os.path.join(cases_dir, f"{tid}.in")
    out_path = os.path.join(cases_dir, f"{tid}.out")

    deleted = False
    if os.path.exists(in_path):
        os.remove(in_path)
        deleted = True
    if os.path.exists(out_path):
        os.remove(out_path)
        deleted = True

    return deleted

def import_zip_testcases(code, zip_file_bytes):
    base_dir = get_problem_dir(code)
    cases_dir = os.path.join(base_dir, 'cases')
    os.makedirs(cases_dir, exist_ok=True)

    imported_count = 0
    with zipfile.ZipFile(io.BytesIO(zip_file_bytes)) as zf:
        for filename in zf.namelist():
            if filename.endswith('/') or '__MACOSX' in filename:
                continue
            base_name = os.path.basename(filename)
            if base_name.endswith('.in') or base_name.endswith('.out') or base_name.endswith('.ans'):
                target_name = base_name
                if target_name.endswith('.ans'):
                    target_name = target_name[:-4] + '.out'
                target_path = os.path.join(cases_dir, target_name)
                with open(target_path, 'wb') as f:
                    f.write(zf.read(filename))
                imported_count += 1

    return imported_count

def get_checker(code):
    base_dir = get_problem_dir(code)
    chk_dir = os.path.join(base_dir, 'checkers')
    for f in ['checker.cpp', 'checker.py', 'custom.cpp']:
        p = os.path.join(chk_dir, f)
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                return {'type': 'custom', 'filename': f, 'code': fl.read()}
    return {'type': 'standard', 'filename': 'standard', 'code': '// Standard White-space Agnostic Checker\n'}

def save_checker(code, content, filename='checker.cpp'):
    base_dir = get_problem_dir(code)
    chk_dir = os.path.join(base_dir, 'checkers')
    os.makedirs(chk_dir, exist_ok=True)
    p = os.path.join(chk_dir, filename)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

def get_validator(code):
    base_dir = get_problem_dir(code)
    val_dir = os.path.join(base_dir, 'validators')
    for f in ['validator.cpp', 'validator.py']:
        p = os.path.join(val_dir, f)
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                return {'type': 'custom', 'filename': f, 'code': fl.read()}
    return {'type': 'standard', 'filename': 'standard', 'code': '// Standard Non-empty Validator\n'}

def save_validator(code, content, filename='validator.cpp'):
    base_dir = get_problem_dir(code)
    val_dir = os.path.join(base_dir, 'validators')
    os.makedirs(val_dir, exist_ok=True)
    p = os.path.join(val_dir, filename)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

def get_solutions(code):
    base_dir = get_problem_dir(code)
    sol_dir = os.path.join(base_dir, 'solutions')
    if not os.path.exists(sol_dir):
        return []

    res = []
    for f in sorted(os.listdir(sol_dir)):
        if f.endswith(('.cpp', '.py', '.java', '.rs')):
            p = os.path.join(sol_dir, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                code_text = fl.read()
            res.append({
                'filename': f,
                'lang': 'cpp' if f.endswith('.cpp') else ('python' if f.endswith('.py') else 'java'),
                'code': code_text
            })
    return res

def save_solution(code, content, filename='official.py'):
    base_dir = get_problem_dir(code)
    sol_dir = os.path.join(base_dir, 'solutions')
    os.makedirs(sol_dir, exist_ok=True)
    p = os.path.join(sol_dir, filename)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

def test_solution(code, filename='official.py'):
    base_dir = get_problem_dir(code)
    sol_path = os.path.join(base_dir, 'solutions', filename)
    if not os.path.exists(sol_path):
        # Check if cpp exists
        for alt in ['official.cpp', 'official.py', 'solution.cpp', 'solution.py']:
            alt_path = os.path.join(base_dir, 'solutions', alt)
            if os.path.exists(alt_path):
                sol_path = alt_path
                filename = alt
                break

    if not os.path.exists(sol_path):
        return {'success': False, 'message': f'Chưa có file solution nào trong thư mục solutions/'}

    cases = get_testcases(code)
    if not cases:
        return {'success': False, 'message': 'Chưa có testcase nào trong thư mục cases/ để kiểm thử!'}

    cases_dir = os.path.join(base_dir, 'cases')
    results = []
    all_ac = True

    # Compile or prepare run command
    is_python = filename.endswith('.py')
    is_cpp = filename.endswith('.cpp')
    run_cmd = None
    tmp_exe = None

    if is_python:
        run_cmd = [sys.executable, sol_path]
    elif is_cpp:
        gpp = shutil.which('g++')
        if not gpp:
            return {'success': False, 'message': 'Không tìm thấy g++ trên máy chủ!'}
        tmp_dir = os.path.join(settings.BASE_DIR, 'judge', 'tmp')
        os.makedirs(tmp_dir, exist_ok=True)
        tmp_exe = os.path.abspath(os.path.join(tmp_dir, f"sol_test_{code}_{int(time.time())}.exe"))

        comp = subprocess.run([gpp, '-O2', '-std=c++17', sol_path, '-o', tmp_exe], capture_output=True, text=True, timeout=15)
        if comp.returncode != 0:
            return {'success': False, 'message': f'Lỗi biên dịch Solution: {comp.stderr}'}
        run_cmd = [tmp_exe]

    try:
        for c in cases:
            tid = c['id']
            in_file = os.path.join(cases_dir, f"{tid}.in")
            out_file = os.path.join(cases_dir, f"{tid}.out")

            if not os.path.exists(out_file):
                results.append({'case': tid, 'status': 'SKIPPED', 'feedback': 'Missing .out file'})
                all_ac = False
                continue

            with open(in_file, 'r', encoding='utf-8', errors='ignore') as fi:
                input_data = fi.read()
            with open(out_file, 'r', encoding='utf-8', errors='ignore') as fo:
                expected_data = fo.read().strip()

            start_t = time.perf_counter()
            proc = subprocess.run(run_cmd, input=input_data, capture_output=True, text=True, timeout=2.0)
            elapsed = time.perf_counter() - start_t
            actual_data = proc.stdout.strip()

            if proc.returncode != 0:
                results.append({'case': tid, 'status': 'RTE', 'time': elapsed, 'feedback': proc.stderr[:100]})
                all_ac = False
            elif actual_data == expected_data or actual_data.split() == expected_data.split():
                results.append({'case': tid, 'status': 'AC', 'time': elapsed, 'feedback': 'Accepted'})
            else:
                results.append({'case': tid, 'status': 'WA', 'time': elapsed, 'feedback': f'Expected {expected_data[:30]}, got {actual_data[:30]}'})
                all_ac = False

    except subprocess.TimeoutExpired:
        return {'success': False, 'message': 'Solution bị Time Limit Exceeded (> 2.0s)'}
    finally:
        if tmp_exe and os.path.exists(tmp_exe):
            try:
                os.remove(tmp_exe)
            except Exception:
                pass

    return {
        'success': True,
        'all_ac': all_ac,
        'solution': filename,
        'total': len(cases),
        'passed': sum(1 for r in results if r['status'] == 'AC'),
        'details': results
    }

def check_publish_readiness(code):
    stmt = get_statement(code)
    cases = get_testcases(code)
    solutions = get_solutions(code)

    has_stmt = len(stmt.get('markdown', '').strip()) > 30
    has_cases = len(cases) > 0
    has_sol = len(solutions) > 0

    checklist = [
        {'id': 'statement', 'name': 'Đề bài (Statement)', 'ok': has_stmt, 'desc': 'Đã có mô tả, input/output và ví dụ'},
        {'id': 'testcases', 'name': 'Bộ testcase (Cases)', 'ok': has_cases, 'desc': f'Có {len(cases)} testcase'},
        {'id': 'checker', 'name': 'Checker kiểm tra', 'ok': True, 'desc': 'Standard White-space agnostic checker'},
        {'id': 'solution', 'name': 'Solution mẫu (Official Solution)', 'ok': has_sol, 'desc': f'Đã upload {len(solutions)} solution'}
    ]

    ready = has_stmt and has_cases
    return {
        'ready': ready,
        'checklist': checklist
    }

def delete_package(code):
    base_dir = get_problem_dir(code)
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir, ignore_errors=True)
        return True
    return False
