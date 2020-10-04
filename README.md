# flask-blog-v1
个人博客项目

### 项目初始化
1. 数据库迁移文件生成 ?? 未实现
```bash
# 添加flask-migrate扩展后，flask自动添加了一系列 flask db [args]终端命令; 通过 --help 查看
 flask db --help
# 生成迁移文件 
 flask db init
# 首次生成迁移文件
 flask db migrate
 flask db migrate -m 'msg'

# 更新数据库变动
 flask db upgrade
```
### bug: 创建的数据库有问题

2. 创建数据库，添加账号和基本数据
```bash
flask inidb

flask init --username benny --password blogdog
```

3. 生成测试数据
```bash
flask forge
# 可以查询参数，自定义参数
```

4.启动项目
```bash
flask run -p 8000
```