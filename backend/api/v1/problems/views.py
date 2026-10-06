"""
VNOI Problem Authoring API v1 Views
Comprehensive endpoints for Problem Setter and Admin workflows
"""

import os
import io
import zipfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from backend.judge.models import Problem, ProblemType, Profile
from backend.judge import problem_package as pkg

def api_response(data=None, error=None, status_code=200):
    if error:
        return Response({'status': status_code, 'error': error}, status=status_code)
    return Response({'status': status_code, 'data': data}, status=status_code)

def get_problem_by_id_or_code(val):
    if str(val).isdigit():
        return get_object_or_404(Problem, id=int(val))
    return get_object_or_404(Problem, code=val)

class ProblemListCreateAPI(APIView):
    def get(self, request):
        qs = Problem.objects.all().order_by('-date')
        status_filter = request.GET.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        q = request.GET.get('q')
        if q:
            qs = qs.filter(name__icontains=q) | qs.filter(code__icontains=q)

        data = []
        for p in qs:
            tests = pkg.get_testcases(p.code)
            data.append({
                'id': p.id,
                'code': p.code,
                'title': p.name,
                'time_limit': p.time_limit,
                'memory_limit': int(p.memory_limit / 1024),
                'points': p.points,
                'difficulty': p.difficulty,
                'status': p.status,
                'is_public': p.is_public,
                'testcase_count': len(tests),
                'date': p.date
            })
        return api_response({'problems': data, 'total': len(data)})

    def post(self, request):
        code = (request.data.get('code') or '').strip().upper()
        title = (request.data.get('title') or request.data.get('name') or '').strip()
        time_limit = float(request.data.get('time_limit') or 1.0)
        memory_limit = int(request.data.get('memory_limit') or 256)
        points = float(request.data.get('points') or 100.0)
        difficulty = request.data.get('difficulty') or 'medium'
        tags = request.data.get('tags') or []

        if not code or not title:
            return api_response(error={'message': 'Mã bài và Tiêu đề không được để trống'}, status_code=400)

        if Problem.objects.filter(code=code).exists():
            return api_response(error={'message': f'Mã bài {code} đã tồn tại'}, status_code=400)

        # 1. Initialize filesystem package in problem-data/problems/{code}/
        pkg.init_package(code, {
            'title': title,
            'time_limit': time_limit,
            'memory_limit': memory_limit,
            'points': points,
            'difficulty': difficulty,
            'status': 'draft'
        })

        # 2. Create Problem DB record
        stmt_info = pkg.get_statement(code)
        prob = Problem.objects.create(
            code=code,
            name=title,
            description=stmt_info.get('html') or stmt_info.get('markdown') or '',
            time_limit=time_limit,
            memory_limit=memory_limit * 1024,
            points=points,
            difficulty=difficulty,
            status='draft',
            is_public=False
        )

        # Tags
        if isinstance(tags, list):
            for t in tags:
                ptype, _ = ProblemType.objects.get_or_create(name=t.lower(), defaults={'full_name': t})
                prob.types.add(ptype)

        return api_response({
            'id': prob.id,
            'code': prob.code,
            'title': prob.name,
            'status': prob.status,
            'message': f'Tạo bài tập {code} thành công'
        }, status_code=201)

class ProblemDetailAPI(APIView):
    def get(self, request, pk):
        p = get_problem_by_id_or_code(pk)
        stmt = pkg.get_statement(p.code)
        tests = pkg.get_testcases(p.code)
        readiness = pkg.check_publish_readiness(p.code)

        return api_response({
            'id': p.id,
            'code': p.code,
            'title': p.name,
            'time_limit': p.time_limit,
            'memory_limit': int(p.memory_limit / 1024),
            'points': p.points,
            'difficulty': p.difficulty,
            'status': p.status,
            'is_public': p.is_public,
            'tags': [t.name for t in p.types.all()],
            'statement': stmt,
            'testcase_count': len(tests),
            'checklist': readiness.get('checklist', []),
            'is_ready': readiness.get('ready', False)
        })

    def patch(self, request, pk):
        p = get_problem_by_id_or_code(pk)
        if 'title' in request.data:
            p.name = request.data['title']
        if 'time_limit' in request.data:
            p.time_limit = float(request.data['time_limit'])
        if 'memory_limit' in request.data:
            p.memory_limit = int(request.data['memory_limit']) * 1024
        if 'points' in request.data:
            p.points = float(request.data['points'])
        if 'difficulty' in request.data:
            p.difficulty = request.data['difficulty']
        if 'status' in request.data:
            p.status = request.data['status']
            p.is_public = (p.status == 'published')

        p.save()
        return api_response({'id': p.id, 'code': p.code, 'message': 'Cập nhật thành công'})

    def delete(self, request, pk):
        p = get_problem_by_id_or_code(pk)
        code = p.code
        pkg.delete_package(code)
        p.delete()
        return api_response({'message': f'Đã xóa bài tập {code} và toàn bộ dữ liệu'})

