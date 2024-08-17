import os
from twilio.rest import Client

account_sid = 'ACd59de4b7ea746ef5cbf1e68d7087ef19'
auth_token = '87c4c5069b3a671e72e462b48689d1d3'

client = Client(account_sid, auth_token)

from_whatsapp_number = 'whatsapp:+14155238886'
to_whatsapp_number = 'whatsapp:+61431515817'

client.messages.create(body = 'Hi',
                       from_ = from_whatsapp_number,
                       to = to_whatsapp_number)