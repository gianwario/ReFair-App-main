from REFAIR import getDomain

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
