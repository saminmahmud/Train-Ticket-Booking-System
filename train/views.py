from django.shortcuts import render,redirect,  get_object_or_404
from django.urls import reverse_lazy
from .models import Train, Seat,Review, Schedule
from django.views.generic import DetailView,FormView, UpdateView , DeleteView, TemplateView
from .forms import ReviewForm, AddTrainForm, Edit_scheduleForm, AddScheduleForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@method_decorator(login_required, name='dispatch')
class buy_ticket(DetailView):
    model = Train
    pk_url_kwarg = 'id' #train id eta
    template_name = 'buy_ticket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        train_id = self.kwargs.get('id')
        train = get_object_or_404(Train, pk=train_id)
        seats = Seat.objects.filter(train=train)
        context['train'] = train
        context['seats'] = seats

        trainnn = Review.objects.filter(train=train)
       
        comments = train.review.all()
        comment_form = ReviewForm()
        context['comments'] = comments
        context['comment_form'] = comment_form

        return context
    
    def post(self, request, *args, **kwargs):
        comment_form = ReviewForm(data=self.request.POST)
        train = self.get_object() 
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.train = train  
            new_comment.save()
        return self.get(request, *args, **kwargs)
    
    
@login_required
def buy(request, tid, sid):
    train = Train.objects.get(pk=tid)
    price = train.price
    account = request.user.account
    initial_balance = account.balance

    if initial_balance >= price:  
        new_balance = initial_balance - price # buy korar por balance
        account.balance = new_balance
        account.save(update_fields=['balance'])

        # seat = Seat.objects.get(pk=sid, train=train)
        seat = get_object_or_404(Seat, pk=sid, train=train, active=False)
        print(f"seat e click korechi: {seat}")
        print(f"train ta holo: {train}")
        seat.active = True
        seat.save(update_fields=['active'])

        messages.success(request, 'Ticket bought successfully😀')

        return redirect("buy_ticket", id=tid)
    else:
        messages.success(request, 'Opps! Insufficient Balance😥')
        return redirect("buy_ticket", id=tid)



@login_required
def addTrain(request):
    if request.method == 'POST':
        form = AddTrainForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get('image')
            train_name = form.cleaned_data.get('train_name')
            start_station = form.cleaned_data.get('start_station')
            end_station = form.cleaned_data.get('end_station')
            price = form.cleaned_data.get('price')
            total_number_of_seats = form.cleaned_data.get('total_number_of_seats')
            train_date = form.cleaned_data.get('train_date')

            print(f"{train_name} - {start_station} -{end_station} -{price} -{total_number_of_seats} -{train_date} --------")

            train = Train.objects.create(
                image = image,
                name = train_name,
                start_station = start_station,
                end_station = end_station,
                price = price,
            )
            print(train)

            for num in range(1, total_number_of_seats + 1):
                # print(num)
                seat = Seat.objects.create(
                   train = train, 
                   seat_number = num,
                   active = False,
                )

            schedule = Schedule.objects.create(
                train = train,
                train_date = train_date,
            )

            messages.success(request, 'Train Added successfully😀')
            return redirect('home')
    else:
        form = AddTrainForm()
    return render(request, 'add_train.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class EditScheduleView(UpdateView):
    model = Schedule
    form_class = Edit_scheduleForm
    template_name = 'edit_schedule.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('home')


def add_schedule(request, id):
    if request.method == 'POST':
        form = AddScheduleForm(request.POST)
        if form.is_valid():
            train = Train.objects.get(pk=id)
            train_date = form.cleaned_data.get('train_date')

            schedule = Schedule.objects.create(
                train = train,
                train_date = train_date,
            )
            messages.success(request, 'Schedule Added successfully😀')
            # form.save()
            return redirect('home') 
    else:
        form = AddScheduleForm()
    return render(request, 'add_schedule.html', {'form': form})

    