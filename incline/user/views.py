from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from numpy import timedelta64
from sqlalchemy import null #login was successful! etc
from .models import Contract, ContractProgress
import datetime
import time
#from .forms import SearchSubmissions #should probably be in .forms

def help(request):
    return render(request, 'user/help.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
            # Redirect to a success page.
        else:
            messages.success(request, ("1"))
            return redirect('login')
            #invalid login
    else:
        return render(request, 'user/login.html', {})

def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        user = User.objects.filter(username = username).first()
        if user is None:
            user = User.objects.filter(email = email).first()
            if user is None:
                if username == "":
                    messages.success(request, ("Username not found."))
                    return redirect('register')
                if email == "":
                    messages.success(request, ("Email not found."))
                    return redirect('register')
                if password == "":
                    messages.success(request, ("Password not found."))
                    return redirect('register')
                user = User.objects.create_user(username, email, password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.success(request, ("Unable to register user.")) 
                    return redirect('register')
            else:
                messages.success(request, ("Email already taken.")) #probably a better way to do this than nesting if statements
                return redirect('register')
        else:
            messages.success(request, ("Username already taken."))
            return redirect('register')
    else:
        return render(request, 'user/register.html', {})

def logout_user(request):
    logout(request)
    return redirect('login')

def contracts(request, contractnumber): #contractnumber is the contract in the url
    ContractProgress.objects.all().order_by('-date')
    user_contracts = Contract.objects.filter(user = request.user)
    ref2 = Contract.objects.filter(referee2 = request.user)
    ref = Contract.objects.filter(referee = request.user)
    ssub_id = 0
    submissions = [0]
    #return HttpResponse(ref2.aim)
    if contractnumber == 0:
        return render(request, 'user/contracts.html', {'user_contracts': user_contracts, 'contractnumber': contractnumber, 'submissions': submissions, 'ssub_id': ssub_id, 'referee_cont': ref, 'referee2_cont': ref2})
    else:
        try:
            contract = Contract.objects.get(id=contractnumber)
            contract_end = 1#(int(contract.end_date) - int(datetime.now().date()))
            now = datetime.datetime.today()
        except:
            return HttpResponse("404")

    contract_finished = False
    date_until_end = contract.end_date-datetime.timedelta(seconds=time.time())
    if int(date_until_end.strftime("%Y"))-1970 <= 0:
        if int(date_until_end.strftime("%m")) <= 0:
            if int(date_until_end.strftime("%d")) <= 0:
                contract_finished = True

    #return HttpResponse(str(contract.end_date)+"    "+str(contract.vote_deadline)+"    "+str(contract.end_date-contract.vote_deadline)+" and "+str(date_until_end))

    def UpdateDict():
        contract = Contract.objects.get(id=contractnumber)
        submissions = ContractProgress.objects.filter(contract = contract)
        sub_date_array = submissions.values_list('date', flat=True)

        min_date = 999999999
        max_date = 0
        sub_date = 0
        sub_for = [] #submissions formatted
        date_tally = []
        date_labels = []
        min_date_unform = 0
        max_date_unform = 0
        date_range_unform = 0
        sub_missed = 0

        for sub_date in sub_date_array:
            comp_int = int(str(sub_date.strftime("%Y"))+str(sub_date.strftime("%m"))+str(sub_date.strftime("%d")))
            dt_string = str(sub_date.strftime("%Y"))+"."+str(sub_date.strftime("%m"))+"."+str(sub_date.strftime("%d"))
            if min_date > comp_int:
                min_date = comp_int
                min_date_unform = sub_date
            if max_date < comp_int:
                max_date = comp_int
                max_date_unform = sub_date
            sub_for.append(str(sub_date.strftime("%Y"))+"."+str(sub_date.strftime("%m"))+"."+str(sub_date.strftime("%d")))
        sub_for.sort()
        date_range = max_date-min_date

        try:
            date_range_unform = (max_date_unform - min_date_unform).days
            sub_missed = date_range_unform % contract.sub_freq
            date_range_unform -= sub_missed
        except:
            pass



        date_labels = []
        date_tally = [0]*13
        if date_range < 1300: #12 months
            date_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            c = 0 #reset to be used as counter
            for date in sub_for:
                date_tally[int(date.split('.')[1])-1] += 1 #add one to the second field when split by . i.e. to the month of the submission
            c = (min_date - (min_date//10000)*10000)//100 #the month of the first submission e.g. 6
            for counter in range(c-1):
                date_tally.append(date_tally.pop(0))
                date_labels.append(date_labels.pop(0)) #e.g. if the first submission is 2022.04.23 then ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']
        else: #over 12 months
            c = min_date//10000 #the year of the first submission e.g. 2016
            for i in range(12):
                date_labels.append(str(c+i))
            for date in sub_for:
                date_tally[int(date.split('.')[0])-c] += 1 #add one to the first field when split by . i.e. to the year of the submission

        #return HttpResponse(str(sub_for) + " range = " + str(max_date-min_date) + " " + str(date_labels) + " " + str(date_tally))
        testdata = "for i in range(int(a))"
        render_dict = {'user_contracts': user_contracts, 'contractnumber': contractnumber, 'submissions': submissions, 'sub_date': sub_date, 'ssub_id': ssub_id, 'date_tally': date_tally, 'date_labels': date_labels, 'referee_cont': ref, 'referee2_cont': ref2, 'cont': contract, 'contract_end': contract_end, 'now': now, 'contract_finished': contract_finished, 'date_range_un': date_range_unform, 'sub_missed': sub_missed, 'testdata': testdata}
        return render_dict

    if request.method == "POST":
        submit = request.POST['submit']
        if submit == "1":
            try:
                description = request.POST['description']
                notes = request.POST['notes']
                date = request.POST['date']
                try:
                    file = request.FILES['file'] 
                except:
                    file = ""
                try:
                    if str(description) == "":
                        messages.success(request, ("f1_fill_error"))
                        return render(request, 'user/contracts.html', UpdateDict())
                    elif str(date) == "":
                        messages.success(request, ("f1_fill_error"))
                        return render(request, 'user/contracts.html', UpdateDict())
                except:
                    pass
            except:
                messages.success(request, ("f1_fill_error"))
                return render(request, 'user/contracts.html', UpdateDict())
            else:
                try:
                    ContractProgress.objects.create_progress(contract, description, notes, date, file) ##CONTRACT PROGRESS AFTER UPDATEEEEEEEEEEEEEEEEEEEE
                except:
                    messages.success(request, ("f1_invalid_error"))
                else:
                    return render(request, 'user/contracts.html', UpdateDict())
        elif submit == "2":
            try:
                ssub_id = request.POST['ssub_id']
                ssub_id = int(ssub_id)
                if ssub_id == 0:
                    messages.success(request, ("f2_error"))
            except:
                messages.success(request, ("f2_error"))
            else:
                return render(request, 'user/contracts.html', UpdateDict())
        else: #submit == 3
            try:
                vote = request.POST['vote']
            except:
                messages.success(request, ("f3_error"))
                return render(request, 'user/contracts.html', UpdateDict())
            else:
                return render(request, 'user/contracts.html', UpdateDict())
    else:
        return render(request, 'user/contracts.html', UpdateDict())

def new_contract(request):
    if request.method == "POST":
        submit = request.POST['submit']
        if submit == "1":
            try:
                description = request.POST['description']
                notes = request.POST['notes']
                date = request.POST['date']
            except:
                pass
    return render(request, 'user/new_contract.html', {})