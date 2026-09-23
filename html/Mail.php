<?php
	
require_once './Email.php';
     $content=$_POST['textarea']; //内容
     $name=$_POST['name']; //名字
     $uemail = $_POST['uemail'];//邮箱
     $contact=$_POST['contact']; //联系方式
     $content = "反馈:".$content."</br>";
     $name ="名字:".$name."</br>";
     $uemail ="邮箱：".$uemail."</br>";
     $contact = "联系方式:".$contact."</br>";
     $coreEmail = new Email();
     // SMTP服务器
    $smtpserver = "smtp.exmail.qq.com";
    
    // SMTP服务器端口 
     $smtpserverport = "465"; //587/465

     // SMTP服务器的用户邮箱
    $smtpusermail = "hi@hispeedcity.com";
    // $smtpusermail = "steve@hispeedcity.com";

     // SMTP服务器的用户密码
     $smtppass = "Hi123456";   //igrtwgblcmxlbhca

     // 发送给谁
    //  $smtpemailto = "bc@bosolution.cn";
    $smtpemailto = "hi@hispeedcity.com";

     // 邮件主题
     $mailtitle = '用户反馈';
     // 邮件内容
     $mailcontent = $content.$name.$contact;

    
    //$this->coreEmail->setServer("smtp@126.com", "XXXXX@126.com", "XXXXX"); //设置smtp服务器，普通连接方式
    $coreEmail->setServer($smtpserver, $smtpusermail, $smtppass, $smtpserverport, true); //设置smtp服务器，到服务器的SSL连接
     
    $coreEmail->setFrom($smtpusermail); //设置发件人
    $coreEmail->setReceiver($smtpemailto);
    $coreEmail->setMail($mailtitle, $mailcontent); //设置邮件主题、内容
    $sendResult = $coreEmail->sendMail(); //发送
	//var_dump($sendResult); //打印的值为false  csw {谦哥改过密码,测试完毕}
	$msg = "We have received your feedback.";
	$status =1;
    echo json_encode($msg,$status);

?>
