<!DOCTYPE html>
<html lang="en">
<head>
    <title>$Title$</title>
    <meta charset="UTF-8">
    <link href="cs1.6.css" type="text/css" rel="stylesheet">
</head>

<form method="post" enctype="multipart/form-data" name="d2" >
    <table class="a2">
        <caption>登录您的账户</caption>
        <tr>
            <td><label>
                    <input name="id" type="text">
                </label>输入您的用户名</td>
        </tr>
        <td><label>
                <input name="psd" type="password">
            </label>请输入您的密码</td>
        </tr>

        <tr>
            <td><label>
                    <input name="submit" type="submit" value="登录">
                </label></td>
        </tr>
    </table>
</form>

<?php

require_once("./conn.php");

session_start();

include "d3_book.php";
include "d3a_book.php";

if (!isset($_POST['submit'])){

    if (!isset($_POST['id'])) echo '用户名不能为空';     //判断用户名是否为空
    elseif (!isset($_POST['psd'])) echo '密码不能为空';   //判断密码是否为空
    else{

        //导入登录账号数据
        $id=$_POST['id'];
        $psd=$_POST['psd'];

        //从数据库中匹配数据
        $sql_id = "select id from users;";
        $sql_psd = "select psd from work5s_user;";
        $result_id = mysqli_query($link, $sql_id);
        $result_psd = mysqli_query($link, $sql_id);

        while ($row = mysqli_fetch_assoc($result_id)) {
            if ($id == $row['id']) {
                while ($row = mysqli_fetch_assoc($result_psd)) {
                    if ($psd== $row['psd']) {
                        echo "登陆成功</br>";
                    }
                }
            }
        }

    }


}

