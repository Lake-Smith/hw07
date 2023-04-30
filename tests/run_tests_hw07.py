import utils
utils.modify_system_path()


import unittest

# import the tests you want to run:
from tests.test_bookmarks import TestBookmarkListEndpoint
from tests.test_followers import TestFollowerListEndpoint
from tests.test_following import TestFollowingListEndpoint
from tests.test_posts import TestPostListEndpoint, TestPostDetailEndpoint
from tests.test_profile import TestProfileEndpoint
from tests.test_stories import TestStoryListEndpoint
from tests.test_suggestions import TestSuggestionsEndpoint

import sys
if __name__ == '__main__':
    verbosity_level = 1
    args = sys.argv
    # print(args)
    custom = False
    if len(args) > 1 and args[1] not in ['-v', '--verbose']:
        custom = True

    for arg in args:
        if arg in ['-v', '--verbose']:
            verbosity_level = 2

    if custom:
        print('running the selected test(s)...')
        unittest.main()
    else:
        print('running all of the hw 7 tests...')
        suite = unittest.TestSuite()
        suite.addTests([

            # Bookmark GET (List) Tests:
            TestBookmarkListEndpoint('test_bookmarks_get_check_if_query_correct'),
            TestBookmarkListEndpoint('test_bookmarks_get_check_if_data_structure_correct'),

            # Followers GET (List) Tests:
            TestFollowerListEndpoint('test_followers_get'),                       
            TestFollowerListEndpoint('test_follower_get_check_data_structure'),
            
            # Following GET (List) Tests:
            TestFollowingListEndpoint('test_following_get_check_data_structure'),   
            TestFollowingListEndpoint('test_following_get_check_if_query_correct'),
            
            # Posts GET (List) Tests:
            TestPostListEndpoint('test_posts_get_defaults_to_20'),              # get (list view)
            TestPostListEndpoint('test_posts_get_has_required_data'),           # get (list view)
            TestPostListEndpoint('test_posts_get_limit_argument'),              # get (list view)
            TestPostListEndpoint('test_posts_get_bad_limit_argument_handled'),  # get (list view)
            TestPostListEndpoint('test_posts_get_is_authorized'),   

            # Posts GET (Detail) Tests:
            TestPostDetailEndpoint('test_post_get'),                            # get (individual)
            TestPostDetailEndpoint('test_post_get_invalid_id_404'),             # get (individual) 
            TestPostDetailEndpoint('test_post_get_id_does_not_exist_404'),      # get (individual)
            TestPostDetailEndpoint('test_post_get_unauthorized_id_404'),

            # Profile GET Tests:
            TestProfileEndpoint('test_profile_get_check_if_query_correct'),

            # Stories GET (List) Tests:
            TestStoryListEndpoint('test_stories_get_check_if_query_correct'),                       
            TestStoryListEndpoint('test_stories_get_check_data_structure'),

            # Suggestions GET (List) Tests:
            TestSuggestionsEndpoint('test_suggestions_get_check_if_query_correct'),
            TestSuggestionsEndpoint('test_suggestions_get_check_if_data_structure_correct')
                
        ])
        unittest.TextTestRunner(verbosity=verbosity_level).run(suite)

# Note: to run on command line (from the tests directory): 
# python run_tests_hw07.py -v

# To run a specific test:
# python run_tests_hw07.py TestPostListEndpoint.test_posts_get_defaults_to_20 -v
