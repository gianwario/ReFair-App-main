import pytest
from REFAIR import getDomain, getMLTask

class TestGetDomain:

    def test_get_domain_1(self):
        user_story = 'As a dermatologist, I want to apply feature selection ' + \
        'to analyze patient data and identify the most important features ' + \
        'related to skin disease, so that I can better diagnose and treat patients.'

        prediction = getDomain(user_story)

        assert prediction == 'Dermatology'

    def test_get_domain_2(self):
        user_story = 'As a social network researcher, I want to use narrative ' + \
        'understanding to analyze and model network structure and dynamics over ' + \
        'time, so that I can better understand and predict social network behavior ' + \
        'and evolution.'

        prediction = getDomain(user_story)

        assert prediction == 'Social Networks'

    def test_get_domain_3(self):
        user_story = 'As a news analyst, I want to use RNN architecture to ' + \
        'analyze news data over time, so that we can identify trends and ' + \
        'patterns in news relevance and design better news recommendation systems.'

        prediction = getDomain(user_story)

        assert prediction == 'News'

class TestGetMLTask:

    def test_get_ml_task_1(self):
        user_story = 'As a plant scientist, I want to use cluster analysis ' + \
        'to group plants based on their genetic and morphological characteristics, ' + \
        'so that I can better understand plant evolution and taxonomy.'
        domain = 'plant science'

        prediction = getMLTask(user_story, domain)

        assert prediction == ['clustering']

    def test_get_ml_task_2(self):
        user_story = 'As a healthcare provider, I want to use neural network hardware to ' + \
        'analyze medical data and predict disease outcomes and treatment effectiveness, so ' + \
        'that I can provide better healthcare services to patients.'
        domain = 'health'

        prediction = getMLTask(user_story, domain)

        assert prediction == ['classification', 'regression']

    def test_get_ml_task_3(self):
        user_story = 'As a sports broadcaster, I want to use hybrid machine translation ' + \
        'to translate and adapt sports commentary and analysis for international audiences ' + \
        'and markets to improve the engagement and enjoyment of sports fans worldwide.'
        domain = 'sports'

        prediction = getMLTask(user_story, domain)

        assert prediction == []

    @pytest.mark.skip(reason="The 'domains-task-mapping.csv' file contains duplicate tasks for " + \
                      "multiple domains. It needs to be cleaned to ensure unique task entries for " + \
                      "each domain. After cleaning, this test should pass.")
    def test_get_ml_task_4(self):
        user_story = 'As a linguist, I want to use sentiment analysis to analyze public ' + \
        'perception of language usage, to understand public perception and inform language ' + \
        'education and policy.'
        domain = 'linguistics'

        prediction = getMLTask(user_story, domain)

        assert prediction == ['sentiment analysis']
