from controllers.index import index
from controllers.login import login

from controllers.setting import setting
from controllers.setting.user import user

from controllers.travel import travel
from controllers.travel.pesanan import pesanan
urls = (
	'/','index',
	
	'/travel/','travel',
	'/travel/pesanan/(.*)','pesanan',
	
	'/setting/','setting',
	
	'/setting/user/','user',
	'/login/','login',
	
)
