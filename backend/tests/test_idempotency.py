from unittest.mock import MagicMock
from botocore.exceptions import ClientError

def test_duplicate_transaction_skipped():
    # giả lập DynamoDB conditional failure
    error_response = {
        "Error": {"Code": "ConditionalCheckFailedException", "Message": "Duplicate"}
    }
    raise_exc = ClientError(error_response, "PutItem")

    table = MagicMock()
    table.put_item.side_effect = raise_exc

    try:
        table.put_item(
            Item={"transaction_id": "tx-1"},
            ConditionExpression="attribute_not_exists(transaction_id)",
        )
    except ClientError as e:
        assert e.response["Error"]["Code"] == "ConditionalCheckFailedException"
