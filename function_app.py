import logging
import time
import azure.functions as func
import azure.durable_functions as df

app = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route='HttpStart')
@app.durable_client_input(client_name='client')
async def http_start(req: func.HttpRequest, client: df.DurableOrchestrationClient):
    '''HTTP trigger that starts the Durable orchestration (v2 decorators).'''
    instance_id = await client.start_new('Orchestrator')
    logging.info(f'Started orchestration with ID = {instance_id}')
    return client.create_check_status_response(req, instance_id)

@app.orchestration_trigger(context_name='context')
def orchestrator_function(context: df.DurableOrchestrationContext):
    '''Orchestrator: call Activity1 then Activity2 sequentially.'''
    name1 = yield context.call_activity(activity1, 'Activity1')
    name2 = yield context.call_activity(activity2, 'Activity2')
    return {'activity1': name1, 'activity2': name2}

@app.activity_trigger(input_name='name')
def activity1(name: str) -> str:
    '''Activity 1: wait 15 seconds and print/log its name.'''
    logging.info(f'Activity triggered: {name}')
    print(name)
    time.sleep(15)
    logging.info(f'Activity completed: {name}')
    return name

@app.activity_trigger(input_name='name')
def activity2(name: str) -> str:
    '''Activity 2: wait 15 seconds and print/log its name.'''
    logging.info(f'Activity triggered: {name}')
    print(name)
    time.sleep(15)
    logging.info(f'Activity completed: {name}')
    return name
