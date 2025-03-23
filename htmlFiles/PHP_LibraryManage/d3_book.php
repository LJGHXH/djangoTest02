<!DOCTYPE html>
<html lang="en">
<head>
    <title>$Title$</title>
    <meta charset="UTF-8">
    <link href="cs1.6.css" type="text/css" rel="stylesheet">
</head>
<?php

require_once("./conn.php");

if (!isset($_POST['submit'])) echo '请先登录';
else{


    if (!isset($_POST['id'])) echo '用户名不能为空';     //判断用户名是否为空
    elseif (!isset($_POST['pw'])) echo '密码不能为空';   //判断密码是否为空
    else{


    }


}