# Portfolio/SIPA/courses/views.py

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Competency, CourseCompetency
from .forms import CourseForm, CompetencyForm, CourseCompetencyFormSet

def home(request):
    return render(request, 'home.html')

def data_science(request):
    codes = Course.objects.values_list('code', flat=True).distinct()
    names = Course.objects.values_list('name', flat=True).distinct()
    hours = Course.objects.values_list('hours', flat=True).distinct()
    credits = Course.objects.values_list('credits', flat=True).distinct()
    semesters = Course.objects.values_list('semester', flat=True).distinct()
    majors = Course.objects.values_list('major', flat=True).distinct()
    competencies = Competency.objects.all()

    context = {
        'codes': codes,
        'names': names,
        'hours': hours,
        'credits': credits,
        'semesters': semesters,
        'majors': majors,
        'competencies': competencies,
        'courses': Course.objects.all(),
    }
    return render(request, 'courses/data_science.html', context)

def filter_courses(request):
    courses = Course.objects.all()

    if request.GET.get('code'):
        courses = courses.filter(code=request.GET['code'])
    if request.GET.get('name'):
        courses = courses.filter(name=request.GET['name'])
    if request.GET.get('hours'):
        courses = courses.filter(hours=request.GET['hours'])
    if request.GET.get('credits'):
        courses = courses.filter(credits=request.GET['credits'])
    if request.GET.get('semester'):
        courses = courses.filter(semester=request.GET['semester'])
    if request.GET.get('major'):
        courses = courses.filter(major=request.GET['major'])
    if request.GET.get('competency'):
        courses = courses.filter(coursecompetency__competency__id=request.GET['competency']).distinct()

    context = {'courses': courses}
    return render(request, 'courses/course_table.html', context)


def chart_data(request):
    courses = Course.objects.all()

    if request.GET.get('code'):
        courses = courses.filter(code=request.GET['code'])
    if request.GET.get('name'):
        courses = courses.filter(name=request.GET['name'])
    if request.GET.get('hours'):
        courses = courses.filter(hours=request.GET['hours'])
    if request.GET.get('credits'):
        courses = courses.filter(credits=request.GET['credits'])
    if request.GET.get('semester'):
        courses = courses.filter(semester=request.GET['semester'])
    if request.GET.get('major'):
        courses = courses.filter(major=request.GET['major'])
    if request.GET.get('competency'):
        courses = courses.filter(coursecompetency__competency__id=request.GET['competency']).distinct()

    competencies_count = {}
    for course in courses:
        for cc in course.coursecompetency_set.all():
            if cc.competency.name in competencies_count:
                competencies_count[cc.competency.name] += cc.occurrence
            else:
                competencies_count[cc.competency.name] = cc.occurrence

    data = {
        'labels': list(competencies_count.keys()),
        'values': list(competencies_count.values()),
    }
    return JsonResponse(data)


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    competencies = CourseCompetency.objects.filter(course=course)
    return render(request, 'courses/course_detail.html', {'course': course, 'competencies': competencies})

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        formset = CourseCompetencyFormSet(request.POST, instance=form.instance)
        if form.is_valid() and formset.is_valid():
            course = form.save()
            formset.save()
            return redirect('home')
    else:
        form = CourseForm()
        formset = CourseCompetencyFormSet(instance=form.instance)
    return render(request, 'courses/add_course.html', {'form': form, 'formset': formset})

def add_competency(request):
    if request.method == 'POST':
        form = CompetencyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CompetencyForm()
    return render(request, 'courses/add_competency.html', {'form': form})
