#!/bin/bash
#set -ex
set -e

#### todo
# 修改为死循环, 在该脚本中完成常用命令的缩写操作
# 添加 git add等快捷方式
# 封装为函数


current_branch=master

echo "请确认当前所处分支是否是(输入y/n): ${current_branch}"; read is_current
#read is_current
case ${is_current} in
"n")
  exit 1;;
esac
echo '------------------------------------------------------------------------------------'

# 获取当前脚本所在的目录
#cd "$(dirname "$0")"
cd `dirname "$0"`
echo "[当前目录: ] $(pwd)"

git add .
git status
#echo $?

echo '------------------------------------------------------------------------------------'
echo '请输入本次更新的注释:　'
read message

if [[ ${message} = "q" ]]
then
    # 通过输入 q, 直接推出当前脚本
    exit 1
elif [[ ${message} = "d" ]]
then
    echo "使用默认注释，进行更新"
    git commit -m "更新"
elif [[ -n ${message} ]]
then
    git commit -m "${message}"
else
    echo "请输入本次更新信息"
fi

echo '------------------------------------------------------------------------------------'
echo "是否向远程分支推送本次修改"
read is_push

case ${is_push} in
"y" | "yes")
  git push origin ${current_branch};;
"q" | "exit" | "e")
 echo "退出,不推送到远程分支"
 exit 1;;
 *)
 echo "退出";;
esac
echo '---------------------------------[end]-----------------------------------------------'


