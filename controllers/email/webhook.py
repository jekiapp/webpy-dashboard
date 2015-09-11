import web,hashlib,hmac,json
from core.model import model as m

# info@radiaranai.com
class webhook:
	url = 'https://app.radiaranai.com/email/webhook/hook/'
	key = 'UqQTSjCW1O5ptKDz5_3qAA'
	db = m()
	def hook(self,data):
		if not data and not self.auth(data): return
		try:
			events = json.loads(data['mandrill_events'])
			for event in events:
				if event['event']=='inbound':
					self.inbound(event['msg'],event['ts'])
		except Exception as e:
			self.db.query("insert into log values(NULL,'"+self.db.escape(e)+"',now())")
	
	def inbound(self,msg,ts):
		from_email = msg['from_email']
		from_name = msg['from_name'] if 'from_name' in msg else None
		subject = msg['subject'] if 'from_subject' in msg else None
		text = msg['text']
		sql = "insert into email_inbox values(NULL,%s,%s,%s,%s,from_unixtime(%s))"
		self.db.query(sql,(from_email,from_name,subject,text,ts))
	
	def auth(self,data):
		try:
			signed_data = self.url
			sorted_key = sorted(data)
			for k in sorted_key:
				signed_data += k
				signed_data += data[k]
			expected = self._calc_signature(signed_data, self.key)
			signature = web.ctx.env['HTTP_X_MANDRILL_SIGNATURE']
			return expected==signature
		except:
			return False
		
	def _calc_signature(self, raw, key):
		hashed = hmac.new(key, raw, hashlib.sha1)
		return hashed.digest().encode("base64").rstrip('\n')
