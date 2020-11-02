# Imports the Google Cloud client library
from google.cloud import language_v1
from pprint import pprint

# Instantiates a client
client = language_v1.LanguageServiceClient()

# The text to analyze
text = u"Hey excelify can you please add 23 to columns A and B"
document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

# Detects the sentiment of the text
sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
response = client.analyze_entities(
     document=document,
     encoding_type='UTF32',
)


result = []
for entity in response.entities:
    temp = "name: " + str(entity.name) + " | type_: " + str(entity.type_ )
    result.append(temp)
    print("name: ", entity.name, " | type_: ", entity.type_)
    print("="*50)
    # pprint(entity)
    # print('=' * 20)
    # print('         name: {0}'.format(entity.name))
    # print('         type: {}'.format(language_v1.Entity.Type(entity.type).name))
    # print('     metadata: {0}'.format(entity.metadata))
    # print('     salience: {0}'.format(entity.salience))
# 
response = client.analyze_syntax(request = {'document': document, 'encoding_type': 'UTF32'})
print("=" * 50)
print('\n')
print('Sytax')
# Loop through tokens returned from the API
i = 0
for token in response.tokens:
    # temp = result[i]
    # i = i + 1
    # pprint(token)
    print("name:", token.text.content)
    print('header_token_label:', token.dependency_edge.label)
    print('part of speech:',token.part_of_speech)
    # dependency_edge = token.dependency_edge
    # print(u"Head token index: {}".format(dependency_edge.head_token_index))
    # print(
    # u"Label: {}".format(language_v1.DependencyEdge.Label(dependency_edge.label).name)
    # )
    print("="*50)
    print("")
    # pprint("name: %s | dependency edge: %s | part_of_speech: %s", token.text, token.dependency_edge, token.part_of_speech.tag)