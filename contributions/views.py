from django.db.models import Sum, Count
from django.views.generic import TemplateView
from contributions.models import Prop, Contribution


class IndexView(TemplateView):
    # tell our view which template to use
    template_name = "contributions/index.html"

    def get_context_data(self, **kwargs):
        # grab our context, so we can add to it
        context = super(IndexView, self).get_context_data(**kwargs)
        # get all of the props
        props = Prop.objects.all()
        # set up an empty data dictionary
        data = []
        # loop through all the props, and grab their totals
        for i in props:
            # grab the IDs of all the commitees that support the prop
            support_committees = i.campaign_set.filter(position='Support')\
                                    .values_list('committee_id', flat=True)
            # And all the committees that oppose it
            oppose_committees = i.campaign_set.filter(position='Oppose')\
                                    .values_list('committee_id', flat=True)
            # Then use those committee IDs to filter on the contributions
            # that either support or oppose the proposition.
            # Use the Django aggregate method to add them all up.
            data.append({
                'prop': i.name,
                'support': Contribution.objects.filter(committee_id__in=support_committees)\
                                .aggregate(sum=Sum('amount'))['sum'] or 0,
                'oppose': Contribution.objects.filter(committee_id__in=oppose_committees)\
                                .aggregate(sum=Sum('amount'))['sum'] or 0,
            })
        # put all of the values in a single list
        # so we can easily grab the max
        all_vals = []
        for i in data:
            all_vals.append(i['support'])
            all_vals.append(i['oppose'])

        # Here we can get a list of all of the unique contributor names
        # along with their total contributions
        contributors = Contribution.objects.values('clean_name')\
                    .annotate(contribs=Sum('amount')).order_by('-contribs')


        context['contributors'] = enumerate(contributors[0:11], start=1)
        context['max_value'] = max(all_vals)
        context['summary_data'] = data

# by committee
        contributors3 = Contribution.objects.values('clean_name', 'committee')\
            .annotate(contribs=Sum('amount')).order_by('-contribs')
                    

        context['contributors3'] = enumerate(contributors3[0:10], start=1)
        context['max_value'] = max(all_vals)
        context['summary_data'] = data

# 11-20

        contributors2 = Contribution.objects.values('clean_name')\
                    .annotate(contribs=Sum('amount')).order_by('-contribs')

        context['contributors2'] = enumerate(contributors2[11:20], start=12)
        context['max_value'] = max(all_vals)
        context['summary_data'] = data
        return context