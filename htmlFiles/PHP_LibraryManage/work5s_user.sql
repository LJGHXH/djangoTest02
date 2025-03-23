
SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- 数据库: `mydatabase`
--

-- --------------------------------------------------------

--
-- 表的结构 `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` varchar(10) NOT NULL,
  `psd` varchar(16) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=18 ;
-- 转存表中的数据 `users`
INSERT INTO `users` (`id`, `psd`) VALUES
( 'a001', '123');



--
CREATE TABLE IF NOT EXISTS `admini` (
  `Aid` varchar(10) NOT NULL,
  `Apsd` varchar(16) NOT NULL,
  PRIMARY KEY (`Aid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=18 ;

INSERT INTO `admini` (`Aid`, `Apsd`) VALUES
( 'admini', 'admini');


CREATE TABLE IF NOT EXISTS `book` (
  
  `Bname` varchar(20) NOT NULL,
  `Wname` varchar(20) NOT NULL,
  `Bprice` float NOT NULL,
  `Bintroduce` varchar(150) NOT NULL,
  `Bid` char(4) NOT NULL,
  `Bpic` varchar(20),
  PRIMARY KEY (`Bid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=18 ;

INSERT INTO `book` (`Bname`, `Wname`, `Bprice`, `Bintroduce`, `Bid`, `Bpic`) VALUES
( '狼图腾', '姜戎','34.5','《狼图腾》被誉为一部描绘蒙古草原狼的“旷世奇书”，它抒写了狼的团队精神和家族责任感，狼的智慧、顽强和尊严，倔强可爱的小狼在失去自由后艰难的成长过程，狼嗥、狼耳、狼眼、狼食、狼烟、狼旗……那些精灵般的狼仿佛随时能从书中呼啸而出。','w1','./pic/w1.jpg');

INSERT INTO `book` (`Bname`, `Wname`, `Bprice`, `Bintroduce`, `Bid`, `Bpic`) VALUES
( '活着', '余华','17.8','《活着》讲述了一个人历尽世间沧桑和磨难的一生，亦将中国大半个世纪的社会变迁凝缩其间。讲述了绝望的不存在；讲述了人是为了活着本身而活着的，而不是为了活着之外的任何事物而活着。','w2','./pic/w2.jpg');

INSERT INTO `book` (`Bname`, `Wname`, `Bprice`, `Bintroduce`, `Bid`, `Bpic`) VALUES
( '围城', '钱钟书','22.9','钱锺书所著的《围城》是一幅栩栩如生的世井百态图，人生的酸甜苦辣千般滋味均在其中得到了淋漓尽致的体现。钱钟书先生将自己的语言天才并入极其渊博的知识，再添加上一些讽刺主义的幽默调料，以一书而定江山。','w3','./pic/w3.jpg');

INSERT INTO `book` (`Bname`, `Wname`, `Bprice`, `Bintroduce`, `Bid`, `Bpic`) VALUES
( '白鹿原', '陈忠实','19.9','《白鹿原》两个家族为争夺白鹿原的统治上演了一幕幕惊心动魄的争斗：巧取风水地，恶施美人计，孝子为匪，亲翁杀媳，兄弟相煎，情人反目……  ','w4','./pic/w4.jpg');

INSERT INTO `book` (`Bname`, `Wname`, `Bprice`, `Bintroduce`, `Bid`, `Bpic`) VALUES
( '谁在敲门', '罗伟章','44','《谁在敲门》人物众多，以许家为核心，描写在风起云涌的时代背景之下，土地对农民的束缚已走向瓦解，依附在土地之上的乡村伦理道德也走向瓦解与重构，三代农民子女的命运变迁，让人切实触摸到当下现实的温度，有一种厚重的历史感，也激发读者对生命、生活、亲情的反思。小说呈现了广阔丰饶的民族性格和深刻的社会内涵。','w5','./pic/w5.jpg');

INSERT INTO `book` (`Bname`, `Wname`, `Bprice`, `Bintroduce`, `Bid`, `Bpic`) VALUES
( '小熊和最好的爸爸', '阿兰德·丹姆','17.5','因为小熊父子的真情交流，单纯、温馨又细致动人，那份相依为命、亲密无间的父子情，被作者拿捏得恰到好处，让你从心中涌起亲切而湿润的感动。','t1','./pic/t1.jpg');

INSERT INTO `book` (`Bname`, `Wname`, `Bprice`, `Bintroduce`, `Bid`, `Bpic`) VALUES
( '会飞的挖土机', '伊恩· 威柏','9.9','泰迪和鲁比从格兰戴姆先生那里得到了两辆玩具挖土机：一辆是反铲装载机，一辆是伸缩臂叉车。然而不可思议的事情发生了，这两辆玩具挖土机居然变成了真正的挖土机，而且还飞了起来……','t2','./pic/t2.jpg');

INSERT INTO `book` (`Bname`, `Wname`, `Bprice`, `Bintroduce`, `Bid`, `Bpic`) VALUES
( '爱哭的猫头鹰', '鲍尔·菲尔斯特','11.2','是谁哭得这么大声？是可怕的威尔伯老狼吗？不，只是一只猫头鹰小宝宝。刺猬、乌鸦、松鼠、鼹鼠、鹿角甲虫都来哄他，大家想尽一切办法让它安静下来。','t3','./pic/t3.jpg');

INSERT INTO `book` (`Bname`, `Wname`, `Bprice`, `Bintroduce`, `Bid`) VALUES
( '世界真好', '吉莉安','10.5','小老鼠睡不着，看着其他的兄弟姐妹都进入了甜甜的梦乡，他偷偷跑出了洞外。在洞外他发现了一个奇妙的世界：嗡嗡的蜜蜂，飞舞的蝴蝶，明亮的蓝天……','t4');

INSERT INTO `book` (`Bname`, `Wname`, `Bprice`, `Bintroduce`, `Bid`, `Bpic`) VALUES
( '小彗星旅行记', '徐刚','21.9','向往光明和温暖的小彗星哈伊，在“好运气”的帮助下，历尽艰辛，穿越太阳系，沿途拜访了海王星、天王星、土星、木星、火星、地球、金星和水星，终于见到了向往已久的太阳。读了这本书，相信小朋友一定能够爱上小彗星、爱上天文。','c1','./pic/c1.jpg');

INSERT INTO `book` (`Bname`, `Wname`, `Bprice`, `Bintroduce`, `Bid`, `Bpic`) VALUES
( '冰冻星球 超乎想象的奇妙世界', '阿拉斯泰尔','46.4','冰冻的海洋和恶劣的气候将两极与其他地区隔离开来，两极的很多动物仅存活于此。如今两极地区都在慢慢融化，给这里的生命带来了深远的影响','c2','./pic/c2.jpg');

INSERT INTO `book` (`Bname`, `Wname`, `Bprice`, `Bintroduce`, `Bid`, `Bpic`) VALUES
( '数学花园漫游记', '马锡文','8.6','如果我们住在土星的光环上通向“色数”的桥梁——欧拉公式四色问题的副产品——莫比乌斯环试验田里的数学如果找不到大块田 再走一步——回到了几何学中图的世界最短路程问题','c3','./pic/c3.jpg');


--
CREATE TABLE IF NOT EXISTS `a001_book` (
  
  `Bname` varchar(20) NOT NULL,
  `Wname` varchar(20) NOT NULL,
  `Bprice` float NOT NULL

) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=18 ;

INSERT INTO `a001_book` (`Bname`, `Wname`,`Bprice`) VALUES
( '狼图腾','姜戎','34.5');