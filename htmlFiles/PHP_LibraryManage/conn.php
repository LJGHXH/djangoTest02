<?php
$hostname ="localhost";
$username ="root";
$psd ='123';
$link =@mysqli_connect($hostname,$username,$psd) or die('数据库连接失败');
mysqli_select_db($link,'final_book') or die('没有找到数据库'.mysqli_error());
mysqli_query($link,"set names utf8"); //设置字符编码
