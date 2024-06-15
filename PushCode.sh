#!/bin/bash

# 获取今天的日期
today=$(date "+%Y-%m-%d")

git add ./

# 使用git commit命令，并附带今天的日期作为提交信息
git commit -m "Commit on $today"

# 执行git push命令
git push -f