<?php

if(isset($_GET['speechinput'])){
	
	// conf
	$ip = "tcp://192.168.1.40";
	$lang = "ru";
	
	$data = array(
		"body" => "jarvis " . $_GET['speechinput'],
		"type" => "chat",
		"from" => "IVR"
	);
	$data_string = json_encode($data);
	
	$handle = fsockopen($ip, 10042, $errno, $errstr, 1);
	if(!$handle){
		echo "Unable to open\n";
	}else{
		
		fwrite($handle, $data_string);
		stream_set_timeout($handle, 2);
		$res = fread($handle, 1024);
		
		$info = stream_get_meta_data($handle);
		fclose($handle);
		
		if($info['timed_out'])
			echo 'Connection timed out!';
	}
	
	$tmp = json_decode($res);
	
	$text = urlencode(iconv("UTF-8", "UTF-8", $tmp->body));
	$ttsurl = "http://translate.google.com/translate_tts?tl=$lang&q=$text";
	$uagent = "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.872.0 Safari/535.2";

	$ch = curl_init($url);
	curl_setopt($ch, CURLOPT_URL, $ttsurl);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_HEADER, 0);
	curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
	curl_setopt($ch, CURLOPT_ENCODING, "");
	curl_setopt($ch, CURLOPT_USERAGENT, $uagent);
	curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 120);
	curl_setopt($ch, CURLOPT_TIMEOUT, 120);
	curl_setopt($ch, CURLOPT_MAXREDIRS, 10);
	$content = curl_exec($ch);
	curl_close($ch);
	
	header('Content-Type: audio/mpeg');
	header('Cache-Control: no-cache');
	print $content;
}else{
	?>
<html>
<head>
<title>.: Jarvis :.</title>
<script>
                    function submitandclear(){
                        if(document.getElementById('speechinput').value != ""){
                            document.jarvisform.submit();
                            console.log(document.getElementById('speechinput').value);
                            document.getElementById('speechinput').value = "";
                        }
                    }
                </script>
</head>
<body>
	<form method="get" name="jarvisform" id="jarvisform"
		action="<?=$_SERVER['PHP_SELF']?>" target="voiceframe">
		<input name="speechinput" id="speechinput" type="text"
			onFocus="submitandclear(this);" style="width: 20px;" x-webkit-speech />
		<!--input type="submit" value="ASK" /-->
	</form>
	<iframe width="0px" height="0px" style="border: 0px;" src="about:none"
		name="voiceframe"></iframe>

	<div id="log"></div>

</body>
</html>
<?
}
