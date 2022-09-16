import mock
import main


mock_context = mock.Mock()
mock_context.event_id = '617187464135194'
mock_context.timestamp = '2019-07-15T22:09:03.761Z'
mock_context.resource = {
    'name': 'projects/my-project/topics/my-topic',
    'service': 'pubsub.googleapis.com',
    'type': 'type.googleapis.com/google.pubsub.v1.PubsubMessage',
}



def test_bucket(capsys):
    data = {"image":"adrian.jpg","bucket":"soaproyecto1-input"}
    # Call tested function
    main.main(data, mock_context)
    out, err = capsys.readouterr()
    assert "{'anger': 'UNLIKELY', 'joy': 'VERY_UNLIKELY', 'sorrow': 'VERY_UNLIKELY', 'surprise': 'VERY_UNLIKELY'}" in out