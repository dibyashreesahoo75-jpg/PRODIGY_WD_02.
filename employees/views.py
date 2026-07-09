from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .models import Employee
from .forms import EmployeeForm, RegisterForm


# Home Page
@login_required
def home(request):
    query = request.GET.get('q')

    employees = Employee.objects.all().order_by('-id')

    if query:
        employees = employees.filter(name__icontains=query)

    total_employees = Employee.objects.count()
    total_departments = Employee.objects.values('department').distinct().count()

    paginator = Paginator(employees, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'employees': page_obj,
        'query': query,
        'total_employees': total_employees,
        'total_departments': total_departments,
        'page_obj': page_obj,
    }

    return render(request, 'employees/home.html', context)


# Add Employee
@login_required
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EmployeeForm()

    return render(request, 'employees/add_employee.html', {'form': form})


# Edit Employee
@login_required
def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'employees/edit_employee.html', {'form': form})


# Delete Employee
@login_required
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        employee.delete()
        return redirect('home')

    return render(request, 'employees/delete_employee.html', {'employee': employee})


# Register User
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'employees/register.html', {'form': form})