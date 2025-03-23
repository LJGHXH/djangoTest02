<!DOCTYPE html>
<html lang="en">
<head>
    <title>$Title$</title>
    <meta charset="UTF-8">
    <link href="cs1.6.css" type="text/css" rel="stylesheet">
</head>

<form method="post" enctype="multipart/form-data" name="d1">
    <table class="a201">
        <caption>注册您的账户</caption>
        <tr>
            <td><label>
                    <input name="sign" type="text">
                </label>不超过10位的字符</td>
        </tr>
            <td><label>
                    <input name="psd" type="password">
                </label>不超过16位的密码</td>
        </tr>
        <tr>
            <td><label>
                    <input name="psdSure" type="password">
                </label>请再一次输入密码</td>
        </tr>
        <tr>
            <td><label>
                    <input name="submit" type="submit" value="确定注册">
                </label></td>
        </tr>
    </table>
</form>


<?php

require_once("./conn.php"); //连接数据库

if (isset($_POST['submit'])){

    if (!isset($_POST['sign'])) echo '用户名不能为空';     //判断用户名是否为空
    elseif (!isset($_POST['psd'])) echo '密码不能为空';   //判断密码是否为空
    else {

        //导入数据
        $sign=$_POST['sign'];
        $psd=$_POST['psd'];
        $psdSure=$_POST['psdSure'];

        if ($psd!==$psdSure) echo '两次密码输入不一致,请重新输入';    //判断两次输入的密码是否一致
        else{
            session_start();
            //存入注册的账户
            $sql_sign="INSERT INTO `users` (`id`, `psd`) VALUES ( '$sign', '$psd');";
            //为刚注册的账户建立借书表
            $sql_sign_book="CREATE TABLE IF NOT EXISTS `$sign` (
                                 `Bname` varchar(20) NOT NULL,
                                 `Wname` varchar(20) NOT NULL,
                                 `Bprice` float NOT NULL
                            ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=18 ;";
            //连接数据库
            $result01 = mysqli_query($link, $sql_sign);
            $result02 = mysqli_query($link, $sql_sign_book);
            session_destroy();

            echo '注册成功！请单击此处跳转<p><a href="d2_Login.php"> 点击我，跳转登录 </a></p>';

        }

    }

}
?>


