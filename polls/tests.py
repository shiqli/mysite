import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from polls.models import Poll

class PollMethodTests(TestCase):

	def test_was_published_recently_with_future_poll(self):
		"""
		was_published_recently() should return False for polls whose pub_date is in the future
		"""

		future_poll = Poll(pub_date=timezone.now()+datetime.timedelta(days=30))
		self.assertEqual(future_poll.was_published_recently(), False)


	def test_was_published_recently_with_old_poll(self):
		"""
		was_published_recently() should return False for polls whose pub_date is in the future
		"""

		old_poll = Poll(pub_date=timezone.now()-datetime.timedelta(days=30))
		self.assertEqual(old_poll.was_published_recently(), False)

	def test_was_published_recently_with_future_poll(self):
		"""
		was_published_recently() should return False for polls whose pub_date is in the future
		"""

		recent_poll = Poll(pub_date=timezone.now()-datetime.timedelta(hours=1))
		self.assertEqual(recent_poll.was_published_recently(), True)


# Create your tests here.i
def create_poll(question, days):
	"""
	Creates a poll with the given 'question' published the given number of 'days' offset to now (negative for polls published inthe past, positive for polls that have yet to be published).
	"""
	return Poll.objects.create(question=question,
		pub_date=timezone.now()+datetime.timedelta(days=days))

class PollViewTest(TestCase):
	def test_index_view_with_no_polls(self):
		"""
		If no polls exist, an appropriate message should be displayed 
		"""

		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "NO polls are available.")
		self.assertQuerysetEqual(response.context['latest_poll_list'],[])

	def test_index_view_with_a_past_poll(self):
		"""
		Polls with a pub_date in the past should be displayed on the index page
		"""
		create_poll(question="Past poll.", days =-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_poll_list'],
			['<Poll: Past poll.>']
		)

	def test_index_view_with_a_future_poll(self):
		"""
		Polls with a pub_date in the future should not be displayed on the index page
		"""
		create_poll(question="Future poll.", days =30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_poll_list'],
			[]
		)

	def test_index_view_with_future_past_poll(self):
		"""
		Polls with a pub_date in the past and in the future should be displayed on the index page
		"""
		create_poll(question="Past poll.", days =-30)
		create_poll(question="Future poll.", days =30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_poll_list'],
			['<Poll: Past poll.>']
		)

	def test_index_view_with_two_past_poll(self):
		"""
		Polls with a pub_date in the past and in the future should be displayed on the index page
		"""
		create_poll(question="Past poll 1.", days =-30)
		create_poll(question="Past poll 2.", days =-10)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_poll_list'],
			['<Poll: Past poll 2.>','<Poll: Past poll 1.>']
		)

class PollIndexDetailTests(TestCase):
	def test_detail_view_with_a_future_poll(self):
		"""
		The detail view of a poll with a pub_date in the future should return 404 not found
		"""
		future_poll = create_poll(question='Future Poll.', days = 5)
		response = self.client.get(reverse('polls:detail', args=(future_poll.id,)))
		self.assertEqual(response.status_code, 404)

	def test_detail_view_with_a_past_poll(self):
		
		"""
		The detail view of a poll with a pub_date in the past should display the poll's question
		"""
		past_poll = create_poll(question='Past Poll.', days =-5)
		response = self.client.get(reverse('polls:detail', args=(past_poll.id,)))
		self.assertContains(response, past_poll.question, status_code=200)