class ProblemStatementAPI(APIView):
    def get(self, request, pk):
        p = get_problem_by_id_or_code(pk)
        stmt = pkg.get_statement(p.code)
        return api_response(stmt)

    def put(self, request, pk):
        p = get_problem_by_id_or_code(pk)
        markdown = request.data.get('markdown', '')
        html = request.data.get('html', markdown)

        pkg.save_statement(p.code, markdown, html)
        p.description = html or markdown
        p.save(update_fields=['description'])

        return api_response({'message': 'Lưu đề bài thành công'})

class ProblemTestcasesAPI(APIView):
    def get(self, request, pk):
        p = get_problem_by_id_or_code(pk)
        tests = pkg.get_testcases(p.code)
        return api_response({'testcases': tests, 'total': len(tests)})

    def post(self, request, pk):
        p = get_problem_by_id_or_code(pk)
        tid = request.data.get('id') or f"{len(pkg.get_testcases(p.code)) + 1:02d}"
        in_data = request.data.get('input', '')
        out_data = request.data.get('output', '')
        points = float(request.data.get('points') or 10.0)

        pkg.save_testcase(p.code, tid, in_data, out_data, points)
        return api_response({'message': f'Đã lưu testcase {tid}', 'id': tid}, status_code=201)

class ProblemTestcaseDetailAPI(APIView):
    def delete(self, request, pk, tid):
        p = get_problem_by_id_or_code(pk)
        deleted = pkg.delete_testcase(p.code, tid)
        return api_response({'deleted': deleted, 'message': f'Đã xóa testcase {tid}'})

class ProblemTestcasesUploadAPI(APIView):
    def post(self, request, pk):
        p = get_problem_by_id_or_code(pk)
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return api_response(error={'message': 'Chưa chọn file zip để upload'}, status_code=400)

        try:
            count = pkg.import_zip_testcases(p.code, uploaded_file.read())
            return api_response({'imported': count, 'message': f'Đã giải nén và nhập {count} file test'})
        except Exception as e:
            return api_response(error={'message': f'Lỗi giải nén ZIP: {str(e)}'}, status_code=400)

class ProblemCheckerAPI(APIView):
    def get(self, request, pk):
        p = get_problem_by_id_or_code(pk)
        chk = pkg.get_checker(p.code)
        return api_response(chk)

    def post(self, request, pk):
        p = get_problem_by_id_or_code(pk)
        code = request.data.get('code', '')
        filename = request.data.get('filename', 'checker.cpp')
        pkg.save_checker(p.code, code, filename)
        return api_response({'message': 'Đã lưu checker'})

class ProblemValidatorAPI(APIView):
    def get(self, request, pk):
        p = get_problem_by_id_or_code(pk)
        val = pkg.get_validator(p.code)
        return api_response(val)

    def post(self, request, pk):
        p = get_problem_by_id_or_code(pk)
        code = request.data.get('code', '')
        filename = request.data.get('filename', 'validator.cpp')
        pkg.save_validator(p.code, code, filename)
        return api_response({'message': 'Đã lưu validator'})

class ProblemSolutionsAPI(APIView):
    def get(self, request, pk):
        p = get_problem_by_id_or_code(pk)
        sols = pkg.get_solutions(p.code)
        return api_response({'solutions': sols})

    def post(self, request, pk):
        p = get_problem_by_id_or_code(pk)
        code = request.data.get('code', '')
        filename = request.data.get('filename', 'official.py')
        pkg.save_solution(p.code, code, filename)
        return api_response({'message': f'Đã lưu solution {filename}'})

class ProblemSolutionsTestAPI(APIView):
    def post(self, request, pk):
        p = get_problem_by_id_or_code(pk)
        filename = request.data.get('filename', 'official.py')
        res = pkg.test_solution(p.code, filename)
        return api_response(res)

class ProblemPreviewAPI(APIView):
    def get(self, request, pk):
        p = get_problem_by_id_or_code(pk)
        stmt = pkg.get_statement(p.code)
        tests = pkg.get_testcases(p.code)
        return api_response({
            'code': p.code,
            'title': p.name,
            'time_limit': p.time_limit,
            'memory_limit': int(p.memory_limit / 1024),
            'points': p.points,
            'difficulty': p.difficulty,
            'html': stmt.get('html') or stmt.get('markdown'),
            'sample_tests': tests[:2]
        })

class ProblemPublishAPI(APIView):
    def post(self, request, pk):
        p = get_problem_by_id_or_code(pk)
        readiness = pkg.check_publish_readiness(p.code)
        if not readiness.get('ready'):
            return api_response(error={
                'message': 'Bài tập chưa đủ điều kiện publish!',
                'checklist': readiness.get('checklist')
            }, status_code=400)

        p.status = 'published'
        p.is_public = True
        p.save(update_fields=['status', 'is_public'])

        return api_response({
            'id': p.id,
            'code': p.code,
            'status': p.status,
            'message': f'Đã Publish bài tập {p.code} ra cộng đồng thành công!'
        })

class ProblemUnpublishAPI(APIView):
    def post(self, request, pk):
        p = get_problem_by_id_or_code(pk)
        p.status = 'draft'
        p.is_public = False
        p.save(update_fields=['status', 'is_public'])
        return api_response({'id': p.id, 'code': p.code, 'status': p.status, 'message': 'Đã chuyển bài tập về trạng thái Draft.'})
