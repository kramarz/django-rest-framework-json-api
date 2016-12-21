from django.core.urlresolvers import reverse

import pytest

from example.tests.utils import load_json

pytestmark = pytest.mark.django_db


def test_sparse_fieldset_ordered_dict_error(multiple_entries, client):
    entry = multiple_entries[0]
    expected = {
        "data": [
            {
                "type": "posts",
                "id": "1",
                "attributes":
                    {
                        "headline": entry.headline,
                    },
                "meta": {
                    "bodyFormat": "text"
                },
                "relationships":
                    {
                        "blog": {
                            "data": {"type": "blogs", "id": str(entry.blog.id)}
                        },
                    }
            }],
        "links": {
            "first": "http://testserver/entries?fields%5Bentries%5D=blog%2Cheadline&page=1",
            "last": "http://testserver/entries?fields%5Bentries%5D=blog%2Cheadline&page=2",
            "next": "http://testserver/entries?fields%5Bentries%5D=blog%2Cheadline&page=2",
            "prev": None,
        },
        "meta":
            {
                "pagination":
                    {
                        "page": 1,
                        "pages": 2,
                        "count": 2
                    }
            }
    }
    base_url = reverse('entry-list')
    querystring = '?fields[entries]=blog,headline'
    response = client.get(base_url + querystring)  # RuntimeError: OrderedDict mutated during iteration
    parsed_content = load_json(response.content)

    assert expected == parsed_content
