import datetime
import os
from src.main.lambdas.utils.aws import trigger_sns_topic,put_item_dynamo,update_item_status_dynamo
from src.main.lambdas.utils.logs import logger
import urllib.parse
def puppy(args):
    if len(args) >= 1:
        
        query = 'puppy %s' % args['keywords']
        logger.info(query)

        message = {
            'query': query,
            'execution_id': args['execution_id']
        }

        try:
            trigger_sns_topic(os.environ['PUPPY_SNS'],message)
        except Exception as e:
            logger.error(str(e))
            update_item_status_dynamo(args['execution_id'],'puppy','failed')
        else:
            update_item_status_dynamo(args['execution_id'],'puppy','triggered')
        return args
    else:
        raise Exception('Not the correct number of arguments.')

def setup_puppy(args):
    now = datetime.datetime.now()
    execution_id = 'puppy_%s' % now.strftime('%m%d%Y%H%M%S%f')

    args['execution_id'] = execution_id

    status = {}
    status['puppy'] = {}
    status['puppy']['current_status'] = 'initiated'
    status['puppy']['execution_data'] = {}

    origin = urllib.parse.unquote(args['To'])
    to = urllib.parse.unquote(args['From'])

    put_item_dynamo(execution_id,status,origin,to)

    return args

feature_map = {
    'puppy': [setup_puppy,puppy]
}