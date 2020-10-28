#!/bin/bash
#set -ex
set -e
#export LC_ALL=zh_CN.UTF-8
#export LANG=zh_CN.UTF-8
# git 提交编码方式警告处理:https://blog.csdn.net/blankrabbit/article/details/80609572
# git config --global i18n.commitencoding utf-8

#### todo
# 修改为死循环, 在该脚本中完成常用命令的缩写操作
# 添加 git add等快捷方式
# 封装为函数

push_branch=master

current_branch="$(git symbolic-ref --short -q HEAD)"

# 获取当前脚本所在的目录
#cd "$(dirname "$0")"
cd `dirname "$0"`
echo "[当前目录: ] $(pwd)"

echo "[当前所在分支名称]: ${current_branch}"
if [[ $current_branch != $push_branch ]]
then
   echo "当前所处分支与推送远程分支不一致!"
   echo "是否将推送分支${push_branch}修改为当前分支${current_branch}"; read is_change
   if test ${is_change} = "y"
   then
       push_branch=${current_branch}
   else
       exit 1
   fi
fi

#echo "请确认当前所处分支是否是(输入y/n): ${current_branch}"; read is_current
##read is_current
#case ${is_current} in
#"n")
#  echo "退出: 当前分支不正确"
#  exit 1;;
#esac

echo '------------------------------------------------------------------------------------'



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
    if test "$(git commit -m 更新)"
    then
       git status
       echo "[commit success!]"
    else
       echo "[commit fail!]"
    fi
elif [[ -n ${message} ]]
then
    if test "$(git commit -m ${message})"
    then
       git status
       echo "[commit success!]"
    else
       echo "[commit fail!]"
    fi
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


