from opensearchpy import OpenSearch

host = [{'host': 'localhost', 'port': 9200}]

client = OpenSearch(
    hosts=host,
    http_compress=True,
    # http_auth=auth,
    use_ssl=False,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False
)
info = client.info()
print(f"Welcome to {info['version']['distribution']} {info['version']['number']}!")


index_name = 'python-test-index'
index_body = {
  'settings': {
    'index': {
      'number_of_shards': 4
    }
  }
}

response = client.indices.create(index_name, body=index_body)


document = {
  'title': 'Moneyball',
  'director': 'Bennett Miller',
  'year': '2011'
}

response = client.index(
    index = 'python-test-index',
    body = document,
    id = '1',
    refresh = True
)
