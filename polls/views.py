from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.core.urlresolvers import reverse
from django.utils import timezone
from polls.models import Choice, Poll, Voter
import datetime

# Create your views here.
class IndexView(generic.ListView):
     	template_name =  'polls/index.html'
     	context_object_name = 'latest_poll_list'
	
	def get_queryset(self):
		"""Return the last five published polls. (not including those set to be 
			published in the future).
		"""
		return Poll.objects.filter(
			pub_date__lte=timezone.now()
		).order_by('-pub_date')[:5]
    
class DetailView(generic.DetailView):
	model = Poll
	template_name = 'polls/detail.html'
	#context_object_name = 'voters'
	def get_queryset(self):
		"""
		Excludes any polls that aren't published yet. 
		"""
		return Poll.objects.filter(pub_date__lte=timezone.now())
	def get_context_data(self, **kwargs):
		context = super(DetailView, self).get_context_data(**kwargs)
		context['voters']=Voter.objects.all()
		return context
	
class ResultsView(generic.DetailView):
	model = Poll
	template_name = 'polls/results.html'

#def results(request, poll_id):
#	poll = get_object_or_404(Poll, pk=poll_id)
#	return render(request, 'polls/results.html', {'poll': poll})

def vote(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)

#Extract voter ID
	if not request.POST.get('voter'):
		return render(request, 'polls/detail.html',{
			'poll':p,
			'voters': Voter.objects.all(),
			'error_message':"You didn't select your name.",
		}) 
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
		pksd = request.POST.getlist('choice')  #get all the choices selected
	except (KeyError, Choice.DoesNotExist):
	# Redisplay the poll voting form
		return render(request, 'polls/detail.html', {
			'poll': p,
			'voters': Voter.objects.all(),
			'error_message': "You didn't select a choice.",
		})
	else:
		for pk in pksd:
			print pksd
			selected_choice = p.choice_set.get(id=pk)
			selected_choice.votes += 1
			v = Voter.objects.filter(voter_name__icontains=request.POST.get('voter'))
			selected_choice.voter.add(v[0])
			selected_choice.save()
	return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

def time_now(request):
	now = datetime.datetime.now()
	return render(request, 'polls/mytemplate.html',{'current_date': now})

#testing whether voter is working
def displayVoter(request):
	name = Voter.objects.get(id=1)
	return HttpResponse(name)

#Extract the meta-information

def display_meta(request):
	values = request.META.items()
	values.sort()
	html = []
	for k, v in values:
		html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
	return HttpResponse('<table>%s</table>' % '\n'.join(html))
