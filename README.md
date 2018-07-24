# 目录规划

```
/cnblog/  
| -- blog/  
	 | -- migrations/        # 基于当前的model创建新的迁移策略文件 
	 | -- templatetags /
		  | -- my_tags.py        # 自定义标签或者过滤器
	 | -- utils        # 封装的自定义方法
	 | -- admin.py        # 配置模型modles在django原生后台的管理 
	 | -- app.py        # 应用级别的配置
	 | -- models.py        # 模型定义
	 | -- my_forms.py        # 表单验证
	 | -- tests.py        # 测试
	 | -- views.py        # 视图函数
| -- cnblog/
	 | -- settings.py        # 项目配置
	 | -- urls.py        # 路由控制
	 | -- wsgi.py        # 内置runserver命令的WSGI应用配置
| -- media/        # 用户上传文件
	 | -- article_image/        # 用户添加文章时插入的图片
	 | -- avatars/        # 用户头像
| -- static/
	 | -- blog/        # blog应用的所有静态文件
	 	  | -- avatars/        # 用户默认头像
	 	  | -- css/        # css文件
	 	  | -- font/        # 字体文件
	 	  | -- image/        # 项目需要用到的图像
	 	  | -- js/        # js文件
	 	  | -- kindeditor        # 富文本编辑框
| -- templates/        # 视图模板文件
	 | -- back_stage        # 后台管理视图模板
	 | -- xxx.html
| -- manage.py        # 命令操作
```

# 实现功能

- 基于auth模块和Ajax实现登录验证

- 基于forms组件和Ajax实现注册功能

- 设计博客首页

- 设计个人站点页面

- 设计文章详情页面

- 实现文章点赞功能

- 实现文章的评论功能，包括对文章的评论以及对文章评论的评论

- 实现富文本编辑框

- 防止xss攻击（例如当用户的文章中含有JS代码，其他用户进行访问时浏览器会执行JS代码，大大降低了用户的安全性）

# 操作事项

```
启动项目之后，在浏览器输入127.0.0.1:8000/login 进入登录界面
已经注册的用户名：GYQ，密码：gyq13142
```
