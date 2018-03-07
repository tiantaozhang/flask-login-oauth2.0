# flask-login-oauth2
flask flask-login google oauth2.0


### 步骤
1. pip install requirement.txt
2. 复制config中的sample并填写相关配置
3. [google app 注册](https://code.google.com/apis/console#access) 注册应用，并开放权限，并填写相应的配置
4. 本地mysql和redis
5. python manage.py runserver -p 9000


好了，愉快地跑起来了

浏览器访问：
[http://127.0.0.1:9000](http://127.0.0.1:9000)

登录：[http://127.0.0.1:9000/login?email=xxx@gmail.com](http://127.0.0.1:9000/login?email=xxx@gmail.com)