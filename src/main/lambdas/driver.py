from src.main.lambdas.utils.logs import logger
from src.main.lambdas.utils.orchestration import feature_map
import urllib.parse
def lambda_handler(event,context):
    logger.info(event)
    if event:
        if 'Body' in event:
            message_in = urllib.parse.unquote_plus(event['Body'].lower()).strip()
            message_in_break = message_in.split(' ',)
            if len(message_in_break) > 1:
                
                args = event

                args['command'] = message_in_break[0]
                args['keywords'] = message_in_break[1]
                
                if args['command'] in feature_map:
                    try:
                        for function in feature_map[args['command']]:
                            logger.info(args)
                            args = function(args)
                    except Exception as e:
                        logger.error(str(e))
                else:
                    logger.error('Command not in feature map.')
            else:
                logger.error('Message misconfigured.')
        else:
            logger.error('No body in event: %s' % event)
    else:
        logger.info('No event present.')