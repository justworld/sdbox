# coding: utf-8
import os
import json
import uuid

from boto3.session import Session
from botocore.exceptions import ClientError
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient, DROP_OLDEST


class AWSIoTClient:
    """
    AWS IoT client
    base on https://github.com/aws-samples/aws-iot-elf
    RUN pip install awscli
    RUN aws configure set aws_access_key_id YOUR_AWS_ACCESS_KEY_ID # provide aws access key id
    RUN aws configure set aws_secret_access_key YOUR_AWS_SECRET_KEY # provide aws secret access key
    RUN curl -o rootCA.crt https://www.symantec.com/content/en/us/enterprise/verisign/roots/VeriSign-Class%203-Public-Primary-Certification-Authority-G5.pem
    """

    def __init__(self, region=None, profile_name=None, cfg_dir=None, thing_cfg_file=None):
        if not region:
            region = 'us-west-2'

        self.region = region
        self.profile_name = profile_name
        if not cfg_dir:
            cfg_dir = 'mstr'
        self.cfg_dir = os.getcwd() + '/' + cfg_dir + '/'

        if not thing_cfg_file:
            thing_cfg_file = 'things.json'

        self.things_file = self.cfg_dir + thing_cfg_file

        self.policy_name_key = "elf_policy"
        self.policy_arn_key = 'elf_policy_arn'
        self.root_cert = 'certs/root-CA.crt'
        self.aws_iot_mqtt_port = 8883

    def _get_iot_client(self):
        client = getattr(self, '_client', None)
        if not client:
            self._client = Session(region_name=self.region, profile_name=self.profile_name).client('iot')
        return self._client

    def _update_things_config(self, things):
        with open(self.things_file, "w") as fc_file:
            json.dump(things, fc_file, indent=2, separators=(',', ': '), sort_keys=True)

        self._things = things

    def _create_and_attach_policy(self, topic, thing_name, thing_cert_arn):
        # Create and attach to the principal/certificate the minimal action
        # privileges Thing policy that allows publish and subscribe
        tp = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Action": [
                    "iot:Connect",
                    "iot:Publish",
                    "iot:Receive",
                    "iot:Subscribe"
                ],
                "Resource": [
                    "arn:aws:iot:{0}:*:*".format(self.region)
                ]
            }]
        }

        client = self._get_iot_client()
        policy_name = 'policy-{0}'.format(thing_name)
        policy = json.dumps(tp)
        p = client.create_policy(
            policyName=policy_name,
            policyDocument=policy
        )
        client.attach_principal_policy(policyName=policy_name, principal=thing_cert_arn)
        return p['policyName'], p['policyArn']

    def _mqtt_client(self, thing_name):
        mqtt_clients = getattr(self, '_mqtt_clients', {})
        mqttc = mqtt_clients.get(thing_name)
        if not mqttc:
            mqttc = AWSIoTMQTTClient(clientID=uuid.uuid4().hex)

            t_name = self.cfg_dir + thing_name
            client = self._get_iot_client()
            endpoint = client.describe_endpoint(endpointType='iot:Data-ATS')

            mqttc.configureEndpoint(hostName=endpoint['endpointAddress'], portNumber=self.aws_iot_mqtt_port)
            mqttc.configureCredentials(CAFilePath=self.root_cert, KeyPath=t_name + ".prv",
                                       CertificatePath=t_name + ".pem")
            mqttc.configureAutoReconnectBackoffTime(1, 128, 20)
            mqttc.configureOfflinePublishQueueing(90, DROP_OLDEST)
            mqttc.configureDrainingFrequency(3)
            mqttc.configureConnectDisconnectTimeout(20)
            mqttc.configureMQTTOperationTimeout(5)

            mqtt_clients[thing_name] = mqttc
            self._mqtt_clients = mqtt_clients

        # mqttc.connect()  # keepalive default at 30 seconds
        return mqttc

    def get_things_config(self):
        things = getattr(self, '_things', {})
        if not things:
            if os.path.exists(self.things_file) and os.path.isfile(self.things_file):
                try:
                    with open(self.things_file, "r") as in_file:
                        things = json.load(in_file)

                    self._things = things
                except OSError as ose:
                    pass

        return things

    def create_things(self, names=None, count=None):
        """
        create thing
        :param names: [thing_name]
        :return:
        """
        if not names and not count:
            return

        if not names:
            # if names empty, use uuid as thing name
            names = [uuid.uuid4().hex for i in range(count)]

        client = self._get_iot_client()
        things = self.get_things_config()
        for t_name in names:
            # Create a Key and Certificate in the AWS IoT Service per Thing
            keys_cert = client.create_keys_and_certificate(setAsActive=True)

            # Create a named Thing in the AWS IoT Service
            client.create_thing(thingName=t_name)

            # Attach the previously created Certificate to the created Thing
            client.attach_thing_principal(thingName=t_name, principal=keys_cert['certificateArn'])

            things[t_name] = keys_cert

            # Save all the Key and Certificate files locally for future cleanup
            # ..could be added to Keyring later (https://github.com/jaraco/keyring)
            try:
                certname = self.cfg_dir + t_name + ".pem"
                public_key_file = self.cfg_dir + t_name + ".pub"
                private_key_file = self.cfg_dir + t_name + ".prv"
                with open(certname, "w") as pem_file:
                    pem_file.write(things[t_name]['certificatePem'])

                with open(public_key_file, "w") as pub_file:
                    pub_file.write(things[t_name]['keyPair']['PublicKey'])

                with open(private_key_file, "w") as prv_file:
                    prv_file.write(things[t_name]['keyPair']['PrivateKey'])

                self._update_things_config(things)
            except OSError as ose:
                # handle error
                pass

    def list_things(self, *args, **kwargs):
        client = self._get_iot_client()
        response = client.list_things(*args, **kwargs)
        return response['things']

    def delete_thing(self, thing_name, only_local=False):
        things = self.get_things_config()
        if not things:
            return

        thing = things.get(thing_name)
        if not thing:
            return

        if not only_local:
            client = self._get_iot_client()

            # First use the DetachPrincipalPolicy API to detach all policies.
            if self.policy_name_key in thing:
                try:
                    client.detach_principal_policy(policyName=thing[self.policy_name_key],
                                                   principal=thing['certificateArn'])

                    # Next, use the DeletePolicy API to delete the policy from the service
                    client.delete_policy(policyName=thing[self.policy_name_key])
                except ClientError as ce:
                    pass

            else:
                # Next, use the UpdateCertificate API to set the certificate to the INACTIVE status.
                try:
                    client.update_certificate(certificateId=thing['certificateId'], newStatus='INACTIVE')

                    # Next, use the DetachThingPrincipal API to detach the Certificate from the Thing.
                    client.detach_thing_principal(thingName=thing_name, principal=thing['certificateArn'])

                    # Last, use the DeleteCertificate API to delete each created Certificate.
                    client.delete_certificate(certificateId=thing['certificateId'])

                except ClientError as ce:
                    pass

                # Then, use the DeleteThing API to delete each created Thing
                client.delete_thing(thingName=thing_name)

        # delete the locally created files
        certname = self.cfg_dir + thing_name + ".pem"
        os.remove(certname)

        public_key_file = self.cfg_dir + thing_name + ".pub"
        os.remove(public_key_file)

        private_key_file = self.cfg_dir + thing_name + ".prv"
        os.remove(private_key_file)

        # Finally, update things config
        things.pop(thing_name, None)
        self._update_things_config(things)

    def delete_all(self):
        things = self.get_things_config()
        if not things:
            return

        names = list(things.keys())
        for thing_name in names:
            self.delete_thing(thing_name)

    def send_message(self, thing_name, topic, message, qos=0):
        things = self.get_things_config()
        if not things:
            return

        thing = things.get(thing_name)
        if not thing:
            return

        if self.policy_name_key not in thing.keys():
            policy_name, policy_arn = self._create_and_attach_policy(topic, thing_name, thing['certificateArn'])
            things[thing_name][self.policy_name_key] = policy_name
            things[thing_name][self.policy_arn_key] = policy_arn
            self._update_things_config(things)

        mqttc = self._mqtt_client(thing_name)
        topic = '{0}/{1}'.format(topic, thing_name)
        msg = {'msg': "{0}".format(message)}
        # publish a JSON equivalent of this Thing's message with a timestamp
        s = json.dumps(msg, separators=(', ', ': '))
        mqttc.connect()  # keepalive default at 30 seconds
        mqttc.publish(topic, s, qos)
        # Now disconnect the MQTT Client
        mqttc.disconnect()

    def subscribe(self, thing_name, topic, callback):
        things = self.get_things_config()
        if not things:
            return

        thing = things.get(thing_name)
        if not thing:
            return

        if self.policy_name_key not in thing.keys():
            policy_name, policy_arn = self._create_and_attach_policy(topic, thing_name, thing['certificateArn'])
            things[thing_name][self.policy_name_key] = policy_name
            things[thing_name][self.policy_arn_key] = policy_arn
            self._update_things_config(things)

        mqttc = self._mqtt_client(thing_name)
        mqttc.connect()  # keepalive default at 30 seconds
        mqttc.subscribe(topic, 1, callback)
        # keep connect until input something
        next = input()
        # Now disconnect the MQTT Client
        mqttc.disconnect()


if __name__ == '__main__':
    client = AWSIoTClient()

    # client.create_things(count=5)
    # client.delete_thing('9da8ed7bf06d43688a3f964194986921')
    # client.delete_thing('a2f54e95fc2f4de48d9a952e88b55a30')
    # print(client.get_things_config())
    # client.delete_all()
    # print(client.get_things_config())
    # print(client.list_things())
    client.send_message('fab819c708684154972fd36b037d8f59', 'test', 'hello,world')
    client.send_message('fab819c708684154972fd36b037d8f59', 'test', 'hello,world')
    client.subscribe('fab819c708684154972fd36b037d8f59', 'test', lambda c, u, m: print(json.loads(m.payload)))
